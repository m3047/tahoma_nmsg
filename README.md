# Tahoma NMSG

A pure-python implementation of Protobuf and NMSG, leveraging Scapy. Scapy is
probably not a module which is familiar to IT shops, however if you're in
"cyber" you're probably already familiar with it or have been looking for an
excuse to become familiar with it.

You don't have to use this code with Scapy, you're welcome to bend it to your
own purposes.

## Compatibility and Prerequisites

Requires Scapy. Recommended installation is with `pip`.

Tested with the following versions of Scapy:

* 2.3.2
* 2.3.3

## Installation

Download the tarfile and unpack it in your project. It will unpack into a
directory `tahoma_nmsg`, which contains another directory named `tahoma_nmsg` which
is the actual python package.

## Usage

The protobuf implementation is in `protobuf`. You will not normally use this
module directly. Scapy and protobuf both take a declarative approach to
definitions; this implementation uses the scapy paradigm. There is no definition
compiler. If you want to implement your own definitions look at `nmsg`.

Subclasses of `Protobuf` are both a packet and a field: you define the packet
and then reference the `Field()` factory method to declare an instance of
the protobuf within `fields_desc` in a packet definition.

There are two `report*.py` examples for consuming SIE channel 213 data.

### report-socket.py

Consumes SIE channel 213 from an `sratunnel` instance terminated at a local UDP
port (127.0.0.1:5000). Best way to do this is with two windows.

In one, run the `sratunnel` instance, which will probably look something like this:

```
sratunnel -c ch213 -w 'ch=213' -o nmsg:127.0.0.1,5000 ...
```

In the other, run `report-socket.py`:

```
./report-socket.py
```

### report-pcap-file.py

Consumes data from a PCAP of SIE channel 213. A sample is provided, which was produced
from the accompanying `ch213.jsonl` by running `nmsgtool -j ch213.jsonl -s 127.0.0.1/5000,10 --unbuffered`.

Run it and you'll see output:

```
./report-pcap-file.py
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

Ensure that you're in the directory above the actual package (`ch213.pcap` will be in
this directory).

```
>>> from tahoma_nmsg.nmsg import NMSG
>>> from scapy.all import bind_layers, UDP, sniff
>>> bind_layers(UDP,NMSG,dport=5000)
>>> pkt = sniff(count=1,offline='ch213.pcap')[0]
>>> pkt
<Ether  dst=00:00:00:00:00:00 src=00:00:00:00:00:00 type=0x800 |<IP  version=4 ihl=5 tos=0x0 len=218 id=51764 flags=DF frag=0 ttl=64 proto=udp chksum=0x71dc src=127.0.0.1 dst=127.0.0.1 options=[] |<UDP  sport=55721 dport=5000 len=198 chksum=0xfed9 |<NMSG  magic_value='NMSG' flag_zlib=0 flag_frag=0 flag_reserved=0 version=2 container_length=180 container=<NmsgContainer payload=<NmsgPayload vid=2 msgtype=5 time_sec=-757159019 time_nsec=2608577 newdomain=<NmsgNewDomain domain='example.com.' time_seen=1514317964 rrname='ww92.8299af6e-7c60-46f4-bbde-f3f67b95ae41.example.com.' type=2 rrclass=1 rdata='ns.example.com.' rdata='ns2.example.com.' bailiwick='example.com.' |> source=2713322191 |> crc=2790016156 sequence=0 sequence_id=5485767635228153502 |> |>>>>
```

The pcap file was made by feeding JSON to `nmsgtool`. You can confirm for yourself that this is the first record in `ch213.jsonl`.

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

