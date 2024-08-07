import pandas as pd
import numpy as np


### To run the cleaning function, import it and then run cleaning_function(df). This will produce two variables.
### The cleaned df and a features summary list.

def feature_list(df):
    '''
    Creates a feature list based on the game_data dataframe.
    
    Parameters:
    df (DataFrame): The game_data dataframe object.
    
    Returns:
    game_feature_summary (DataFrame): A dataframe object with the features summarized.
    
    '''

    attributes_vals = df.columns.tolist()
    attributes = {'attributes':attributes_vals}
    
    x = 0
    type_list = []

    while x <= len(attributes_vals):
        try:
            cur_col = attributes_vals[x]
            if df[cur_col].nunique() > 2:
                if df[cur_col].dtypes == 'int64':
                    type_list.append('numerical')
                elif df[cur_col].dtypes == 'float64':
                    type_list.append('numerical')
                else:
                    type_list.append('categorical')
                x += 1
            else:
                type_list.append('categorical')
                x += 1
        except IndexError as excpt:
            break
            
    types = {'type': type_list}
    
    demographic_level = {'demographic_level': ['personal', 'personal', 'personal', 'game', 'game', 'game', 'game', 'stat', 'stat', 'stat', 'stat', 'stat']}
    priority = {'priority': [1, 1, 1, 1, 2, 3, 3, 2, 2, 3, 3, 2]}

    a_df = pd.DataFrame(data=attributes, index = range(12))
    t_df = pd.DataFrame(data=types, index = range(12))
    i_df = pd.DataFrame(data=demographic_level, index = range(12))
    p_df = pd.DataFrame(data=priority, index = range(12))
    
    game_feature_summary = a_df.join((t_df, i_df, p_df), how='outer')
    
    return game_feature_summary
    

def cleaning_function(df):
    '''
    This is the final designed cleaning function for the dataset. 
    This function completes preprocessing steps before analysis.
    
    Parameters:
    df (DataFrame): Dataframe object to clean.
    
    Returns:
    df (DataFrame): Cleaned dataframe object.
    
    '''
    
    df = df.drop(['PlayerID'], axis=1)
    
    game_feature_summary = feature_list(df)
    
    num_features = game_feature_summary[game_feature_summary['type'] == 'numerical']['attributes']
    cat_features = game_feature_summary[game_feature_summary['type'] == 'categorical']['attributes']
    
    cat_features = cat_features.drop(index=11)

    # EngagementLevel has three different values, thus we can substitute it with mapping.
    e_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    df['EngagementLevel'] = df['EngagementLevel'].map(e_mapping)

    for col in cat_features:
        vc = df[col].value_counts()
        mapping = {value: idx for idx, value in enumerate(vc.index)}
        df[col] = df[col].map(mapping)
    
    return df, game_feature_summary
