# fah_stats_influxdb
A small python application that will download the public stats file from folding at home and import the stats for your team into an influxdb.

You can then utilize the influx db to display those in grafana.

## Setup
1. Create an influx database on your influx server.
2. Modify update_stats.py and update the following section
```
team = '<team number to track>'
path = '<path to download .bz2 file to>'
client = InfluxDBClient(host='<host>', port=8086)
client.switch_database('<db_name>')
```
3. Install the required modules
```
pip3 install influxdb
pip3 install wget
pip3 install bz2
```
4. Run script
Easiest way to do this would be to add it to a cronjob, but no more often than every 10 minutes
``` 
python3 update_stats.py
```
5. Import Grafana dashboard
You can import the grafana dashboard by going to the import page in grafana and pasting in in the JSON from the dashboard.json file
