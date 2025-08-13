import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
claims_path = os.path.join(BASE_DIR, 'data', 'claims')
pharmacies_path = os.path.join(BASE_DIR, 'data', 'pharmacies')
reverts_path = os.path.join(BASE_DIR, 'data', 'reverts')

def read_data_folder(folder_path):
    dfs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            df = pd.read_json(file_path, lines=False, dtype={'npi': str, 'ndc': str})
            dfs.append(df)
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path, dtype={'npi': str, 'ndc': str})
            dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    else:
        return pd.DataFrame()

claims_df = read_data_folder(claims_path)
pharmacies_df = read_data_folder(pharmacies_path)
reverts_df = read_data_folder(reverts_path)

merged_df = claims_df.merge(reverts_df, left_on='id', right_on='claim_id', how='left', suffixes=('', '_revert'))

metrics_df = merged_df.groupby(['npi', 'ndc']).agg(
    fills=('id', 'nunique'),
    reverted=('id_revert', 'nunique'),
    avg_price=('price', 'mean'),
    total_price=('price', 'sum')
).reset_index()

metrics_df.to_json(os.path.join(BASE_DIR, 'output', 'metrics.json'), orient='records', lines=False, force_ascii=False)
#test