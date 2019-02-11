import pandas as pd
import io
import numpy as np
# from sklearn.cluster import DBSCAN
from sklearn.cluster import DBSCAN


class Incremental_DBSCAN:

    def __init__(self):
        self.dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk'])

    def set_data(self, message):
        # store the collected message to a temp dataframe
        temp = pd.read_csv(io.StringIO(message), sep=',', header=None)
        temp.columns = ['CPU', 'Memory', 'Disk']

        # append the temp to the dataset
        self.dataset = self.dataset.append(temp)

    def get_headers(self):
        return list(self.dataset)

    def batch_dbscan(self):
        batch_dbscan = DBSCAN(eps=3, min_samples=2).fit(self.dataset)

        # Store the labels in a ndarray
        labels = batch_dbscan.labels_

        # Get the number of the clusters created
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        print('Number of clusters: ', n_clusters_)

        # TODO  Still not fully working -- Needs to be  checked
        self.add_labels_to_dataset(labels=labels)

        # Store the label of each element on the dataset
        # print(type(labels))

    def add_labels_to_dataset(self, labels):
        labels_df = pd.DataFrame(labels, columns=['Labels'])

        self.dataset.index = labels_df.index
        self.dataset['Labels'] = labels_df['Labels']
        # print(len(labels_df), type(labels_df))
        # print(len(self.dataset), type(self.dataset))

    def find_mean_element(self):
        # TODO find them mean element of each dataset in order to
        # TODO compare the distances on each dataset
        return self.dataset
