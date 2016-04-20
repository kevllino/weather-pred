<h1>Quick guide to jelp you run a Spark application on an EC2 cluster</h1> with the right configurations (toavoid e.g. MetadataFailedFetchException) 

<ol>
<li>
<b>Export AWS credentials</b> <br>
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXX<br>
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXX<br>
</li>
<li>
<b>Create cluster in EC2</b><br>
./spark-ec2 -k mykey -i mykey.pem -s 2 --instance-type m3.xlarge -r eu-west-1 --hadoop-major-version 2 launch weather-cluster8<br>
</li>
<li>
<b>Get the master public DNS</b><br>
./spark-ec2 -r eu-west-1  get-master weather-cluster8<br>
</li>
<li>
<b>Copy files with SCP from local to Spark EC2 cluster</b><br>
scp -i mykey.pem -r eu-west-1 ./weather_predicta.py root@ec2-52-16-114-50.eu-west-1.compute.amazonaws.com:~<br>
</li>
<li>
<b>Login or SSH master </b><br>
./spark-ec2 -k mykey -i mykey.pem  -r eu-west-1 login weather-cluster8<br>
ssh -i mykey.pem root@ec2-52-16-114-50.eu-west-1.compute.amazonaws.com<br>
</li>
<li>
<b>Store data in S3 </b><br>
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXX<br>
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXX<br>
sc.textFile(“s3n://usweatherdata/clean_data2.txt”)<br>
</li>
<li>
<b>Run the application </b><br>
./spark/bin/spark-submit --master spark://ec2-52-16-114-50.eu-west-1.compute.amazonaws.com:7077 --executor-memory 8g --driver-memory 4g --executor-cores 4 --num-executors 3 ./weather_predicta.py<br>
</li>
<li>
<b>Destroy the cluster instances</b><br>
./spark-ec2 -k mykey -i mykey.pem -r eu-west-1 destroy weather-cluster8<br>
</li>
</ol>
