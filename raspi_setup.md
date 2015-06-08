
### login
    ssh pi@sounderbox.local
    pi:raspberry

### config
    sudo raspi-config

- boot options
- hostname
- ssh

### updates
    sudo apt-get update
    sudo apt-get upgrade

### network
    ifconfig
    sudo nano /etc/network/interfaces

    auto lo
     
    iface lo inet loopback
    iface eth0 inet dhcp
     
    allow-hotplug wlan0
    auto wlan0
    face wlan0 inet dhcp
            wpa-ssid "ssid"
            wpa-psk "password"

    sudo ifup wlan0
    ping google.com

### time
    sudo /etc/init.d/ntp status
    ntpq -c rl

### hostname / remote
    sudo nano /etc/hosts
    sudo nano /etc/hostname
    sudo /etc/init.d/hostname.sh
    sudo reboot
change raspberrypi references to desired

    ssh pi@sounderbox.local

### sound
    sudo nano /etc/modprobe.d/alsa-base.conf
    options snd-usb-audio index=-2          # change to 0
    sudo reboot
    alsamixer

### python
    sudo apt-get install python3-setuptools
    sudo easy_install3 pip    

### monit
    sudo apt-get install monit
see monitrc.smp

### testing with Granu
- everything plugged into switch, set to dchp
- share internet connection

### shutdown, remember:
    sudo shutdown -h now


### notes
from shawn -- disk will get corrupted after awhile, have to disable writes

create an image: http://smittytone.wordpress.com/2013/09/06/back-up-a-raspberry-pi-sd-card-using-a-mac/

    # be sure you have the right disk!
    diskutil list
    diskutil unmountDisk /dev/disk1
    sudo dd if=/dev/rdisk1 of=~/Desktop/pi.img bs=1m            # note the 'r' prefix


locking:
http://raspberrypi.stackexchange.com/questions/5112/running-on-read-only-sd-card



### wiring

    git clone git://git.drogon.net/wiringPi
    cd wiringPi
    ./build

    sudo apt-get install python3-dev
    sudo apt-get install python3-rpi.gpio 


    import RPi.GPIO as GPIO
    import time

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)

    for x in range(0,10):
      time.sleep(5)
      GPIO.output(4,1)
      time.sleep(5)
      GPIO.output(4,0)    

sudo pip3 install PyYAML
