#!/usr/bin/python3
import time
from datetime import datetime
import sys
from influxdb import InfluxDBClient
import wget
import bz2
import os

# Update the following items to match your environment.  You will need to create the influx db, 
# This script does not create it.
team = '<team number to track>'
path = '<path to download .bz2 file to>'
client = InfluxDBClient(host='<host>', port=8086)
client.switch_database('<db_name>')


measurement = "Folding Stats"

# URL to the folding at home stats file.
url = 'https://apps.foldingathome.org/daily_user_summary.txt.bz2'

iso_time = time.ctime(datetime.utcnow().timestamp())

client = InfluxDBClient(host='192.168.1.16', port=8086)
client.switch_database('fah_stats')
measurement = "Folding Stats"


class FAHStats(object):
    def __init__(self):
        self.stats = []

    def download_file(self):
        # Check for existing file, and delete if needed
        if os.path.exists(path):
            os.remove(path)

        print("Downloading New stats file from folding@home server")
        try:
            wget.download(url, path)
            return True
        except Exception:
            print("Couldn't download file, please try again later")
            return False

    def decompress_file(self):
        print("Decompressing file")
        input_file = bz2.BZ2File(path, 'rb')
        return input_file

    def process_stats(self, input_file):
        print("Reading File")
        for line in input_file.readlines():
            #Create an array object
            stats = line.decode("utf-8").strip().split("\t")
            # Validate we have all the fields we need
            if len(stats) == 4:
                user = stat[0]
                points = stats[1]
                wus = stats[2]
                team_number = stats[3]
                # Check it's out team
                if team_number == team:
                    data = [
                        {
                            "measurement": measurement,
                               "tags": {
                                   "User": user,
                                },
                                "time": iso_time,
                                "fields": {
                                   "Total Points" : points,
                                   "Total WUs": wus
                                }
                        }
                    ]
                    try:
                        client.write_points(data)
                    except Exception:
                        print("Couldn't write data to influx")
                        pass
    
            # Close the influx connection
            client.close()
        return True

    def remove_file(self):
        # Remove File
        try:
            os.remove(path)
            return True
        except Exception:
            return False


if __name__ == '__main__':
    # Create instance
    fah = FAHStats()
    # Download new file
    if fah.download_file():
        # Decompress file
        dc_file = fah.decompress_file()
        # Process Stats
        fah.process_stats(dc_file)
        # Delete File
        fah.remove_file()
