#!/usr/bin/python
# Copyright (c) 2017 by Fred Morris Tacoma WA and/or Farsight Security, Inc. San Mateo CA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample program which reads channel 213 pcap data from a file.

The data file ostensibly being produced by running:

  sratunnel -c ch213 -o nmsg:127.0.0.1,5000 ...

and then capturing that to a file with:

  tcpdump -ilo -s0 -n -wch213.pcap port 5000
  
"""

from sys import stderr
from scapy.all import sniff, StreamSocket, NoPayload

from tahoma_nmsg.nmsg import NMSG, NmsgContainer, NmsgPayload, NmsgNewDomain

UDP_IP = "127.0.0.1"
UDP_PORT = 5000

from scapy.all import UDP, bind_layers
bind_layers(UDP, NMSG, dport=UDP_PORT)

TOP_PACKET = NMSG
PAYLOAD_PACKET = NmsgNewDomain

def write(pkt):
    opkt = pkt
    while True:
        if isinstance(pkt,PAYLOAD_PACKET):
            print '\t'.join(str(getattr(pkt,f,None)) for f in ('rrname','type','rdata') )
            return
        if isinstance(pkt,NoPayload):
            print >>stderr, repr(opkt)
            return
        pkt = pkt.payload
    return

def main():
    # There are 4 records in the shipped pcap sample. You may need to adjust this.
    sniff(offline='ch213.pcap',count=4,prn=write)
    return

if __name__ == '__main__':
    main()
    
