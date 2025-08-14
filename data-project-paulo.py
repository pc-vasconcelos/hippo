import os
import re
import json
import subprocess
import sys

# Ensure pandas is installed
try:
    import pandas as pd
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd

# Set base directory and data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
claims_path = os.path.join(BASE_DIR, 'data', 'claims')
pharmacies_path = os.path.join(BASE_DIR, 'data', 'pharmacies')
reverts_path = os.path.join(BASE_DIR, 'data', 'reverts')

# Create output directory if it does not exist
os.makedirs(os.path.join(BASE_DIR, 'output'), exist_ok=True)

# Function to read all JSON and CSV files from a folder and concatenate them into a DataFrame
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

# Read data from folders
claims_df = read_data_folder(claims_path)
pharmacies_df = read_data_folder(pharmacies_path)
reverts_df = read_data_folder(reverts_path)

# Merge claims with reverts and pharmacies data
merged_df = claims_df.merge(reverts_df, left_on='id', right_on='claim_id', how='left', suffixes=('', '_revert'))
merged_df = merged_df.merge(pharmacies_df, on='npi', how='left')

# Calculate metrics for each npi and ndc
metrics_df = merged_df.groupby(['npi', 'ndc']).agg(
    fills=('id', 'nunique'),
    reverted=('id_revert', 'nunique'),
    avg_price=('price', 'mean'),
    total_price=('price', 'sum')
).reset_index()

# Save metrics to JSON file
metrics_df.to_json(os.path.join(BASE_DIR, 'output', 'metrics.json'), orient='records', lines=False, force_ascii=False, indent=3)

# Get two lowest avg_price for each ndc and chain
recommend_df = merged_df.groupby(['ndc', 'chain']).agg(
    avg_price=('price', 'mean')   
).reset_index().sort_values('avg_price').groupby('ndc').head(2).sort_values('ndc')

# Format recommended output for JSON
recommend_output = (
    recommend_df
    .rename(columns={'chain': 'name'})
    .groupby(['ndc'])[['name', 'avg_price']]
    .apply(lambda x: x.to_dict('records'))
    .reset_index(name='chain')
    .to_dict('records')
)

# Save recommend output to JSON file
with open(os.path.join(BASE_DIR, 'output', 'recommend.json'), 'w', encoding='utf-8') as f:
    json.dump(recommend_output, f, ensure_ascii=False, indent=3)

# Find the 5 most common quantities for each ndc
most_commom = claims_df.groupby(['ndc', 'quantity']).agg(
    count=('quantity', 'count')
).reset_index().sort_values(['ndc', 'count'], ascending=False).groupby('ndc').head(5)

# Format most common output for JSON
most_commom_output = (
    most_commom
    .rename(columns={'quantity': 'most_prescribed_quantity'})
    .groupby(['ndc'])['most_prescribed_quantity']
    .apply(list)
    .reset_index()
    .to_dict('records')
)

most_commom_path = os.path.join(BASE_DIR, 'output', 'most-commom.json')

# Save most common output to JSON file
with open(most_commom_path, 'w', encoding='utf-8') as f:
    json.dump(most_commom_output, f, ensure_ascii=False, indent=3)

# Read the JSON file for post-processing
with open(most_commom_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to format lists: add indentation and put all numbers on the same line
content = re.sub(
    r'\[\s*([\d\.,\s]+)\s*\]',
    lambda m: '[\n          ' + ' '.join(x.strip() for x in m.group(1).splitlines() if x.strip()) + '\n      ]',
    content
)

# Write the formatted content back to the JSON file
with open(most_commom_path, 'w', encoding='utf-8') as f:
    f.write(content)