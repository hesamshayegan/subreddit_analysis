from data_preprocessor import dfs
import numpy as np  
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


max_scores = {}
for i, df in enumerate(dfs):

    max_score = df['score'].max()
    subreddit_title = df['subreddit'].iloc[0]
    
    max_scores[subreddit_title] = max_score

def calculate_max_scores_upvotes(dfs):
    max_scores_upvotes = []
    for i, df in enumerate(dfs):

        max_row = df.loc[df['score'].idxmax()]
        
        subreddit_title = max_row['subreddit']
        max_score = max_row['score']
        max_upvote = max_row['upvote_ratio']
        max_scores_upvotes.append([subreddit_title, max_score, max_upvote])
    return max_scores_upvotes

max_scores_upvotes = calculate_max_scores_upvotes(dfs)

extracted_max_scores = [row[1] for row in max_scores_upvotes]
mean = np.mean(extracted_max_scores)
stdev = np.std(extracted_max_scores)

z_score_upvotes = []
for subreddit_list in max_scores_upvotes:

    z_score = (subreddit_list[1] - mean) / stdev
    z_score_upvotes.append([subreddit_list[0], z_score, subreddit_list[2]])

df_z_score_upvotes = pd.DataFrame(z_score_upvotes,
                                  columns=['category', 'z_score', 'upvote_ratio'])

# Add a new column for categorizing the points
df_z_score_upvotes['highlight'] = df_z_score_upvotes.apply(
    lambda row: 'breakout posts(z-score>2 & upvote>0.95)' if row['z_score'] > 2 and row['upvote_ratio'] > 0.95
                else 'high upvotes posts(upvote>0.95)' if row['upvote_ratio'] > 0.95 
                else 'Other',
    axis=1
)

# Create a column for dot size based on conditions
df_z_score_upvotes['dot_size'] = df_z_score_upvotes.apply(
    lambda row: 300 if row['z_score'] > 2 and row['upvote_ratio'] > 0.95 
                else 200 if row['upvote_ratio'] > 0.95 
                else 100,
    axis=1
)

palette = {
    'breakout posts(z-score>2 & upvote>0.95)': '#ff4d4d',
    'high upvotes posts(upvote>0.95)': '#ff9999',
    'Other': '#b3b3b3'
}

plt.figure(figsize=(10, 6))
scatter = sns.scatterplot(
    x='z_score',
    y='upvote_ratio',
    hue='highlight',
    size='dot_size',
    sizes=(100,300),
    palette=palette,
    legend='full',
    data=df_z_score_upvotes
)

for i, row in df_z_score_upvotes.iterrows():
    if row['highlight'] == 'breakout posts(z-score>2 & upvote>0.95)':
        plt.text(
            row['z_score'] - 0.05,
            row['upvote_ratio'] - 0.01,
            row['category'].upper(),
            fontdict={'family': 'monospace', 'size': 8},
            color='black',
            rotation=0,
            ha='right'
        )

plt.grid(ls='--')

plt.title('Breakout Post Identification Based on Z-Scores and Upvotes', 
          fontdict={'family': 'monospace',
                    'size': 12,
                    'weight':'bold',
                    'style': 'italic'})
plt.xlabel('Z-Score=(max_score - mean)/stdev', fontdict={'family': 'monospace', 'size': 12})
plt.ylabel('Upvote Ratio', fontdict={'family': 'monospace', 'size': 12})

# Remove the size legend while keeping the hue legend
handles, labels = scatter.get_legend_handles_labels()
new_labels = ['breakout posts(z-score>2 & upvote>0.95)', 'high upvotes posts(upvote>0.95)', 'Other']
new_handles = [handles[labels.index(label)] for label in new_labels]

plt.legend(new_handles, new_labels, loc='lower right',
           prop={'family': 'monospace', 'size': 10})


plt.savefig('img/z_score_analysis_plot.png')