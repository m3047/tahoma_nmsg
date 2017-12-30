#!/usr/bin/python

import unittest
import tahoma_nmsg.protobuf as protobuf


class ProtobufPacket(protobuf.Protobuf):
    fields_desc = []

def hex2str(h):
    """Converts a string of hexadecimal digits into an equivalent string."""
    return ''.join([chr(eval('0x'+h[n*2:n*2+2])) for n in range(len(h)/2)])


class TestPbAnyFieldWithID(unittest.TestCase):
    """PbAnyField with an ID specified."""
    
    def setUp(self):
        self.field = protobuf.PbAnyField('test_field',id=5)
        self.packet = ProtobufPacket()
        return

    def test_getfield_bad_id(self):
        self.assertRaises(protobuf.FieldIDMismatchError,
            self.field.getfield, self.packet, hex2str('3a0648656c6c6f21')
        )
        return
    
    def test_getfield_good_id(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2a0648656c6c6f21')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,'Hello!',"Value should be 'Hello!' (without the quotes).")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2a0648656c6c6f21')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,"'Hello!'","Value should be 'Hello!' (with the quotes).")
        return

class TestPbAnyFieldNoID(unittest.TestCase):
    """PbAnyField with no ID specified."""

    def setUp(self):
        self.field = protobuf.PbAnyField('test_field')
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_no_id(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2a0648656c6c6f21')
        )
        self.assertEqual(v,'Hello!',"Value should be 'Hello!' (without the quotes).")
        self.assertEqual(self.field.name,'test_field',"Name of field should be test_field.")
        self.assertEqual(self.field.pb_id,5,"pb_id should be 5.")
        return
    
class TestPbBytesField(unittest.TestCase):

    def setUp(self):
        self.field = protobuf.PbBytesField('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('28')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2a0648656c6c6f21')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,'Hello!',"Value should be 'Hello!' (without the quotes).")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2a0648656c6c6f21')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,"'Hello!'","Value should be 'Hello!' (with the quotes).")
        return
    
class TestPbFixed32Field(unittest.TestCase):

    def setUp(self):
        self.field = protobuf.PbFixed32Field('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('2a03e81e97')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2d03e81e97')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,2535385091,"Value should be 2535385091.")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2d03e81e97')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,'2535385091',"Value should be '2535385091'.")
        return
    
class TestPbInt32Field(unittest.TestCase):
    
    def setUp(self):
        self.field = protobuf.PbInt32Field('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('29cd2f')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('28cd2f')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,-3047,"Value should be -3047.")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('28cd2f')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,'-3047',"Value should be '-3047'.")
        return
    
class TestPbUInt32Field(unittest.TestCase):

    def setUp(self):
        self.field = protobuf.PbUInt32Field('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('29cd2f')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('28cd2f')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,6093,"Value should be 6093.")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('28cd2f')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,'6093',"Value should be '6093'.")
        return

class TestPbInt64Field(unittest.TestCase):

    def setUp(self):
        self.field = protobuf.PbInt64Field('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('2997829cbaf2e105')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2897829cbaf2e105')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,-12676925456524,"Value should be -12676925456524.")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2897829cbaf2e105')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,'-12676925456524',"Value should be '-12676925456524'.")
        return

class TestPbUInt64Field(unittest.TestCase):

    def setUp(self):
        self.field = protobuf.PbUInt64Field('test_field',id=5)
        self.packet = ProtobufPacket()
        return
    
    def test_getfield_bad_wtype(self):
        self.assertRaises(protobuf.FieldTypeMismatchError,
            self.field.getfield, self.packet, hex2str('2997829cbaf2e105')
        )
        return
    
    def test_getfield(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2897829cbaf2e105')
        )
        self.assertEqual(s,'',"Buffer should be empty.")
        self.assertEqual(v,25353850913047,"Value should be 25353850913047.")
        return
    
    def test_i2repr(self):
        s,v = self.field.getfield(self.packet,
            hex2str('2897829cbaf2e105')
        )
        r = self.field.i2repr(self.packet,v)
        self.assertEqual(r,'25353850913047',"Value should be '25353850913047'.")
        return
    

if __name__ == '__main__':
    unittest.main()
    