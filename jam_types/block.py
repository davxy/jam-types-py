from scalecodec import BoundedVec, FixedLengthArray, Struct, Vec

from .const import epoch_length, validators_count, max_tickets_per_block
from .types import Preimage, TicketBody
from .utils import class_name as n

#
# Header
#

class TicketsMark(FixedLengthArray):
    sub_type = n(TicketBody)
    element_count = epoch_length

class EpochMark(Struct):
    type_mapping = [
        ('entropy', 'OpaqueHash'),
        ('tickets_entropy', 'OpaqueHash'),
        ('validators', f'[BandersnatchPublic; {validators_count}]')
    ]

class OffendersMark(Struct):
    type_mapping = [
        # Offenders marker (H_o)
        ('offenders_mark', 'Vec<Ed25519Public>')
    ]

class Header(Struct):
    type_mapping = [
        ("parent", "OpaqueHash"),
        ("parent_state_root", "OpaqueHash"),
        ("extrinsic_hash", "OpaqueHash"),
        ("slot", "TimeSlot"),
        ("epoch_mark", "Option<EpochMark>"),
        ("tickets_mark", "Option<TicketsMark>"),
        ("offenders_mark", "Vec<Ed25519Public>"),
        ("author_index", "U16"),
        ("entropy_source", "BandersnatchVrfSignature"),
        ("seal", "BandersnatchVrfSignature")
    ]

#
# Extrinsic
#
 
class TicketsXt(BoundedVec):
    sub_type = "TicketEnvelope"
    max_elements = max_tickets_per_block

class DisputesXt(Struct):
    type_mapping = [
        ("verdicts", "Vec<Verdict>"),
        ("culprits", "Vec<Culprit>"),
        ("faults", "Vec<Fault>")
    ]

class PreimagesXt(Vec):
    sub_type = n(Preimage)

class AssurancesXt(Vec):
    sub_type = "AvailAssurance"

class GuaranteesXt(Vec):
    sub_type = 'ReportGuarantee'

class Extrinsic(Struct):
    type_mapping = [
        ("tickets", "TicketsXt"),
        ("preimages", "PreimagesXt"),
        ("guarantees", "GuaranteesXt"),
        ("assurances", "AssurancesXt"),
        ("disputes", "DisputesXt")
    ]

#
# Block
#

class Block(Struct):
    type_mapping = [
        ("header", "Header"),
        ("extrinsic", "Extrinsic")
    ]
