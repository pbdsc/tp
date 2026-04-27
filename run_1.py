rm_batches = ['batch_1', 'batch_2', 'batch_3', 'batch_4']
orders = ['o1', 'o2', 'o3', 'o4', 'o5', 'o6']
q_params = ['qlty_1', 'qlty_2', 'qlty_3']

rm = {
        'batch_1':{'inv_qty': 5, 'grade': 'top', 'prem_grade': 'y', 'qlty_1': 0.5, 'qlty_2': 0.7, 'qlty_3': 4.2, 'exp_days': 1, 'exp_flag': 'y'},
        'batch_2':{'inv_qty': 15, 'grade': 'mid', 'prem_grade': 'n', 'qlty_1': 0.6, 'qlty_2': 0.9, 'qlty_3': 4.1, 'exp_days': 16, 'exp_flag': 'n'},
        'batch_3':{'inv_qty': 5, 'grade': 'bottom', 'prem_grade': 'n', 'qlty_1': 0.5, 'qlty_2': 0.6, 'qlty_3': 5.7, 'exp_days': 2, 'exp_flag': 'y'},
        'batch_4':{'inv_qty': 15, 'grade': 'top', 'prem_grade': 'y', 'qlty_1': 0.55, 'qlty_2': 0.65, 'qlty_3': 4.25, 'exp_days': 25, 'exp_flag': 'n'}
      }

fg_order = {
            'o1':{'cust': 'c1', 'day': 1, 
                  'qty': 10, 'demand_rm': 5, 
                  'batch_count_rm_min': 1, 'batch_count_rm_max': 2, 
                  'qlty_1_ucl': 0.9, 'qlty_1_lcl': 0.7, 'qlty_1_cl': 0.8, 
                  'qlty_2_ucl': 5.0, 'qlty_2_lcl': 4.6, 'qlty_2_cl': 4.8, 
                  'qlty_3_ucl': 6.0, 'qlty_3_lcl': 5.5, 'qlty_3_cl': 5.75},
            'o2':{'cust': 'c2', 'day': 1, 
                  'qty': 15, 'demand_rm': 6, 
                  'batch_count_rm_min': 1, 'batch_count_rm_max': 2, 
                  'qlty_1_ucl': 0.95, 'qlty_1_lcl': 0.75, 'qlty_1_cl': 0.85, 
                  'qlty_2_ucl': 6, 'qlty_2_lcl': 5, 'qlty_2_cl': 5.5, 
                  'qlty_3_ucl': 5.75, 'qlty_3_lcl': 5.25, 'qlty_3_cl': 5.5},
            'o3':{'cust': 'c3', 'day': 2, 
                  'qty': 5, 'demand_rm': 2, 
                  'batch_count_rm_min': 2, 'batch_count_rm_max': 4, 
                  'qlty_1_ucl': 0.95, 'qlty_1_lcl': 0.75, 'qlty_1_cl': 0.85, 
                  'qlty_2_ucl': 5.0, 'qlty_2_lcl': 4.6, 'qlty_2_cl': 4.8, 
                  'qlty_3_ucl': 8, 'qlty_3_lcl': 7, 'qlty_3_cl': 7.5},
            'o4':{'cust': 'c1', 'day': 2, 
                  'qty': 15, 'demand_rm': 7.5, 
                  'batch_count_rm_min': 1, 'batch_count_rm_max': 2, 
                  'qlty_1_ucl': 0.9, 'qlty_1_lcl': 0.7, 'qlty_1_cl': 0.8, 
                  'qlty_2_ucl': 5.0, 'qlty_2_lcl': 4.6, 'qlty_2_cl': 4.8, 
                  'qlty_3_ucl': 6.0, 'qlty_3_lcl': 5.5, 'qlty_3_cl': 5.75},
            'o5':{'cust': 'c1', 'day': 2, 
                  'qty': 10, 'demand_rm': 5, 
                  'batch_count_rm_min': 1, 'batch_count_rm_max': 2, 
                  'qlty_1_ucl': 0.9, 'qlty_1_lcl': 0.7, 'qlty_1_cl': 0.8, 
                  'qlty_2_ucl': 5.0, 'qlty_2_lcl': 4.6, 'qlty_2_cl': 4.8, 
                  'qlty_3_ucl': 6.0, 'qlty_3_lcl': 5.5, 'qlty_3_cl': 5.75},
            'o6':{'cust': 'c2', 'day': 3, 
                  'qty': 20, 'demand_rm': 8, 
                  'batch_count_rm_min': 1, 'batch_count_rm_max': 2, 
                  'qlty_1_ucl': 0.95, 'qlty_1_lcl': 0.75, 'qlty_1_cl': 0.85, 
                  'qlty_2_ucl': 6, 'qlty_2_lcl': 5, 'qlty_2_cl': 5.5, 
                  'qlty_3_ucl': 5.75, 'qlty_3_lcl': 5.25, 'qlty_3_cl': 5.5}
            }

allowed_grade = {
                ('o1','batch_1'):1,
                ('o1','batch_2'):0,
                ('o1','batch_3'):1,
                ('o1','batch_4'):1,
                ('o2','batch_1'):0,
                ('o2','batch_2'):1,
                ('o2','batch_3'):0,
                ('o2','batch_4'):0,
                ('o3','batch_1'):1,
                ('o3','batch_2'):0,
                ('o3','batch_3'):1,
                ('o3','batch_4'):1,
                ('o4','batch_1'):1,
                ('o4','batch_2'):0,
                ('o4','batch_3'):1,
                ('o4','batch_4'):1,
                ('o5','batch_1'):1,
                ('o5','batch_2'):0,
                ('o5','batch_3'):1,
                ('o5','batch_4'):1,
                ('o6','batch_1'):0,
                ('o6','batch_2'):1,
                ('o6','batch_3'):0,
                ('o6','batch_4'):0
                 }

W1_GRADE = 5 
W2_QLTY_VIOLATION = 10
W3_EXPIRY = 2

import blend
blend.multi_prod_blend(rm_batches, orders, q_params, rm, fg_order, allowed_grade, W1_GRADE, W2_QLTY_VIOLATION, W3_EXPIRY)