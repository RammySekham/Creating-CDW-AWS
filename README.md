#### Introduction
##### As the organisation 's user base grows, there is a requirement to scale the resources to cater new users' needs. Under organisation's resources, data is a crucial resource to scale on basis of avaliablity, consistency and partition tolerance. The industry cloud players i.e. AWS, Azure, Cloudera and GCP offers a similiar and distinguishable options to choose from, for data migration to cloud.The process of hosting datawarehouse on cloud is fast, less of choas, need almost no infrastructure/hardware and requires less resources as compared to on-premises solution.

#### Why Redshift?
##### For this project we have selected 'AWS-Redshift' for migrating data to cloud.AWS RedShift facilitates MPP Architecture(Massive Parrllel processing on multiple nodes,offers query optimization, horizontal scaling(add as many nodes as needed), massive storage, with VPC security and SQL based.

#### Challenges of Redshift
##### 'Primary Key' 'Foreign Key' 'UNIQUE' CONSTRAINTS WON'T WORK. We need to code extra step in 'INSERT statements' while loading data to tables to make sure data entered is unique. Need extra effort to build logic.
##### Careful consideration of distkey and sortkey: helps in data distribution on partitions for query optimization




