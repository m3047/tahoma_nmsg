# Tahoma NMSG

A pure-python implementation of Protobuf and NMSG, leveraging Scapy. Scapy is
probably not a module which is familiar to IT shops, however if you're in
"cyber" you're probably already familiar with it or have been looking for an
excuse to become familiar with it.

You don't have to use this code with Scapy, you're welcome to bend it to your
own purposes.

## Installation

Download the tarfile and unpack it in your project. It will unpack into a
directory `tahoma_nmsg`.

## Usage

The protobuf implementation is in `protobuf`. You will not normally use this
module directly. Scapy and protobuf both take a declarative approach to
definitions; this implementation uses the scapy paradigm. There is no definition
compiler. If you want to implement your own definitions look at `nmsg`.

Subclasses of `Protobuf` are both a packet and a field: you define the packet
and then reference the `Field()` factory method to declare an instance of
the protobuf within `fields_desc` in a packet definition.

`report.py` is a simple example for consuming SIE channel 213 from an 
`sratunnel` instance terminated at a local UDP port (127.0.0.1:5000). It can
also read from pcap files. To run the program, copy it to the enclosing directory
and run it from there:

```
cp report.py ..
cd ..
python report.py
```

To read from a PCAP file named `ch213.pcap`:

1) Comment out the lines:

```
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

sniff(opened_socket=StreamSocket(sock,TOP_PACKET), prn=write)
```

2) Uncomment the lines:

```
from scapy.all import bind_layers
bind_layers(UDP, NMSG, dport=UDP_PORT)

sniff(offline='ch213.pcap', prn=write)
```

## Idioms

Several idioms are useful with Scapy/NMSG. We will assume that the variable
`pkt` contains a packet and you're in an interactive python shell.

### Displaying an Entire Payload

Scapy nests protocols as _layers_. To display all layers of the packet:

```
>>> pkt
```
or
```
>>> repr(pkt)
```

### Printing a Field Value

Scapy exposes fields as attributes, and will (mostly) find the correct layer.

```
>>> pkt.rrname
```

### Locating the Actual Payload

Payloads are chained together. The actual payload is `NmsgNewDomain`. The end
of the payload list is terminated with an instance of `NoPayload`. To locate
the `NmsgNewDomain` instance:

```
>>> while not isinstance(pkt,NmsgNewDomain): pkt = pkt.payload
```

### Getting One Packet from a PCAP

The use of `bind_layers()` here is a hack which relies on the fact that the capture
file was generated from port 5000, i.e. `tcpdump port 5000`

```
>>> from tahoma_nmsg.nmsg import NMSG
>>> from scapy.all import bind_layers, UDP, sniff
>>> bind_layers(UDP,NMSG,dport=5000)
>>> pkt = sniff(count=1,offline='tahoma_nmsg/ch213.pcap')[0]
```

## License

 Copyright (c) 2017 by Fred Morris Tacoma WA and/or Farsight Security, Inc. San Mateo CA

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

