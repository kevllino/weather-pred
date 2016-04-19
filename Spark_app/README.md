<h1>Spark App</h1>

The WeatherPred Data Pipeline consists in 3 parts:
<ol>
<li>
<b>extract.sh</b> allowed to collect the data from the U.S. NCDC repository.<br>
</li>

<li>
<b>text-manip.sh</b> allowed to process, and transform the data in a format which could be fed to Spark.<br>
</li>

<li>
<b>weather_predict.py</b> ecncompasses the processing of the data in SPark, the implementation and tunning of the regression model and an evaluation of its performance. It also allowed to store the predictions to S3. <br>
</li>
</ol>
