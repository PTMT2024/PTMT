import seaborn as sns
import pandas as pd
from kneed import KneeLocator
import numpy as np
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsRegressor
import pickle
from knn_model import *
from var import *

class PredictorV2:
    def __init__(self, model_name, check_outliers=False):
        self.model_path = f"{MLDPP_DIR}/models/{model_name}"
        self.check_outliers = check_outliers
        self.__prepare_model()

    
    def find_optimal_config(self, new_point,  target = 'latency'):
        # Find the K nearest neighbors of the new point
        new_datapoint = self.__process_new_point(new_point)
        cluster = self.kmeans.predict(new_datapoint)[0]
        knn = self.knn_models[cluster]
        is_outlier = False
        if self.check_outliers:
            is_outlier = self.__is_outlier(cluster, new_datapoint.iloc[0])

        distances, indices = knn.kneighbors(new_datapoint)
        # print(distances, indices)
        # Get the neighbors in the original data
        neighbors = self.knn_data[cluster].iloc[indices.flatten()]
        # Find the index of the neighbor based on target
        if target == 'latency':
            target_neighbor = neighbors.sort_values(by='llc_read_miss_latency(ns)', ascending=True).iloc[0]
        elif target == 'ipc':
            target_neighbor =  neighbors.sort_values(by='ipc', ascending=False).iloc[0]
        # Get the data of the neighbor based on target
        # print("target_neighbor: ", target_neighbor)

        return target_neighbor, {'is_outlier': is_outlier}

    def __is_outlier(self, cluster_label, data_point):
        """Determine if a new data point is an outlier."""
        centroid = self.kmeans.cluster_centers_[cluster_label]
        distance = euclidean(data_point, centroid)
        return distance > self.cluster_thresholds[cluster_label]

    def __prepare_model(self):
        with open(self.model_path, 'rb') as f:
            data_loaded = pickle.load(f)

        self.kmeans = data_loaded['kmeans']
        self.knn_models = data_loaded['knn_models']
        self.knn_data = data_loaded['knn_data']
        feature_importance_df = data_loaded['feature_importance_df']
        set_feature_importance_df(feature_importance_df)
        self.top_features = feature_importance_df['Feature'].values
        self.cluster_thresholds = data_loaded.get('cluster_thresholds')

    def __process_new_point(self, new_point):
        top_features = self.top_features
        data = pd.DataFrame(new_point, index=[0])
        data['ipc'] = data['ipc'].fillna(0)

        data["pmm_ratio_of_write"] = data["written_to_pmm(MB/s)"] / (
            data["written_to_pmm(MB/s)"] + data["written_to_dram(MB/s)"]
        )
        data["pmm_ratio_of_read"] = data["read_from_pmm(MB/s)"] / (
            data["read_from_pmm(MB/s)"] + data["read_from_dram(MB/s)"]
        )
        data["total_write_traffic"] = (
            data["written_to_pmm(MB/s)"] + data["written_to_dram(MB/s)"]
        )
        data["total_read_traffic"] = (
            data["read_from_pmm(MB/s)"] + data["read_from_dram(MB/s)"]
        )
        data["total_traffic"] = data["total_write_traffic"] + data["total_read_traffic"]
        data["write_traffic_ratio"] = (
            data["total_write_traffic"] / data["total_traffic"]
        )
        data["read_traffic_ratio"] = data["total_read_traffic"] / data["total_traffic"]
        data["total_pmm_traffic"] = data["written_to_pmm(MB/s)"] + data["read_from_pmm(MB/s)"]
        data["total_dram_traffic"] = data["written_to_dram(MB/s)"] + data["read_from_dram(MB/s)"]   
        data["total_pmm_trafic_norm"] = data["total_pmm_traffic"] / (2666 * 8)
        data["total_dram_trafic_norm"] = data["total_dram_traffic"] / (2933 * 8)

        for column in data.columns:
            data[f'prev_{column}'] = data[column]
        
        # print(data[top_features])
        return data[top_features]