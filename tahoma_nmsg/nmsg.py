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

"""Protobuf declarations for NMSG.

The following are defined:

    NmsgNewDomain       Channel data.
    NmsgPayload         Wrapper for channel data with vendor id and message type.
    NmsgContainer       Wrapper for the wrapper.

The following is not a protobuf:

    NMSG                The actual UDP packet definition.
"""

import struct

from scapy.all import Packet, Field, bind_layers, UDP, \
                      StrFixedLenField, BitField, ByteField, IntField, DNSStrField, RDataField, NoPayload, DNSgetstr

from .protobuf import PbBytesField, PbUInt32Field, PbAnyField, PbUInt64Field, PbFixed32Field, PbInt64Field, \
                     Protobuf
                  
#from scapy.config import conf
#conf.debug_dissector = True


class ImprovedRDataField(RDataField):
    """The scapy RDataField doesn't understand NS, CNAME."""
    #TODO: I should submit this to the scapy project.
    def m2i(self,pkt,s):
        if pkt.type in (2,5):   # NS, CNAME
            return DNSgetstr(s,0)[0]
        return RDataField.m2i(self,pkt,s)
    

class NmsgNewDomain(Protobuf):
    """Protobuf definition for channel 213."""
    fields_desc = [
            PbBytesField("domain",id=1,cls=DNSStrField("domain_fqdn",'')),
            PbUInt32Field("time_seen",id=2),
            PbAnyField("dedupe_type",id=13),    # See note regarding dns.RDataField
            PbUInt32Field("count",id=10),
            PbUInt32Field("time_first",id=11),
            PbUInt32Field("time_last",id=12),
            PbUInt32Field("zone_time_first",id=17),
            PbUInt32Field("zone_time_last",id=18),
            PbAnyField("response_ip",id=14),
            PbBytesField("rrname",id=3,cls=DNSStrField("rrname_fqdn",'')),
            # NOTE: Has to be "type" so that dns.RDataField can find it. Also has to
            # be already parsed from the stream before dns.RDataField is encountered.
            #PbUInt32Field("rrtype",id=4),
            PbUInt32Field("type",id=4),
            PbUInt32Field("rrclass",id=5),
            PbUInt32Field("rrttl",id=6),
            PbBytesField("rdata",id=7,multi=True,
                         provide_length_from=True,cls=ImprovedRDataField("rdata_field",'')),
            #PbBytesField("rdata",id=7,multi=True),
            PbBytesField("response",id=15),
            PbBytesField("bailiwick",id=16,cls=DNSStrField("bailiwick_fqdn",'')),
            PbBytesField("keys",id=9,multi=True),
            PbAnyField("new_domain",id=19),
            PbAnyField("new_rrname",id=20),
            PbAnyField("new_rrtype",id=21),
            PbAnyField("new_rr",id=22,multi=True),
            PbAnyField("new_rrset",id=23)
        ]

class NmsgPayload(Protobuf):
    """Payload wrapper protobuf.
    
    Vendor ID will always be 2. Message type 5 means NmsgNewDomain (see above).
    
    At the moment, NmsgNewDomain is hard-coded here.
    """
    fields_desc = [
            PbUInt32Field("vid",2,id=1),
            PbUInt32Field("msgtype",5,id=2),
            PbInt64Field("time_sec",id=3),
            PbFixed32Field("time_nsec",id=4),
            NmsgNewDomain.Field("newdomain",id=5),
            PbUInt32Field("source",id=7),
            PbUInt32Field("operator",id=8),
            PbUInt32Field("group",id=9)
        ]

class NmsgContainer(Protobuf):
    fields_desc = [
            NmsgPayload.Field("payload",id=1),
            PbUInt32Field("crc",id=2),
            PbUInt32Field("sequence",id=3),
            PbUInt64Field("sequence_id",id=4)
        ]
    
class NMSG(Packet):
    """This is what you see if you grab the UDP packets.
    
    If you want to grab raw packets and have them automagically recognized,
    then you need to call bind_layers(), which looks something like this:
    
        # This is just a hack. It depends on the fact that sratunnel was terminated
        # on UDP port 5000.
        bind_layers(UDP, NMSG, dport=5000)
    
    If you're actually listening in layer 3 mode, then NMSG is what you'll see,
    you won't see the network layers (Ethernet, IP, UDP).
    
    NOT SUPPORTED: zlib compression and fragmentation are not supported.
    
    NOT TESTED: multiple payloads are not tested.
    """
    fields_desc = [
            StrFixedLenField("magic_value","NMSG",4),
            BitField("flag_zlib",0,1),
            BitField("flag_frag",0,1),
            BitField("flag_reserved",0,6),
            ByteField("version",2),
            IntField("container_length",0),
            NmsgContainer.Field("container",length_from=lambda pkt: pkt.container_length)
       ]

# This is just a hack. It depends on the fact that sratunnel was terminated
# on UDP port 5000.
#bind_layers(UDP, NMSG, dport=5000)

