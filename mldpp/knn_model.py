import numpy as np
feature_importance_df = None

def set_feature_importance_df(df):
    global feature_importance_df
    feature_importance_df = df

def weighted_distance(x, y):
    global feature_importance_df
    weights = feature_importance_df['Importance'].values
    return np.sqrt(np.sum((x - y)**2 * weights))

# def weighted_distance(x, y):
#     global feature_importance_df
#     weights = feature_importance_df['Importance'].values
#     return np.sqrt(np.sum((x - y)**2 * 1))