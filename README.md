### Introduction
##### As the organisation's user base grows, there is a requirement to scale the resources to cater new users' needs. Under organisation's resources, data is a crucial resource to scale on the basis of avaliablity, consistency and partition tolerance. The industry cloud players i.e. AWS, Azure, Cloudera and GCP offer similiar and distinguishable options to choose from, for the data migration to the cloud.The process of hosting datawarehouse on cloud is fast, less of choas, need almost no infrastructure/hardware and requires less resources as compared to on-premises solution.

#### Why Redshift?
##### For this project we have selected 'AWS-Redshift' for migrating data to cloud. AWS RedShift facilitates MPP Architecture(Massive Parallel processing on multiple nodes, offers query optimization, horizontal scaling(add as many nodes as needed), massive storage, with VPC security and SQL based.

#### Challenges of Redshift
##### 'Primary Key' 'Foreign Key' 'UNIQUE' constraints of SQL DDL won't work in Redshift. We need to code extra step in 'INSERT statements' while loading data to redshift tables, so to make sure data entered is unique/not duplicated. It requires an additional effort to build logic in SQL queries.
#####  Distkey and sortkey should be conisdered carefully. Dist keys helps in data distribution on partitions for query optimization specifically in case of SQL JOINS. Data is stored on basis of sort key on disk. Redshift query optimizer uses sort keys in query optimization.
#
### Project:
##### For a streaming music app company sparkify, an ETL pipeline is built, that extracts raw data in the form of json logs and metadata from S3 bucket, staged in Redshift, and transformed it into a set of dimensional tables(database) for the analytics team.
#
### Process:
##### 1. Understanding Data and Creating the Schema 
######     Raw Data : JSON logs on user activity on the app and JSON metadata on the songs in the app hosted on S3 Bucket
######     Star Scehma : A Fact table of Songs-Played and Dimenisons Table: Users, Songs, Artists and time

##### 2. After understanding the data and schema, project is implemented as follows:
 ![](https://github.com/RammySekham/ETL-Pipeline--AWS-Redshift/blob/main/images/project.png)

### How to run this code
##### 1. Clone the repository or download the files
##### 2. Install requirements from `requirements.txt`
##### 3. Configure `dwh_create.cfg` with Amazon Access KEY AND SECRET( with previliegs to create redshift cluster i.e. admin access)
##### 4. Run `create_cluster.ipynb` to create redshift cluster and Retrieve Cluster Endpoint(Host) and ARN.
##### 5. Configfure `dwh.cfg` to include Cluster Host and ARN
##### 6. Run in terminal/bash
            python create_tables.py
            python etl.py
##### 7. Go to  AWS Redshift Console to query data or perform queries as shown. 
###### Query Snapshots in Redshift Console
![](https://github.com/RammySekham/ETL-Pipeline--AWS-Redshift/blob/main/images/Redshift1.PNG)
##### 8. If project is run for experimentation and learning. We can delete the cluster and remove the roles and policies by running `delete_cluster.ipynb`
