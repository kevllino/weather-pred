# WeatherPred
WeatherPred: An application to predict temperatures using Spark mllib

Our project, WeatherPred is an application enabling weather predictions in the 50 most populated American cities. The genuine objective behind the application of this application was to use some of the cloud technologies available to deal with large datasets. Moreover, we were able to gain more expertise in Machine Learning by training a regression model on our data to predict future temperatures for a given city. In order to process, and clean the data, we leveraged the power of bash and awk by coding many scripts to clean the raw data. Then, the processing part was also mostly done in Apache Spark which we also used to implement the machine learning model thanks to the mllib library. It is important to note that because of the insufficient computing processing power and storage that our laptops were able to provide, we used AWS by deploying EC2 instances on a standalone Spark cluster. Finally, we took the opportunity to try Amazon ML on our data and assessed how it compared to our ML model in Spark. 
 
The below details all of the Data Pipeline implemntation: 

![test - new page 1](https://cloud.githubusercontent.com/assets/9676662/14622302/f1a743de-05c0-11e6-993a-3def75723c85.png)
