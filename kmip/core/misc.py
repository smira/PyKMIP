# Copyright (c) 2014 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from kmip.core.enums import Tags
from kmip.core.enums import QueryFunction as QueryFunctionEnum

from kmip.core.primitives import Enumeration
from kmip.core.primitives import Interval
from kmip.core.primitives import Struct
from kmip.core.primitives import TextString

from kmip.core.utils import BytearrayStream


class Offset(Interval):
    """
    An integer representing a positive change in time.

    Used by Rekey and Recertify requests to indicate the time difference
    between the InitializationDate and the ActivationDate of the replacement
    item to be created. See Sections 4.4, 4.5, and 4.8 of the KMIP v1.1
    specification for more information.
    """

    def __init__(self, value=None):
        """
        Construct an Offset object.

        Args:
            value (int): An integer representing a positive change in time.
                Optional, defaults to None.
        """
        super(Offset, self).__init__(value, Tags.OFFSET)


class QueryFunction(Enumeration):
    """
    An encodeable wrapper for the QueryFunction enumeration.

    Used by Query requests to specify the information to retrieve from the
    KMIP server. See Sections 4.25 and 9.1.3.2.24 of the KMIP v1.1
    specification for more information.
    """
    ENUM_TYPE = QueryFunctionEnum

    def __init__(self, value=None):
        """
        Construct a QueryFunction object.

        Args:
            value (QueryFunction enum): A QueryFunction enumeration value,
                (e.g., QueryFunction.QUERY_OPERATIONS). Optional, default to
                None.
        """
        super(QueryFunction, self).__init__(value, Tags.QUERY_FUNCTION)


class VendorIdentification(TextString):
    """
    A text string uniquely identifying a KMIP vendor.

    Returned by KMIP servers upon receipt of a Query request for server
    information. See Section 4.25 of the KMIP v1.1. specification for more
    information.
    """

    def __init__(self, value=None):
        """
        Construct a VendorIdentification object.

        Args:
            value (str): A string describing a KMIP vendor. Optional, defaults
                to None.
        """
        super(VendorIdentification, self).__init__(
            value, Tags.VENDOR_IDENTIFICATION)


class ServerInformation(Struct):
    """
    A structure containing vendor-specific fields and/or substructures.

    Returned by KMIP servers upon receipt of a Query request for server
    information. See Section 4.25 of the KMIP v1.1 specification for more
    information.

    Note:
    There are no example structures nor data encodings in the KMIP
    documentation of this object. Therefore this class handles encoding and
    decoding its data in a generic way, using a BytearrayStream for primary
    storage. The intent is for vendor-specific subclasses to decide how to
    decode this data from the stream attribute. Likewise, these subclasses
    must decide how to encode their data into the stream attribute. There
    are no arguments to the constructor and therefore no means by which to
    validate the object's contents.
    """

    def __init__(self):
        """
        Construct a ServerInformation object.
        """
        super(ServerInformation, self).__init__(Tags.SERVER_INFORMATION)

        self.data = BytearrayStream()

        self.validate()

    def read(self, istream):
        """
        Read the data encoding the ServerInformation object and decode it into
        its constituent parts.

        Args:
            istream (Stream): A data stream containing encoded object data,
                supporting a read method; usually a BytearrayStream object.
        """
        super(ServerInformation, self).read(istream)
        tstream = BytearrayStream(istream.read(self.length))

        self.data = BytearrayStream(tstream.read())

        self.is_oversized(tstream)
        self.validate()

    def write(self, ostream):
        """
        Write the data encoding the ServerInformation object to a stream.

        Args:
            ostream (Stream): A data stream in which to encode object data,
                supporting a write method; usually a BytearrayStream object.
        """
        tstream = BytearrayStream()
        tstream.write(self.data.buffer)

        self.length = tstream.length()
        super(ServerInformation, self).write(ostream)
        ostream.write(tstream.buffer)

    def validate(self):
        """
        Error check the types of the different parts of the ServerInformation
        object.
        """
        self.__validate()

    def __validate(self):
        # NOTE (peter-hamilton): Intentional pass, no way to validate data.
        pass

    def __eq__(self, other):
        if isinstance(other, ServerInformation):
            if len(self.data) != len(other.data):
                return False
            elif self.data != other.data:
                return False
            else:
                return True
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, ServerInformation):
            return not (self == other)
        else:
            return NotImplemented

    def __repr__(self):
        return "ServerInformation()"

    def __str__(self):
        return str(self.data)