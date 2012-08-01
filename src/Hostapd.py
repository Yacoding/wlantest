#!/usr/bin/python
##
## Hostapd.py
##
## Author(s):
##  - Maxence VIALLON <mviallon@aldebaran-robotics.com>
##

CONF_FILE = "/etc/hostapd.conf"
IFACE = "wlan1"
DRIVER = "nl80211"

NAS_IP = "192.168.2.2"
RADIUS_IP = "192.168.2.3"
RADIUS_PORT = "1812"
RADIUS_SECRET = "testing123"

import subprocess
import os,signal
from time import sleep

class Config:
    """
    Class to write conf file
    """

    def __init__(self):
        self.config = open (CONF_FILE, "w+")
        # Set shared settings
        self.set("interface", IFACE)
        self.set("driver", DRIVER)

    def default(self):
        self.setChannel('11')
        self.setMode('g')

    def setChannel(self, chan):
        self.set("channel", chan)

    def setMode(self, mode):
        self.set("hw_mode", mode)

    def setHidden(self, bool):
        if bool == 'true':
            self.set("ignore_broadcast_ssid", "1")

    def set(self, key, value):
        self.config.write("%s=%s\n" %(key,value))

    def close(self):
        self.config.close()

class Hostapd:
    """
    Class to manage hostapd
    """

    def __init__(self):
        # Set default config to let hostapd start
        config = Config()
        config.default()
        config.close()

        self.cmd = ["hostapd", CONF_FILE]
        self.proc = subprocess.Popen(self.cmd)
        sleep(3)

    def open(self, mode, chan, ssid, hidden):

        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)

        config.close()
        self.reload()

    def wep(self, mode, chan, ssid, hidden, passphrase):

        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)
        config.set("wep_default_key", "0")
        config.set("wep_key0", passphrase)

        config.close()
        self.reload()

    def wpa_psk(self, mode, chan, ssid, hidden, passphrase):

        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)
        config.set("wpa", "1")
        config.set("wpa_passphrase", passphrase)
        config.set("wpa_key_mgmt", "WPA-PSK")
        config.set("wpa_pairwise", "TKIP")

        config.close()
        self.reload()        

    def wpa2_psk(self, mode, chan, ssid, hidden, passphrase):

        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)
        config.set("wpa", "2")
        config.set("wpa_passphrase", passphrase)
        config.set("wpa_key_mgmt", "WPA-PSK")
        config.set("wpa_pairwise", "CCMP")

        config.close()
        self.reload()        

    def wpa_eap(self, mode, chan, ssid, hidden):
         
        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)
        config.set("ieee8021x", "1")
        config.set("own_ip_addr", NAS_IP)
        config.set("auth_server_addr", RADIUS_IP)
        config.set("auth_server_port", RADIUS_PORT)
        config.set("auth_server_shared_secret", RADIUS_SECRET)
        config.set("wpa", "1")
        config.set("wpa_key_mgmt", "WPA-EAP")
        config.set("wpa_pairwise", "TKIP")

        config.close()
        self.reload()

    def wpa2_eap(self, mode, chan, ssid, hidden):
         
        config = Config()

        config.setMode(mode)
        config.setChannel(chan)
        config.set("ssid", ssid)
        config.setHidden(hidden)
        config.set("ieee8021x", "1")
        config.set("own_ip_addr", NAS_IP)
        config.set("auth_server_addr", RADIUS_IP)
        config.set("auth_server_port", RADIUS_PORT)
        config.set("auth_server_shared_secret", RADIUS_SECRET)
        config.set("wpa", "2")
        config.set("wpa_key_mgmt", "WPA-EAP")
        config.set("wpa_pairwise", "CCMP")

        config.close()
        self.reload()

    def reload(self):
        os.kill(self.proc.pid, signal.SIGHUP)
        sleep(1)

    def kill(self):
        os.kill(self.proc.pid, signal.SIGTERM)
        sleep(1)

if (__name__ == "__main__"):

    myhost = Hostapd()
    myhost.wpa2_psk(mode = 'g', \
                chan = '4', \
                ssid = 'Ohyeah', \
                passphrase = '12345678')
