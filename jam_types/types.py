from scalecodec import (
    U8,
    U32,
    BoundedVec,
    Enum,
    FixedLengthArray,
    Struct,
    Vec,
)

from .const import (
    avail_bitfield_bytes,
    core_count,
    epoch_length,
    validators_count,
    validators_super_majority,
)
from .simple import *
from .simple import OpaqueHash, TimeSlot, ServiceId, n
from .work import WorkReport

#
# Disputes
# 

class Disputes(Struct):
    type_mapping = [
        # Good verdicts sequence
        ('good', 'Vec<WorkReportHash>'),
        # Bad verdicts sequence
        ('bad', 'Vec<WorkReportHash>'),
        # Wonky verdicts sequence
        ('wonky', 'Vec<WorkReportHash>'),
        # Offenders sequence
        ('offenders', 'Vec<WorkReportHash>')
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
        ('report', n(WorkReport)),
        ('timeout', n(TimeSlot))
    ]

class AvailabilityAssignments(FixedLengthArray):
    sub_type = 'Option<AvailabilityAssignment>'
    element_count = core_count

#
# Statistics
#

class ValActivityRecord(Struct):
    type_mapping = [
        ("blocks", n(U32)),
        ("tickets", n(U32)),
        ("pre_images", n(U32)),
        ("pre_images_size", n(U32)),
        ("guarantees", n(U32)),
        ("assurances", n(U32)),
    ]

class ValActivityRecords(FixedLengthArray):
    sub_type = n(ValActivityRecord)
    element_count = validators_count

class CoreActivityRecord(Struct):
    pass
    
class CoresStatistics(FixedLengthArray):
    sub_type = n(CoreActivityRecord)
    element_count = core_count

class ServiceActivityRecord(Struct):
    pass

class ServicesStatisticsMapEntry(Struct):
    type_maping = [
        ("service_id", n(ServiceId)),
        ("record", n(ServiceActivityRecord))
    ]

class ServicesStatistics(Vec):
    sub_type = n(ServicesStatisticsMapEntry)

class Statistics(Struct):
    type_mapping = [
        ("vals_current", n(ValActivityRecords)),
        ("vals_last", n(ValActivityRecords)),
    	("cores", n(CoresStatistics)),
    	("services", n(ServicesStatistics)),
    ]

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

class TicketsBodies(FixedLengthArray):
    sub_type = n(TicketBody)
    element_count = epoch_length

class TicketsAccumulator(BoundedVec):
    sub_type = n(TicketBody)
    max_elements = epoch_length

class EpochKeys(FixedLengthArray):
    sub_type = 'BandersnatchPublic'
    element_count = epoch_length

class TicketsOrKeys(Enum):
    type_mapping = {
        0: ('tickets', n(TicketsBodies)),
        1: ('keys', n(EpochKeys))
    }

#
# Guarantees
#

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

#
# Services
#
 
class ServiceInfo(Struct):
    type_mapping = [
        ('code_hash', 'OpaqueHash'),
        ('balance', 'U64'),
        ('min_item_gas', 'Gas'),
        ('min_memo_gas', 'Gas'),
        ('bytes', 'U64'),
        ('items', 'U32')
    ]

class AlwaysAccumulateMapItem(Struct):
    type_mapping = [
        ('id', n(ServiceId)),
        ('gas', n(Gas)),
    ]

class Privileges(Struct):
    type_mapping = [
        ('bless', n(ServiceId)),
        ('assign', n(ServiceId)),
        ('designate', n(ServiceId)),
        ('always_acc', "Vec<AlwaysAccumulateMapItem>"),
    ]
