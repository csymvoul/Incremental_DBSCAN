import pandas as pd
import io
from sklearn.cluster import DBSCAN
from math import sqrt


def distance(element, mean_core_elements):
    print(element['CPU'])


class Incremental_DBSCAN:

    def __init__(self, eps=5, min_samples=3):
        self.dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk'])
        self.labels = pd.DataFrame(columns=['Label'])
        self.final_dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])
        self.mean_core_elements = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])
        self.eps = eps
        self.min_samples = min_samples

    def set_data(self, message):
        # store the collected message to a temp dataframe
        temp = pd.read_csv(io.StringIO(message), sep=',', header=None)
        temp.columns = ['CPU', 'Memory', 'Disk']
        # append the temp to the dataset
        self.dataset = self.dataset.append(temp, ignore_index=True)

    def batch_dbscan(self):
        batch_dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(self.dataset)
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
        print(self.final_dataset)
        self.final_dataset = self.final_dataset.sort_values(by=['Label'])
        # Cast everything in the final_dataset as integer. If this line is missing, it throws an error
        self.final_dataset = self.final_dataset.astype(int)

    def find_mean_core_element(self):
        # Exclude rows labeled as outliers
        self.mean_core_elements = self.final_dataset.loc[self.final_dataset['Label'] != -1]
        # Find the mean core elements of each cluster
        self.mean_core_elements = self.mean_core_elements.groupby('Label')['CPU', 'Memory', 'Disk'].mean()
        print(self.mean_core_elements)
        response = self.calculate_distance()
        print(response)

    def calculate_distance(self):
        print(self.final_dataset.tail(n=1))
        if not self.mean_core_elements.empty:
            distance(element=self.final_dataset.tail(n=1), mean_core_elements=self.mean_core_elements)
            return self.mean_core_elements
        else:
            return 'Empty dataframe, no clusters found'
