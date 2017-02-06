# RPi-Temperature-logger
Raspberry Pi programs for logging temperature with DS18B20+ one wire sensor.

This documents how I set up my temperature logging system with 2 sensors.

System:
Raspberry Pi 3, Raspbian Jessie, Python3, DS18B20+ sensors 


Wiring and testing information:
https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi

1. Load kernel modules \n
sudo modprobe w1-gpio
sudo modprobe w1-therm
-- these seem to load automatically on boot

check your sensors:
ls /sys/bus/w1/devices
28-000008a260c3  28-000008a4a333  w1_bus_master1
and data:
cat /sys/bus/w1/devices/28-000008a260c3/w1_slave
7a 01 4b 46 7f ff 06 10 0b : crc=0b YES
7a 01 4b 46 7f ff 06 10 0b t=23625

2. Set ramdisk, so that SD card is not constantly written to avoid wearing
sudo mkdir /mnt/ramdisk
sudo chmod ugo+rwx /mnt/ramdisk

Modify /etc/fstab by adding line:
tmpfs /mnt/ramdisk tmpfs defaults,noatime,nosuid,mode=0777,size=20m 0 0
-- will give all rights to access these directories

3. Download and modify scripts
readtemp.sh
temperature_logger.py
