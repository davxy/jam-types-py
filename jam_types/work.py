from .const import core_count
from .simple import *
from .simple import (
    U32,
    CoreIndex,
    Enum,
    FixedLengthArray,
    Null,
    OpaqueHash,
    ServiceId,
    Struct,
    Vec,
    Gas,
    ByteSequence,
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
        ("gas_limit", "Gas"),
        ("import_segments", "Vec<ImportSpec>"),
        ("extrinsic", "Vec<ExtrinsicSpec>"),
        ("export_count", "U16")
    ]

class AuthPool(Vec):
    # Authorizer hash (blake2b(encode(Authorizer)))
    sub_type = n(OpaqueHash)

class AuthPools(FixedLengthArray):
    sub_type = n(AuthPool)
    element_count = core_count

class Authorizer(Struct):
    type_mapping = [
        ("code_hash", "OpaqueHash"),
        ("params", "ByteSequence")
    ]

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
        ('exports_root', 'OpaqueHash')
    ]

class RefineContext(Struct):
    type_mapping = [
        ('anchor', 'HeaderHash'),
        ('state_root', 'OpaqueHash'),
        ('beefy_root', 'OpaqueHash'),
        ('lookup_anchor', 'HeaderHash'),
        ('lookup_anchor_slot', 'TimeSlot'),
        ('prerequisite', 'Option<OpaqueHash>')
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
        ("gas", n(Gas)),
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
        ('package_spec', 'WorkPackageSpec'),
        ('context', 'RefineContext'),
        ('core_index', n(CoreIndex)),
        ('authorizer_hash', n(OpaqueHash)),
        ('auth_output', n(AuthorizerOutput)),
        ("segment_root_lookup", 'Vec<SegmentRootLookupItem>'),
        ('results', n(WorkResults))
    ]
