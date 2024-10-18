import seaborn as sns
import pandas as pd
from kneed import KneeLocator
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsRegressor
import pickle
from knn_model import *
from var import *


class Predictor:
    def __init__(self, model_name):
        self.model_path = f"{MLDPP_DIR}/models/{model_name}"
        self.__prepare_model()

    
    def find_optimal_config(self, new_point,  target = 'latency'):
        # Find the K nearest neighbors of the new point
        new_datapoint = self.__process_new_point(new_point, self.top_features)
        distances, indices = self.model.kneighbors(new_datapoint)
        # print(distances, indices)
        # Get the neighbors in the original data
        neighbors = self.data.iloc[indices.flatten()]
        # Find the index of the neighbor based on target
        if target == 'latency':
            min_latency_index = neighbors['llc_read_miss_latency(ns)'].idxmin()
        elif target == 'ipc':
            min_latency_index = neighbors['ipc'].idxmax()
        # Get the data of the neighbor based on target
        min_latency_neighbor = self.data.loc[min_latency_index]
        return min_latency_neighbor, {}

    def __prepare_model(self):
        with open(self.model_path, 'rb') as f:
            data_loaded = pickle.load(f)

        self.model = data_loaded['model']
        self.data = data_loaded['data']
        feature_importance_df = data_loaded['feature_importance_df']
        set_feature_importance_df(feature_importance_df)
        self.top_features = feature_importance_df['Feature'].values

        # # def weighted_distance(x, y):
        # #     weights = feature_importance_df['Importance'].head(n_features).values
        # #     return np.sqrt(np.sum((x - y)**2 * weights))
        # self.model.metric = weighted_distance

    def __process_new_point(self, new_point, top_features):
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