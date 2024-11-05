from scalecodec import (
    U8,
    Enum,
    FixedLengthArray,
    Null,
    Struct,
    Vec,
)

from .const import (
    avail_bitfield_bytes,
    epoch_length,
    core_count,
    validators_count,
    validators_super_majority,
)
from .simple import *
from .simple import n
from .block import TicketsMark

#
# Disputes
# 

class Disputes(Struct):
    type_mapping = [
        # Good verdicts sequence
        ('psi_g', 'Vec<WorkReportHash>'),
        # Bad verdicts sequence
        ('psi_b', 'Vec<WorkReportHash>'),
        # Wonky verdicts sequence
        ('psi_w', 'Vec<WorkReportHash>'),
        # Offenders sequence
        ('psi_o', 'Vec<WorkReportHash>')
    ]

##
# Validator Data
##
 
class ValidatorMetadata(ByteArray):
    element_count = 128

class ValidatorData(Struct):
    type_mapping = [
        ("bandersnatch", 'BandersnatchPublic'),
        ("ed25519", 'Ed25519Public'),
        ("bls", 'BlsPublic'),
        ("metadata", 'ValidatorMetadata')
    ]

class ValidatorsData(FixedLengthArray):
    sub_type = 'ValidatorData'
    element_count = validators_count

#
# Availability Assigments
# 

class AvailabilityAssignment(Struct):
    type_mapping = [
        # TODO
        ('dummy_work_report', '[u8; 354]'),
        ('timeout', 'TimeSlot')
    ]

class AvailabilityAssignments(FixedLengthArray):
    sub_type = 'Option<AvailabilityAssignment>'
    element_count = core_count

#
# Misc
# 

class AvailAssurance(Struct):
    type_mapping = [
        ("anchor", "OpaqueHash"),
        ("bitfield", f"[U8; {avail_bitfield_bytes}]"),
        ("validator_index", "U16"),
        ("signature", "Ed25519Signature")
    ]

class Preimage(Struct):
    type_mapping = [
        ("requester", "ServiceId"),
        ("blob", "ByteSequence")
    ]

class Culprit(Struct):
    type_mapping = [
        ("target", "WorkReportHash"),
        ("key", "Ed25519Public"),
        ("signature", "Ed25519Signature")
    ]

class Fault(Struct):
    type_mapping = [
        ("target", "WorkReportHash"),
        ("vote", "Bool"),
        ("key", "Ed25519Public"),
        ("signature", "Ed25519Signature")
    ]

class Judgement(Struct):
    type_mapping = [
        ("vote", "Bool"),
        ("index", "ValidatorIndex"),
        ("signature", "Ed25519Signature")
    ]

class Judgements(FixedLengthArray):
    sub_type = 'Judgement'
    element_count = validators_super_majority
    
class Verdict(Struct):
    type_mapping = [
        ("target", "WorkReportHash"),
        ("age", "EpochIndex"),
        ("votes", "Judgements")
    ]

#
# Tickets
#
 
class TicketId(OpaqueHash):
    pass

class TicketAttempt(U8):
    pass

class TicketBody(Struct):
    type_mapping = [
        ('id', 'TicketId'),
        ('attempt', 'TicketAttempt')
    ]

class TicketEnvelope(Struct):
    type_mapping = [
        ("attempt", "TicketAttempt"),
        ("signature", "BandersnatchRingVrfSignature")
    ]

class TicketsBodies(TicketsMark):
    pass

class EpochKeys(FixedLengthArray):
    sub_type = 'BandersnatchPublic'
    element_count = epoch_length

class TicketsOrKeys(Enum):
    type_mapping = {
        0: ('tickets', 'TicketsBodies'),
        1: ('keys', 'EpochKeys')
    }

###
# Work Package
###
 
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
        ('hash', 'OpaqueHash'),
        ('length', 'u32'),
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
        ("work_package_hash", "OpaqueHash"),
        ("segment_tree_root", "OpaqueHash")
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

class GuaranteeSignature(Struct):
    type_mapping = [
        ('validator_index', 'ValidatorIndex'),
        ('signature', 'Ed25519Signature')
    ]

class GuaranteeSignatures(Vec):
    sub_type = 'GuaranteeSignature'

class ReportGuarantee(Struct):
    type_mapping = [
        ('report', 'WorkReport'),
        ('slot', 'TimeSlot'),
        ('signatures', 'GuaranteeSignatures')
    ]
