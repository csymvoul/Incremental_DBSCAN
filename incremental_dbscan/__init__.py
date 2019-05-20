import pandas as pd
import io
from sklearn.cluster import DBSCAN
from incremental_dbscan import cluster


def distance(element_1, element_2):
    """
    Calculates the distance between the element and the mean_core_element using the Euclidean distance
    :param element_1:  the current element that needs to be checked
    :param element_2:  the element to check the distance from
    :returns distance: the Euclidean distance between the element_1 and the element_2(float)
    """
    euclidean_distance = ((element_1['CPU'] - element_2['CPU']) ** 2 +
                          (element_1['Memory'] - element_2['Memory']) ** 2 +
                          (element_1['Disk'] - element_2['Disk']) ** 2) ** (1 / 2)
    return euclidean_distance.iloc[0].astype(float)


class IncrementalDBSCAN:

    def __init__(self, eps=5, min_samples=3):
        """
        Constructor the Incremental_DBSCAN class.
        :param eps:  the  maximum radius that an element should be in order to formulate a cluster
        :param min_samples:  the minimum samples required in order to formulate a cluster
        In order to identify the optimum eps and min_samples we need to  make a KNN
        """
        self.dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk'])
        self.labels = pd.DataFrame(columns=['Label'])
        self.final_dataset = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])
        self.mean_core_elements = pd.DataFrame(columns=['CPU', 'Memory', 'Disk', 'Label'])
        self.eps = eps
        self.min_samples = min_samples
        self.largest_cluster = -1

    def set_data(self, message):
        """
        After the connection with the RabbitMQ is complete a message is received.
        This function is used to gather the message from the consumer. It appends the newly arrived data to the
        dataset used for clustering.
        :param message:  The message consumed by the RabbitMQ. Should be a 3-column, comma-separated text.
        """
        # store the collected message to a temp dataframe
        temp = pd.read_csv(io.StringIO(message), sep=',', header=None)
        temp.columns = ['CPU', 'Memory', 'Disk']
        # append the temp to the dataset
        self.dataset = self.dataset.append(temp, ignore_index=True)

    def batch_dbscan(self):
        """
        The DBSCAN algorithm taken from the sklearn library. It is used to formulate the clusters the first time.
        Based on the outcomes of this algorithm the Incremental_DBSCAN algorithm
        """
        batch_dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(self.dataset)
        # Get the number of the clusters created
        n_clusters_ = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        self.add_labels_to_dataset(batch_dbscan.labels_)

        # Cast everything in the final_dataset as integer.
        # If this line is missing, it throws an error
        self.final_dataset = self.final_dataset.astype(int)
        # TODO this needs to be changed! The incremental_dbscan() function needs to be initiated by a third function.
        #  Once the batch_dbscan() is called and the first clusters are created then the
        #  incremental_dbscan() has to be called.
        self.incremental_dbscan_()
        # self.sort_dataset_based_on_labels()
        # self.find_mean_core_element()
        # response = self.calculate_distance()
        # # print(response)
        # if response is not None:
        #     self.check_min_samples_in_eps(min_dist_index=response)
        # self.largest_cluster = self.find_largest_cluster()

    def add_labels_to_dataset(self, labels):
        """
        This function adds the labels on the dataset after the batch DBSCAN is done
        :param labels: The labels param should be a list that  describes the cluster of each element.
        If an element is considered as an outlier it should be equal to -1
        """
        self.labels = pd.DataFrame(labels, columns=['Label'])
        self.final_dataset = pd.concat([self.dataset, self.labels], axis=1)

    def sort_dataset_based_on_labels(self):
        """
        This function sorts the dataset based on the Label of each cluster.
        """
        # print(self.final_dataset)
        self.final_dataset = self.final_dataset.sort_values(by=['Label'])
        # Cast everything in the final_dataset as integer.
        # If this line is missing, it throws an error
        self.final_dataset = self.final_dataset.astype(int)

    def find_mean_core_element(self):
        """
        This function calculates the average core elements of each cluster.
        Note: It does not calculate an average core element for the outliers.
        """
        # Exclude rows labeled as outliers
        self.mean_core_elements = self.final_dataset.loc[self.final_dataset['Label'] != -1]
        # Find the mean core elements of each cluster
        self.mean_core_elements = self.mean_core_elements \
            .groupby('Label')['CPU', 'Memory', 'Disk'].mean()
        # print(self.mean_core_elements)
        # response = self.calculate_distance()
        # # print(response)
        # if response is not None:
        #     self.check_min_samples_in_eps(min_dist_index=response)

    def calculate_distance(self):
        """
        This function identifies the closest mean_core_element to the incoming element
        that has not yet been added to a cluster or considered as outlier.
        The distance is calculated using the distance function as it is described above.

        :returns min_dist_index: if there is a cluster that is closest to the new entry element
        or None if there are no clusters yet.
        """
        min_dist = None
        min_dist_index = None

        # Check if there are elements in the core_elements dataframe.
        # In other words if there are clusters created by the DBSCAN algorithm
        if not self.mean_core_elements.empty:
            # Iterate over the mean_core_elements dataframe and find the minimum distance
            for index, current_mean_core_element in self.mean_core_elements.iterrows():
                tmp_dist = distance(element_1=self.final_dataset.tail(n=1),
                                    element_2=current_mean_core_element)
                if min_dist is None:
                    min_dist = tmp_dist
                    min_dist_index = index
                elif tmp_dist < min_dist:
                    min_dist = tmp_dist
                    min_dist_index = index
            print('Minimum distance is: ', min_dist, ' at cluster ', min_dist_index)
            return min_dist_index
        else:
            return None

    def check_min_samples_in_eps(self, min_dist_index):
        """
        This function checks whether there are at least min_samples in the given radius from the new
        entry element.
        If there are at least min_samples this element will be added to the cluster and the
        mean_core_element of the current cluster has to be re-calculated.
        If not, there are two options.
            1. Check if there are at least min_samples  outliers in the given radius in order to create a new
                cluster, or
            2.  Consider it as a new outlier

        :param min_dist_index: This is the parameter that contains information related to the closest
        mean_core_element to the current element.
        """
        # print("this is the  final element")
        # print(self.final_dataset.iloc[-1])
        print(self.mean_core_elements)
         
    def incremental_dbscan_(self):
        self.find_mean_core_element()
        response = self.calculate_distance()
        # print(response)
        if response is not None:
            self.check_min_samples_in_eps(min_dist_index=response)
        self.largest_cluster = self.find_largest_cluster()

    def find_largest_cluster(self):
        """
        This function identifies the largest of the clusters with respect to the number of the core elements.
        The largest cluster is the one with the most core elements in it.

        :returns: the number of the largest cluster. If -1 is returned, then there are no clusters created
        in the first place
        """
        cluster_size = self.final_dataset.groupby('Label')['Label'].count()
        # cluster_size = cluster_size['CPU'].value_counts()
        try:
            cluster_size = cluster_size.drop(labels=[-1])
        except ValueError:
            print("The label -1 does not exist")
        largest_cluster = -1
        if not cluster_size.empty:
            largest_cluster = cluster_size.idxmax()
            print('The cluster with the most elements in it is cluster no: ', cluster_size.idxmax())
            return largest_cluster
        else:
            print('There aren\'t any clusters formed yet')
            return largest_cluster

    # TODO 1:
    #  Find if there are at least min_samples  belonging
    #  in the cluster with the minimum distance in a radius of eps from the current element .
    #  If  TRUE, then consider this element as part of the cluster and recompute the mean_core_element.

    #  TODO 2:
    #   If FALSE, check whether there are at least min_samples outliers in the eps radius of the element,
    #   in order to create their own cluster.
    #       If TRUE, then create another cluster, change their Label and find their mean_core_element
    #       If FALSE, consider the element as outlier

    #  TODO 3:
    #   Delete old elements - Not sure if it is going to happen

    #     TODO 4:
    #      Find the biggest cluster's boundaries and publish them back the RabbitMQ
