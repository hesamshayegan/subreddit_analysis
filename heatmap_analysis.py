import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_preprocessor import dfs


selected_subreddit = "pics"


dataframes = []
for df in dfs:
    dataframes.append(df)


combined_df = pd.concat(dataframes, ignore_index=True)

filtered_df = combined_df[combined_df['subreddit'] == selected_subreddit]

filtered_df['created_utc'] = pd.to_datetime(filtered_df['created_utc'], unit='s')

filtered_df['year'] = filtered_df['created_utc'].dt.year
filtered_df['month'] = filtered_df['created_utc'].dt.month

# normalize scores (score / max score)
filtered_df['normalized_score'] = filtered_df['score'] / filtered_df['score'].max()

# creating pivot table for heatmap
heatmap_data = filtered_df.pivot_table(
    values='normalized_score',
    index='year',
    columns='month',
    aggfunc='max'
)


plt.figure(figsize=(12, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="viridis",
    linewidths=0.5,
    cbar_kws={'label': 'Normalized Score'}
)

plt.title(f"Normalized Scores Heatmap for '{selected_subreddit}'", 
          fontdict={'family': 'monospace',
                    'size': 12,
                    'weight':'bold',
                    'style': 'italic'})
plt.xlabel("Month", fontsize=12)
plt.ylabel("Year", fontsize=12)
plt.xticks(
    ticks=range(1, 13), 
    labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
    rotation=45
)

plt.yticks(fontsize=12)
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig(f"img/heatmap_normalized_scores_{selected_subreddit}.png")
plt.show()