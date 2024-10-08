import pandas as pd
import os

directory = 'input'

file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

dfs = [pd.read_csv(file_path) for file_path in file_paths]

# cleaning data
def clean_data(dfs):
    for i, df in enumerate(dfs):
        
        if 'created_utc' in df.columns:
            # convert 'created_utc' to datetime
            try:
                df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
            except ValueError:
                df['created_utc'] = pd.to_datetime(df['created_utc'])

            # missing value
            df.fillna({'crosspost_subreddits': '', 'body': '', 'is_bot': ''}, inplace=True)

    return dfs

dfs = clean_data(dfs)