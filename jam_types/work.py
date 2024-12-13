from .const import auth_pool_max_size, auth_queue_size, core_count
from .simple import *
from .simple import (
    U16,
    U32,
    BoundedVec,
    ByteSequence,
    CoreIndex,
    Enum,
    FixedLengthArray,
    Gas,
    Null,
    OpaqueHash,
    ServiceId,
    Struct,
    Vec,
)
from .utils import class_name as n


class WorkReportHash(OpaqueHash):
    pass

class WorkPackageHash(OpaqueHash):
    pass

class SegmentTreeRoot(OpaqueHash):
    pass

class WorkPackageAvailSpec(Struct):
    type_mapping = [
        ("hash", "OpaqueHash"),
        ("len", "U32"),
        ("root", "OpaqueHash"),
        ("segments", "OpaqueHash")
    ]

class ImportSpec(Struct):
    type_mapping = (
        ("tree_root", "OpaqueHash"),
        ("index", "U16")
    )

class ExtrinsicSpec(Struct):
    type_mapping = (
        ("hash", "OpaqueHash"),
        ("len", "U32")
    )

class WorkItem(Struct):
    type_mapping = [
        ("service", "ServiceId"),
        ("code_hash", "OpaqueHash"),
        ("payload", "ByteSequence"),
        ("refine_gas_limit", "Gas"),
        ("accumulate_gas_limit", "Gas"),
        ("import_segments", "Vec<ImportSpec>"),
        ("extrinsic", "Vec<ExtrinsicSpec>"),
        ("export_count", "U16")
    ]

class Authorizer(Struct):
    type_mapping = [
        ("code_hash", "OpaqueHash"),
        ("params", "ByteSequence")
    ]

class AuthPool(BoundedVec):
    # Authorizer hash (blake2b(encode(Authorizer)))
    sub_type = n(OpaqueHash)
    max_elements = auth_pool_max_size

class AuthPools(FixedLengthArray):
    sub_type = n(AuthPool)
    element_count = core_count

class AuthQueue(FixedLengthArray):
    # Authorizer hash (blake2b(encode(Authorizer)))
    sub_type = n(OpaqueHash)
    element_count = auth_queue_size
    
class AuthQueues(FixedLengthArray):
    sub_type = n(AuthQueue)
    element_count = core_count


class WorkPackage(Struct):
    type_mapping = [
        ("authorization", "ByteSequence"),
        ("auth_code_host", "ServiceId"),
        ("authorizer", "Authorizer"),
        ("context", "RefineContext"),
        ("items", "Vec<WorkItem>")
    ]

class AuthorizerOutput(ByteSequence):
    pass

class WorkPackageSpec(Struct):
    type_mapping = [
        ('hash', n(WorkPackageHash)),
        ('length', n(U32)),
        ('erasure_root', 'OpaqueHash'),
        ('exports_root', 'OpaqueHash'),
        ('exports_count', n(U16))
    ]

class RefineContext(Struct):
    type_mapping = [
        ('anchor', 'HeaderHash'),
        ('state_root', 'OpaqueHash'),
        ('beefy_root', 'OpaqueHash'),
        ('lookup_anchor', 'HeaderHash'),
        ('lookup_anchor_slot', 'TimeSlot'),
        ('prerequisites', 'Vec<OpaqueHash>')
    ]

class WorkExecResult(Enum):
    type_mapping = {
        0: ("ok", n(ByteSequence)),
        1: ("out_of_gas", n(Null)),
        2: ("panic", n(Null)),
        3: ("bad_code", n(Null)),
        4: ("code_oversize", n(Null))
    }

class WorkResult(Struct):
    type_mapping = [
        ("service_id", n(ServiceId)),
        ("code_hash", n(OpaqueHash)),
        ("payload_hash", n(OpaqueHash)),
        ("accumulate_gas", n(Gas)),
        ("result", n(WorkExecResult))
    ]

class WorkResults(Vec):
    sub_type = n(WorkResult)

class SegmentRootLookupItem(Struct):
    type_mapping = [
        ("work_package_hash", n(WorkReportHash)),
        ("segment_tree_root", n(SegmentTreeRoot))
    ]

class WorkReport(Struct):
    type_mapping = [
        ('package_spec', n(WorkPackageSpec)),
        ('context', n(RefineContext)),
        ('core_index', n(CoreIndex)),
        ('authorizer_hash', n(OpaqueHash)),
        ('auth_output', n(AuthorizerOutput)),
        ("segment_root_lookup", 'Vec<SegmentRootLookupItem>'),
        ('results', n(WorkResults))
    ]
