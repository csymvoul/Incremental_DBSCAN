import pandas as pd
import io
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
        print(batch_dbscan.labels_)
    # def initiate_dbscan(first_datum):
        # def incremental_dbscan(datum):
