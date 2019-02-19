import pandas as pd
import io
from sklearn.cluster import DBSCAN
from math import sqrt
from math import pow


# Returns the Euclidean of a mean core element and the current element
def distance(element, mean_core_element):
    distance = ((element['CPU'] - mean_core_element['CPU'])**2 +
                    (element['Memory'] - mean_core_element['Memory'])**2 +
                    (element['Disk'] - mean_core_element['Disk'])**2)**(1/2)
    return distance.iloc[0].astype(float)


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
        self.add_labels_to_dataset(batch_dbscan.labels_)

        # Cast everything in the final_dataset as integer.
        # If this line is missing, it throws an error
        self.final_dataset = self.final_dataset.astype(int)
        # self.sort_dataset_based_on_labels()
        self.find_mean_core_element()

    def add_labels_to_dataset(self, labels):
        self.labels = pd.DataFrame(labels, columns=['Label'])
        self.final_dataset = pd.concat([self.dataset, self.labels], axis=1)

    def sort_dataset_based_on_labels(self):
        # print(self.final_dataset)
        self.final_dataset = self.final_dataset.sort_values(by=['Label'])
        # Cast everything in the final_dataset as integer.
        # If this line is missing, it throws an error
        self.final_dataset = self.final_dataset.astype(int)

    def find_mean_core_element(self):
        # Exclude rows labeled as outliers
        self.mean_core_elements = self.final_dataset.loc[self.final_dataset['Label'] != -1]
        # Find the mean core elements of each cluster
        self.mean_core_elements = self.mean_core_elements \
            .groupby('Label')['CPU', 'Memory', 'Disk'].mean()
        # print(self.mean_core_elements)
        response = self.calculate_distance()

    def calculate_distance(self):
        min_dist = None
        min_dist_index = None
        # Check if there are elements in the core_elements dataframe.
        # In other words if there are clusters created by the DBSCAN algorithm
        if not self.mean_core_elements.empty:
            # Iterate over the mean_core_elements dataframe and find the minimum distance
            for index, current_mean_core_element in self.mean_core_elements.iterrows():
                tmp_dist = distance(element=self.final_dataset.tail(n=1),
                                    mean_core_element=current_mean_core_element)
                if min_dist is None:
                    min_dist = tmp_dist
                    min_dist_index = index
                elif tmp_dist < min_dist:
                    min_dist = tmp_dist
                    min_dist_index = index
            print('Minimum distance is: ', min_dist, ' at cluster ', min_dist_index)
            return min_dist_index
        else:
            return 'Empty dataframe, no clusters found'
