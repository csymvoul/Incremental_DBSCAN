import pandas as pd
import io
import numpy as np
# from sklearn.cluster import DBSCAN
from sklearn.cluster import DBSCAN


class Incremental_DBSCAN:

    def __init__(self):
        self.dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk'])
        self.labels = pd.DataFrame(columns=['Label'])
        self.final_dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])
        self.mean_core_elements = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])

    def set_data(self, message):
        # store the collected message to a temp dataframe
        temp = pd.read_csv(io.StringIO(message), sep=',', header=None)
        temp.columns = ['CPU', 'Memory', 'Disk']
        # append the temp to the dataset
        self.dataset = self.dataset.append(temp, ignore_index=True)

    def get_headers(self):
        return list(self.dataset)

    def batch_dbscan(self):
        batch_dbscan = DBSCAN(eps=3, min_samples=2).fit(self.dataset)
        # Get the number of the clusters created
        n_clusters_ = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        # TODO  Still not fully working -- Needs to be  checked
        self.add_labels_to_dataset(batch_dbscan.labels_)
        self.sort_dataset_based_on_labels()
        self.find_mean_core_element()

    def add_labels_to_dataset(self, labels):
        self.labels = pd.DataFrame(labels, columns=['Label'])
        self.final_dataset = pd.concat([self.dataset, self.labels], axis=1)

    def sort_dataset_based_on_labels(self):
        self.final_dataset = self.final_dataset.sort_values(by=['Label'])
        self.final_dataset = self.final_dataset.astype(int)
        print(self.final_dataset)

    def find_mean_core_element(self):
        self.mean_core_elements = self.final_dataset.groupby('Label')['CPU', 'Memory', 'Disk'].mean()
        print(self.mean_core_elements)

