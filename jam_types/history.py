from .simple import Struct, OpaqueHash

class Mmr(Struct):
    type_mapping = [
        ('peaks', 'Vec<Option<OpaqueHash>>')
    ]

class ReportedWorkPackage(Struct):
    type_mapping = [
        ('hash', 'OpaqueHash'),
        # Exported segments root
        ('exports_root', 'OpaqueHash')
    ]

class BlockInfo(Struct):
    type_mapping = [
        ('header_hash', 'OpaqueHash'),
        ('mmr', 'Mmr'),
        ('state_root', 'OpaqueHash'),
        ('reported', 'Vec<ReportedWorkPackage>')
    ]
