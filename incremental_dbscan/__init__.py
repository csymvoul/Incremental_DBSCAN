import pandas as pd
from sklearn.cluster import DBSCAN


def initiate_dbscan(first_datum):
    dataset = pd.read_csv(first_datum, sep=',')
    dbscan = DBSCAN(eps=15, min_samples=3).fit(dataset)
    labels = dbscan.labels_
    print(labels)

def incremental_dbscan(datum):