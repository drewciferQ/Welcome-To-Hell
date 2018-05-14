#!/usr/bin/env python

# SSID sniffer

import sys

from scapy.all import *

BEACON_TYPE = 0
BEACON_SUBTYPE = 8

ap_list = []

def packetHandler(pkt):

    if pkt.haslayer(Dot11):

        if pkt.type == 0 and pkt.subtype == 8

            if pkt.info:
                if pkt.addr2 not in ap_list:
                    ap_list.append(pkt.addr2)
                    print 'Beacon Frame - BSSID: %s SSID %s' % (pkt.addr2, pkt.info)

sniff(iface=sys.argv[1], count=int(sys.argv[2]), prn=packetHandler)
