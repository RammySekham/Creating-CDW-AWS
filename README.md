#### Introduction
##### As the organisation 's user base grows, there is a requirement to scale the resources to cater new users' needs. Under organisation's resources, data is a crucial resource to scale on basis of avaliablity, consistency and partition tolerance. The industry cloud players i.e. AWS, Azure, Cloudera and GCP offers similiar and distinguishable options to choose from, for the data migration to the cloud.The process of hosting datawarehouse on cloud is fast, less of choas, need almost no infrastructure/hardware and requires less resources as compared to on-premises solution.

#### Why Redshift?
##### For this project we have selected 'AWS-Redshift' for migrating data to cloud. AWS RedShift facilitates MPP Architecture(Massive Parallel processing on multiple nodes, offers query optimization, horizontal scaling(add as many nodes as needed), massive storage, with VPC security and SQL based.

#### Challenges of Redshift
##### 'Primary Key' 'Foreign Key' 'UNIQUE' constraints of SQL DDL won't work in Redshift. We need to code extra step in 'INSERT statements' while loading data to redshift tables, so to make sure data entered is unique/not duplicated. It requires an additional effort to build logic in SQL queries.
#####  Distkey and sortkey should be conisdered carefully. Distkey helps in data distribution on partitions for query optimization specifically in case of SQL JOINS. Data is stored on basis of sort key on disk. redshift query optimizer uses sort key in  query optimization




