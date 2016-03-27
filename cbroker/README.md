#CSB Framework (cbroker)

In order to the use CSB Framework the following steps have to be performed:
##Download the source code of the CSB framework from the following repository:
https://github.com/sonnenfeldt/peyresourde/tree/master/cbroker

##Installation of Python:
1. Install Python 2.7.x
2. Install the SQLAlchemy, MySQL-python, NumberJack and python-dockercloud libraries

`pip install sqlalchemy` 

`pip install mysql-python`

`pip install numberjack`

`pip install python-dockercloud` 

## Installation and configuration of MySQL:
1. Install MySQL or deploy a MySQL container
2. Install the MySQL Workbench and connect to the MySQL installation
3. Create a schema `cbroker`
4. Use the Data Import wizard to import the self-contained file `cbrocker.sql` from package `cbroker.db.sql` which contains the database structure and pre-populated tables.
5. Configure the file `cbrokerdb.properties` in package `cbroker.cb`: 

`[MySQL]` 

`database.user=<user name>`

`database.password=<password>` 

`database.hostname=<hostname>` 

`database.port=<port>` 

## Set up of the Docker Cloud API access:
1. Please note that with the use of Docker Cloud and the associated cloud providers costs occur which the user will have to pay on its own expense.
2. Login to Docker Cloud and configure the cloud provider access, please note that this step requires to obtain and configure own accounts for AWS, DigitalOcean, IBM SoftLayer, Microsoft Azure and Packet.  
3. Create an Docker Cloud API key and use it in the next step.
4. Configure the file `docker.properties` in package `cbroker.cb`:

`[Credentials]`

`dockercloud.user=<user name>`

`dockercloud.apikey=<api key>` 

## Run the code: 
The class CBroker defines the basic methods for deploying containers and terminating them, and can be used as entry point for working with the framework.

