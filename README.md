# RPi-Temperature-logger
Raspberry Pi programs for logging temperature with DS18B20+ one wire sensor.

This documents how I set up my temperature logging system with 2 sensors.

System:
Raspberry Pi 3, Raspbian Jessie, Python3, DS18B20+ sensors 


Wiring and testing information:
https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi

- Load kernel modules
```
sudo modprobe w1-gpio
sudo modprobe w1-therm
```
-- these seem to load automatically on boot

check your sensors:
```
ls /sys/bus/w1/devices
28-000008a260c3  28-000008a4a333  w1_bus_master1
cat /sys/bus/w1/devices/28-000008a260c3/w1_slave
7a 01 4b 46 7f ff 06 10 0b : crc=0b YES
7a 01 4b 46 7f ff 06 10 0b t=23625
```

- Set ramdisk, so that SD card is not constantly written to avoid wearing
```
sudo mkdir /mnt/ramdisk
sudo chmod ugo+rwx /mnt/ramdisk
```
Modify /etc/fstab by adding line:
```
tmpfs /mnt/ramdisk tmpfs defaults,noatime,nosuid,mode=0777,size=20m 0 0
```
-- will give all rights to access this directory

- Download and modify scripts
```
readtemp.sh
temperature_logger.py
```
Change the sensor ID:s in "readtemp.sh".
You may want to modify temperature_logger.py so that the outputFile points to a desired location.

- Set cron so that these scripts are run at desired intervals
```
crontab -e
```

Add these lines to the end of crontab. Check that file paths match yours.
```
#save temperature measurements to a file in ramdisk, every other minute
*/2 * * * * /home/pi/temperature/readtemp.sh >> /mnt/ramdisk/tempreadings.txt

#rename temperature data at midnight
59 23 * * * mv /mnt/ramdisk/tempreadings.txt /mnt/ramdisk/tempreadings_old.txt
#process temperature data
30 0 * * * python3 /home/pi/temperature_logger.py
```
## Outcome
This will append "tempreadings.txt" every 2nd minute and one minute to midnight will rename this file. Half hour past midnight the renamed file is read by the python script, which will make file "17-02-05.txt" (YY-MM-DD) containing the days readings formatted as "17-02-05 23:58:01 23.500 19.187" line by line.

## Uploading to Google sheets

## Plotting and viewing from local network


