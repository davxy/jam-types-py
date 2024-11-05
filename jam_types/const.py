# Full Spec
# validators_count = 1023
# epoch_length = 600

# Tiny Spec
validators_count = 6
epoch_length = 12

validators_per_core = 3

core_count = validators_count // validators_per_core

validators_super_majority = validators_count // 3 * 2 + 1
avail_bitfield_bytes = (core_count + 7) // 8

hash_size = 32

max_tickets_per_block = 16
