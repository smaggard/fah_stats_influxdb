# fah_stats_influxdb

## Setup
1. Create an influx database on your influx server.
2. Modify update_stats.py and update the following section
```team = '<team number to track>'
path = '<path to download .bz2 file to>'
client = InfluxDBClient(host='<host>', port=8086)
client.switch_database('<db_name>')```
3. Install the required modules
``` pip3 install influxdb
pip3 install wget
pip3 install bz3```
4. Run script
``` python3 update_stats.py```
