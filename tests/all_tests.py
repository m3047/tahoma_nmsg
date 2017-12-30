#!/usr/bin/python

import unittest

from protobuf_primitives import TestProtobufVarint, TestProtobufFieldHeader, TestProtobufZigZag
from protobuf_field_types import TestPbAnyFieldWithID, TestPbAnyFieldNoID, TestPbBytesField, \
                                 TestPbFixed32Field, TestPbInt32Field, TestPbUInt32Field, \
                                 TestPbInt64Field, TestPbUInt64Field

if __name__ == '__main__':
    unittest.main(verbosity=2)
