# Incremental_DBSCAN
An incremental DBSCAN approach in Python. 

This implementation uses 3 attributes (CPU, Memory, Disk) and creates clusters.

Every 5 seconds it receives monitoring data from a RabbitMQ Pub/Sub and either adds the new element to an already existing cluster, declares it an outlier or forms new clusters at runtime. 
