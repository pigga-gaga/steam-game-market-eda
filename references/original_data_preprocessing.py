# -*- coding: utf-8 -*-
"""
Created on Sat Oct 11 22:14:47 2025

@author: 24104
"""
import json
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt

# Import dataset and convert to dataframe format
with open('games.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
df = pd.DataFrame.from_dict(json_data, orient='index').reset_index()

# Rename index column to AppID
df = df.rename(columns={'index': 'AppID'})

# Remove unnecessary attributes
df = df.drop(columns=['detailed_description', 'about_the_game',
                      'short_description','reviews','header_image',
                      'website','support_url','support_email','packages',
                      'metacritic_url','notes','screenshots','movies'
                      ,'discount'])

# Filter data for games released in the past year
# Convert date column to datetime type
df1 = df
df['release_date'] = pd.to_datetime(df['release_date'], format='mixed')

# Remove data before 2020-05-30
df_filtered = df[df['release_date'] >= '2020-05-30']

# Remove attributes with high missing values
df_filtered = df_filtered.drop(columns=['tags','full_audio_languages'])

# Check for null values
df_filtered.isnull().sum()

# Count the number and proportion of empty strings in each column of the DataFrame
def count_empty_strings(df):
    empty_stats = {}
    
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            empty_count = df[col].apply(lambda x: x == '').sum()
        else:
            empty_count = 0 
            
        total_rows = len(df)
        empty_percent = (empty_count / total_rows) * 100 if total_rows > 0 else 0
        
        empty_stats[col] = {
            'type': df[col].dtype,
            'empty_string_count': empty_count,
            'empty_string_ratio(%)': round(empty_percent, 2)
        }
    
    result_df = pd.DataFrame.from_dict(empty_stats, orient='index')
    return result_df

print(count_empty_strings(df_filtered))

# Found that score_rank column has 100% empty strings, so remove it
df_filtered = df_filtered.drop(columns='score_rank')

#Count the number of each category for categorical variables in the DataFrame
def count_categorical_values(df):

    for col in df.columns:

        if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
            print(f"column name: {col}")
            print("-" * 30)

            count_result = df[col].value_counts(dropna=False)  
            print(count_result)
            print("\n" + "=" * 40 + "\n")
    return
     
count_categorical_values(df_filtered)


#Filter rows where estimated_owners is '0 - 0', randomly select 10 names and output them.
def get_random_names(df):

    filtered_df = df[df['estimated_owners'] == '0 - 0']
    
    if filtered_df.empty:
        print("No rows where estimated_owners is '0 - 0' were found.")
        return []
    
    names = filtered_df['name']
    
    sample_size = min(10, len(names))
    random_names = names.sample(n=sample_size, random_state=np.random.RandomState())  
    
    return random_names.tolist()

random_names = get_random_names(df_filtered)
print(random_names)

#Delete rows where estimated_owners is '0 - 0'
df_filtered = df_filtered[df_filtered['estimated_owners'] != '0 - 0']
count_categorical_values(df_filtered)

# Plot individual boxplots for each numeric column in the DataFrame
def plot_individual_boxplots(df, figsize=(8, 5), suptitle="Boxplots of Numeric Columns"):
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) == 0:
        print("There are no numeric columns in the DataFrame, cannot plot boxplots")
        return
    
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False
    
    n_cols = 3
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0]*n_cols, figsize[1]*n_rows))
    fig.suptitle(suptitle, fontsize=16, y=1.02)  
    
    axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
    
    for i, col in enumerate(numeric_cols):
        
        df.boxplot(column=col, ax=axes[i], grid=False)
        
        axes[i].set_title(f'{col}', fontsize=12)
        axes[i].set_ylabel('Value')
        
        axes[i].spines['top'].set_visible(False)
        axes[i].spines['right'].set_visible(False)
    
    for i in range(len(numeric_cols), len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()
    return

def plot_individual_boxplots_2(df, figsize=(8, 5), suptitle_prefix="Boxplots of Numeric Columns"):

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) == 0:
        print("There are no numeric columns in the DataFrame, cannot plot boxplots")
        return
    
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False
    
    for col in numeric_cols:
        
        fig, ax = plt.subplots(figsize=figsize)
        
        df.boxplot(column=col, ax=ax, grid=False)
        
        ax.set_title(f'{suptitle_prefix}{col}', fontsize=16)
        ax.set_ylabel('Value', fontsize=12)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.show()
    
    return

plot_individual_boxplots(df_filtered, figsize=(8, 5), suptitle="Boxplots of Numeric Columns")
plot_individual_boxplots_2(df_filtered, figsize=(8, 5), suptitle_prefix="Boxplots of Numeric Columns")

df_filtered = df_filtered.drop(columns='user_score')
df_filtered.to_csv('steam_2.csv', index=False,encoding='utf-8-sig')

# Split columns containing multiple categories
def expand_list_column(df, column_name, prefix):

    if column_name not in df.columns:
        raise ValueError(f"Column does not exist in DataFrame: {column_name}")
    
    list_series = df[column_name].apply(lambda x: x if isinstance(x, list) else [])
    
    all_categories = set()
    for item_list in list_series:
        all_categories.update(item_list)
    all_categories = sorted(list(all_categories)) 
    
    one_hot_data = {}
    for category in all_categories:
        new_col_name = f"{prefix}{category}"
        one_hot_data[new_col_name] = list_series.apply(lambda x: 1 if category in x else 0)
    
    one_hot_df = pd.DataFrame(one_hot_data)
    
    result_df = pd.concat([df, one_hot_df], axis=1)
    
    return result_df

df_filtered = expand_list_column(df_filtered, 'supported_languages','languages_')
df_filtered = expand_list_column(df_filtered, 'categories','categories_')
df_filtered = expand_list_column(df_filtered, 'genres','genres_')

# Save the result as a csv file
df_filtered.to_csv('steam_split.csv', index=False, encoding='utf-8-sig')