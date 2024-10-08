from data_preprocessor import dfs
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import textwrap

movies = []
pics = []
memes = []
for i, df in enumerate(dfs):

    category = df['subreddit'].iloc[1]
    if category == 'movies':
        movies_sorted = df.sort_values(by='score', ascending=False)
        top_5_movies = movies_sorted.head(5)

        for index, row in top_5_movies.iterrows():
            movies.append([row['subreddit'], row['created_utc'], row['score'], row['title'], row['post_type']])

    elif category == 'pics':
        pics_sorted = df.sort_values(by='score', ascending=False)
        top_5_pics = pics_sorted.head(5)

        for index, row in top_5_pics.iterrows():
            pics.append([row['subreddit'], row['created_utc'], row['score'], row['title'], row['post_type']])
    
    elif category == 'memes':
        memes_sorted = df.sort_values(by='score', ascending=False)
        top_5_memes = memes_sorted.head(5)

        for index, row in top_5_memes.iterrows():
            memes.append([row['subreddit'], row['created_utc'], row['score'], row['title'], row['post_type']])      
    
top_categories = movies + pics + memes

df_top_categories = pd.DataFrame(data= top_categories,
                                 columns=['category', 'timestamp', 'score', 'title', 'post_type'])

df_sorted_by_year = df_top_categories.sort_values(by=['timestamp'], ascending=False)
df_sorted_by_year['date_formatted'] = df_sorted_by_year['timestamp'].dt.strftime('%d %b, %Y')

# print(df_sorted_by_year.head())

sns.set_theme(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(
    nrows=1, ncols=2, figsize=(16, 10), 
    gridspec_kw={'width_ratios': [2, 1]}
)

custom_palette = sns.color_palette(["#4d0026", "#ff0080", "#ff99cc"])

df_sorted_by_year['Categories'] = df_sorted_by_year.apply(
    lambda row: 'MOVIES' if row['category'] == 'movies'
                else 'MEMES' if row['category'] == 'memes'
                else 'PICS',
    axis=1
)

sns.barplot(
    x='score', 
    y='date_formatted', 
    data=df_sorted_by_year,
    palette = custom_palette,
    hue="Categories",
    dodge=False,
    ax=ax1,
    width=0.5 
    )

ax1.set_xlabel("Score", fontdict={'family': 'monospace', 'size': 14})
ax1.set_ylabel("Time", fontdict={'family': 'monospace', 'size': 14})
ax1.legend(loc='upper right', bbox_to_anchor=(1, 1),
           facecolor='white', title="Categories")
ax1.set_title('Top Performers: High-Scoring Posts from Breakout Categories',
              fontdict={'family': 'monospace',
                        'size': 12,
                        'weight':'bold',
                        'style': 'italic'})

max_values = df_sorted_by_year.groupby('category')['score'].idxmax()

for idx in max_values: 
    score = df_sorted_by_year.loc[idx, 'score']
    ax1.axvline(x = score, color = 'blue', linestyle= 'dashed')

graph_text = []
for idx in max_values:
    category = df_sorted_by_year.loc[idx, 'category']
    title = df_sorted_by_year.loc[idx, 'title']
    post_type = df_sorted_by_year.loc[idx, 'post_type']
    graph_text.append([category, title, post_type])

full_text = ""
max_width = 40

for category, title, post_type in graph_text:

    text = f"Category: {category.upper()}\nPost Type: {post_type}\nPost Title: {title}"
    
    wrapped_title1 = "\n".join(textwrap.wrap(f"Post Type: {post_type}", max_width))
    wrapped_title2 = "\n".join(textwrap.wrap(f"Post Title: {title}", max_width))
    
    full_text += f"Category: {category.upper()}\n{wrapped_title1}\n{wrapped_title2}\n\n"

ax2.text(
    0.5, 0.5, full_text, style='italic', ha='center', va='center',
    bbox={'facecolor': 'white', 'edgecolor': 'blue', 'boxstyle': 'round,pad=1'},
    transform=ax2.transAxes
)
 
ax2.axis('off')
plt.tight_layout()
plt.savefig('img/content_analyis_plot.png')