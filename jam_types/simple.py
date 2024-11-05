from scalecodec import U8, U16, U32, U64, FixedLengthArray, HexBytes, Struct, Vec, Enum, Null
from .const import hash_size, validators_count

def class_name(cls):
    return cls.__name__

n = class_name

# Out of Spec
 
class Errno(U8):
    pass

class ByteSequence(HexBytes):
    pass

class ByteArray(FixedLengthArray):
    sub_type = n(U8)
    
# Basic types

class EpochIndex(U32):
    pass

class CoreIndex(U16):
    pass

class ValidatorIndex(U16):
    pass

class TimeSlot(U32):
    pass

class OpaqueHash(ByteArray):
    element_count = hash_size

class HeaderHash(OpaqueHash):
    pass

class Entropy(OpaqueHash):
    pass

class EntropyBuffer(FixedLengthArray):
    sub_type = n(Entropy)
    element_count = 4

class ServiceId(U32):
    pass

class Gas(U64):
    pass

