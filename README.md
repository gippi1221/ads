# Ads app

The sample solution is designed to track and analyze key metrics.
It provides the ability to gather new events, as well as analytics of already collected data.

### Functionality overview
 - Adding new events: it allows to add new events to the database.
 - Analytics: it is possible to get aggregated data for further analysis.
 - Logging: event logging to track errors and informational messages.
 - Input Validation: checks and validates input parameters to ensure correct and secure query processing.

### Technology stack
 - [FastAPI](https://fastapi.tiangolo.com/): A framework for creating web APIs in Python.
 - [Clickhouse](https://clickhouse.com//): columnar database for fast analysis of large volumes of data.
 - [Kafka](https://kafka.apache.org/): event streaming platform to handle large amount of events.
 - [Logging](https://docs.python.org/3/library/logging.html): module for logging events.
 - [Pydantic](https://docs.pydantic.dev/latest/): A library for data validation and data schema creation.

### The System Design
![Design](./Design.png)

#### Deployment
The command below is used to launch the application. It will build and run all the necessary services.
```
docker-compose -f docker-compose.prd.yml up -d
```
The nginx is available on port: 8088
The application endpoints:
 - \<server-address>:8088/event/
 - \<server-address>:8088/analytics/query
#### Monitoring
The command below is used to monitor the services execution. Change the LOG_LEVEL environment variable to see all the messages. By default it is set to ERROR level for prod-like environments.
```
docker-compose -f docker-compose.prd.yml logs -f
```
#### Maintenance and Updates
The github actions is used to ci/cd changes. All the Commits/Pull requests pushed to master will be delivered by actions workflow. To read more about it, use [this link](https://docs.github.com/en/actions).

#### Stopping and Decommissioning
Use command below to stop the containers:
```
docker-compose -f docker-compose.prd.yml down
```
If you want to get rid of volumes:
```
docker-compose -f docker-compose.prd.yml down -v
```

### Development
You can use **docker-compose.dev.yml** configuration for development purposes in your local environment. The separate docker-compose files are used for better development expirience.

### Services
All the services consume the .env file with variables. The production containers have additional logging rules.

**clickhouse**
- This is a standard image without modifications. There is an entrypoint script to create a new database **sample** and to create a table **Events**.

**api**
- The Fast API application to handle http api requests. Dockerfile describes the image. It has dependecy on clickhouse. Moreover, it has an entrypoint bash script to validate if clickhouse is ready to accept connections.
- The **gunicorn** handles web server questions. It is set to 4 workers.

**nginx**
- The basic nginx image with a simple configuration file.

**kafka**
- The image created by wurstmeister. Kafka cluster has only one broker. Some default settings described in env file

**zookeeper**
- The image created by wurstmeister. 

### Why did I choose this stack?
**Clickhouse**
- This columnar DBMS is great for quickly returning aggregated data.
- Possibility of horizontal scaling. Master-Slave, Master-Master replications
- It was also a plus that I had little experience working with it.

**Fast API**
- Productive, lightweight python framework.
- Perhaps GO or Rust would be more suitable here, but I have absolutely no experience working with them, so I chose Fast API.
- Automatic documentation. A great 'absolutely free' addition out of the box.

**Nginx**
- This service will come in handy if we need to implement application load balancing.

**Kafka**
- I faced an issue with CPU overload by clickhouse, kafka is used here to ensure smooth processing of events to clickhouse by its own engine.


### Things for consideration
This block is to keep my thoughts for further analysis, some of the consideration depends on the facts that were not mentioned in the task. In order to enhance the solution, some details should be clarified.

**CPU overhead**
 - First iteration of the project was to ensure the direct writes to Clickhouse. However, I realised that CH becomes a cpu consumer. I decided to change the way of publishing messages to CH through Kafka engine and Materialized view. This approach allow us to move CPU overhead from DB to api application level. In my mind, to scale the api apps is "cheaper" then to scale DB.

**data storage**
 - Storing data in one table with daily partitions.
   The task states that a large amount of data is expected, but there are no specifics, so I made partitions by day. For real use, this needs to be further analyzed and partitions configured depending on the initial requirements and real requests for data.
 - For housekeeping needs the TTL option is enabled and set to event_date + 30 days. All the data older than 30 days will be removed by clickhouse.
 - MergeTree is selected as an engine.
   It is not clear from the task how to work with duplicates. I believe the MergeTree is better choice for massive insertion of data. However, there is a possibility for duplication.
 - Data compression on the server level.
   There is always a possibility to enable data compression in clickhouse. However it's not clear the expectation of the system - should it accept the inserts quickly or should it response quickly with the query result.

**horizontal scaling**
- The technologies used in this solution are good for scalling. There are several options how to achieve performance improvement by adding application servers and database servers. The load balancer will route requests between resources. It can solve not only http request overhead but the network related issue also.

**read-only replica**
- Clickhouse allows to have read-only replica. It can be used when there is a need to separate write intensive request with analytical queries. This approach can also be useful if the analytics queries come from distant sources.

**application code refactoring**<br>
Perhaps the desire to strictly type the incoming parameters for better data validation, the application API code turned out to be overloaded. From this point I see some conclusins for further analysis and enhancements:
- The response time might be improved if the data retrieved from the db transferred directly to the requestor. Manipulating with the data inside api causes additional time and resources.
- The data validation takes some resources as well.

**security**
 - This sample doesn't cover any security related questions.

### Appendix
- [Useful script](./_test/test.py) to perform MOCK data injection
- [Postman collection](./_test/api.postman_collection.json) with samples for api testing
