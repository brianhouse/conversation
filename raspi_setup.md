### updates
    sudo apt-get update
    sudo apt-get upgrade

### network
    ifconfig
    sudo nano /etc/network/interfaces

    auto lo
    iface lo inet loopback

    auto eth0
    allow-hotplug eth0
    iface eth0 inet manual

    auto wlan0
    allow-hotplug wlan0
    iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

    auto wlan1
    allow-hotplug wlan1
    iface wlan1 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    network={
    ssid="DFLTD"
    psk="TKM6ZG7BTXJM6XZR"
    proto=RSN
    key_mgmt=WPA-PSK
    pairwise=CCMP
    auth_alg=OPEN
    }    


### time
    sudo /etc/init.d/ntp status
    ntpq -c rl

### setup
    sudo apt-get install monit
    sudo apt-get install python3-pip
    sudo apt-get install python3-rpi.gpio
    sudo pip-3.2 install PyYAML


### testing with Granu
- everything plugged into switch, set to dchp
- share internet connection

### shutdown, remember:
    sudo shutdown -h now


    u: sounderbox
    p: raspberry
