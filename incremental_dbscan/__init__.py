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

    def add_labels_to_dataset(self, labels):
        self.labels = pd.DataFrame(labels, columns=['Labels'])
        # final_ds =
        # final_ds =
        self.final_dataset = pd.concat([self.dataset, self.labels], axis=1)
        print('printing final_dataset')
        print(self.final_dataset)

    def find_mean_element(self):
        # TODO find them mean element of each dataset in order to
        # TODO compare the distances on each dataset
        return self.dataset
