import gurobipy as gp
from gurobipy import GRB


def multi_prod_blend(rm_batches, orders, q_params, rm, fg_order, allowed_grade, W1_GRADE, W2_QLTY_VIOLATION, W3_EXPIRY):

    # --- Model Initialization ---
    model = gp.Model("Batch_Limited_Multi_Blend")

    # --- Decision Variables (Sparse approach) ---
    valid_pairs = [(i, o) for i in rm_batches for o in orders 
                if allowed_grade[(o, i)] == 1
                and rm[i]['exp_days'] >= fg_order[o]['day']]

    x = model.addVars(valid_pairs, name="qty_rm_batch", lb=0.0)
    y = model.addVars(valid_pairs, vtype=GRB.BINARY, name="batch_count")

    # Deviation variables (These represent the error in 'Quality Units')
    valid_pairs_qlty = [(o, k) for o in orders for k in q_params if k + '_ucl' in fg_order[o]]
    dev_plus = model.addVars(valid_pairs_qlty, lb=0, name="dev_plus")
    dev_minus = model.addVars(valid_pairs_qlty, lb=0, name="dev_minus")

    # --- OBJECTIVE FUNCTION ---
    obj_grade_penalty = gp.quicksum(x[i, o] for i, o in valid_pairs if rm[i]['prem_grade'] == 'y')
    obj_quality_violation_penalty = gp.quicksum(dev_plus[o,k] + dev_minus[o,k] for o, k in valid_pairs_qlty)
    obj_expiry_penalty = gp.quicksum(rm[i]['inv_qty'] for i, o in valid_pairs if rm[i]['exp_flag'] == 'y') -  \
                        gp.quicksum(x[i, o] for i, o in valid_pairs if rm[i]['exp_flag'] == 'y')

    model.setObjective(W1_GRADE * obj_grade_penalty + W2_QLTY_VIOLATION * obj_quality_violation_penalty + W3_EXPIRY * obj_expiry_penalty, GRB.MINIMIZE)

    # --- Constraints ---

    # Quality constraints
    for o, k in valid_pairs_qlty:
        FGLQP = {}

        if k == 'qlty_1':
            FGLQP[o,k] = gp.quicksum(x[i, o]*(1.5*rm[i][k]) for i, o in valid_pairs if orders[0] == o)
        elif k == 'qlty_2':
            FGLQP[o,k] = gp.quicksum(x[i, o]*(2.7*rm[i][k] + 0.3) for i, o in valid_pairs if orders[0] == o)
        elif k == 'qlty_3':
            FGLQP[o,k] = gp.quicksum(x[i, o]*(1.4*rm[i][k] - .17) for i, o in valid_pairs if orders[0] == o)

#        fg_qlty_centerline = (fg_order[o][k+'_ucl'] + fg_order[o][k+'_lcl'])/2

        model.addConstr(FGLQP[o,k] == (fg_order[o][k+'_cl'] + dev_plus[o,k] - dev_minus[o,k])*gp.quicksum(x[i, o] for i, o in valid_pairs if orders[0] == o),
                        name=f"qc_{o}_{k}"
                        )

    # Other constraints
    for o in orders:
        lst_valid_rm = [tup[0] for tup in valid_pairs if tup[1] == o]
#        print('Order:', o)
#        print('Valid RMs:', lst_valid_rm)
        model.addConstr(gp.quicksum(x[i, o] for i in lst_valid_rm) == fg_order[o]['demand_rm'], 
                        name=f"demandrm_{o}")
        model.addConstr(gp.quicksum(y[i, o] for i in lst_valid_rm) >= fg_order[o]['batch_count_rm_min'], 
                        name=f"bcmin_{o}")
        model.addConstr(gp.quicksum(y[i, o] for i in lst_valid_rm) <= fg_order[o]['batch_count_rm_max'], 
                        name=f"bcmax_{o}")

    for i in rm_batches:
        lst_valid_o = [tup[1] for tup in valid_pairs if tup[0] == i]
        model.addConstr(gp.quicksum(x[i, o] for o in orders if o in valid_pairs) <= rm[i]['inv_qty'], name=f"inv_{i}")

    for i, o in valid_pairs:
        model.addConstr(x[i, o] >= 0, name=f"rmpos_{o}_{i}")
        model.addConstr(x[i, o] <= min(rm[i]['inv_qty'], fg_order[o]['demand_rm'])*y[i,o], name=f"rm_mininv_demandrm_{o}_{i}")
        if rm[i]['exp_days'] < fg_order[o]['day']:
            model.addConstr(x[i, o] == 0, name=f"rmexp_{o}_{i}")

    # ------ Solve ------
    model.setParam('DualReductions', 0)
    model.optimize()
    print (model.Status)
    if model.Status == GRB.OPTIMAL:
        for o in orders:
            print(f"\nResults for Order {o}:")
            actual_points = 0
            lst_valid_rm = [tup[0] for tup in valid_pairs if tup[1] == o]
            for i in lst_valid_rm:
                if x[i, o].X > 0.01:
                    print(f"  - Lot {i}: {x[i, o].X:.2f} units")
#                    lot_fg_q = (2 * rm_batches[i]['q']) + 15
#                    print(f"  - Lot {i}: {x[i, o].X:.2f} units | Lot FG Quality: {lot_fg_q}")
#                    actual_points += lot_fg_q * x[i, o].X
            
#            final_q = actual_points / orders[o]['demand']
#            print(f"Final Weighted Average FG Quality: {final_q:.4f} (Target: {orders[o]['centerline']})")

    if model.Status == GRB.INFEASIBLE:
        print("Model is infeasible. Computing IIS...")
        model.computeIIS()
        model.write("model.ilp")
        print("IIS written to file 'model.ilp'. Open this file to see the conflicting constraints.")