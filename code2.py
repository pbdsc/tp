import pandas as pd

def group_duplicate_columns(df):
    """
    Identifies and groups columns with identical values into an output DataFrame
    with a group number.

    Args:
        df: The input pandas DataFrame.

    Returns:
        A pandas DataFrame mapping column names to their group number.
    """
    # Transpose the DataFrame to treat columns as rows for easier duplicate checking
    df_transposed = df.T
    
    # Use duplicated() to find duplicate rows (original columns)
    # keep=False marks all duplicates as True, including the first occurrence
    duplicated_mask = df_transposed.duplicated(keep=False)
    
    # Select only the duplicated columns
    duplicated_cols_transposed = df_transposed[duplicated_mask]
    
    # Create a mapping of unique column value sets to a group ID
    unique_cols = duplicated_cols_transposed.drop_duplicates()
    group_map = {tuple(unique_cols.iloc[i]): f'Group_{i+1}' for i in range(len(unique_cols))}
    
    # Map original column names to their group ID
    col_to_group = {}
    for col_name, col_values in duplicated_cols_transposed.iterrows():
        # Use tuple(col_values) as the key for dictionary lookup
        col_to_group[col_name] = group_map[tuple(col_values)]
    
    # Create the output DataFrame
    output_df = pd.DataFrame(list(col_to_group.items()), columns=['Column_Name', 'Group_ID'])
    
    # Optional: Add non-duplicated columns to the output, if desired (e.g., as 'Unique')
    # non_duplicated_cols = df.columns[~duplicated_mask]
    # unique_df = pd.DataFrame({'Column_Name': non_duplicated_cols, 'Group_ID': 'Unique'})
    # output_df = pd.concat([output_df, unique_df], ignore_index=True)
    
    return output_df

# Example Usage
data = {
    'col_a': [1, 2, 3, 4],
    'col_b': [1, 2, 3, 4],
    'col_c': [5, 6, 7, 8],
    'col_d': [1, 2, 3, 4],
    'col_e': [9, 0, 1, 2],
    'col_f': [5, 6, 7, 8]
}
df = pd.DataFrame(data)

duplicate_groups_df = group_duplicate_columns(df)
print(duplicate_groups_df)