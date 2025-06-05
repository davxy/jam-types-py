import os
import logging

# Spec configurations
SPECS = {
    'full': {
        'validators_count': 1023,
        'epoch_length': 600,
        'max_tickets_per_block': 16,
    },
    'tiny': {
        'validators_count': 6,
        'epoch_length': 12,
        'max_tickets_per_block': 3,
    }
}

# Get spec from environment variable, default to 'tiny'
_current_spec = os.environ.get('JAM_SPEC', 'full').lower()

def set_spec(spec_name):
    """Set the current spec configuration."""
    global _current_spec
    if spec_name not in SPECS:
        raise ValueError(f"Unknown spec: {spec_name}. Available specs: {list(SPECS.keys())}")
    _current_spec = spec_name
    _update_constants()

def get_current_spec():
    """Get the name of the current spec."""
    return _current_spec

def _update_constants():
    """Update all derived constants based on current spec."""
    global validators_count, epoch_length, max_tickets_per_block
    global validators_per_core, core_count, validators_super_majority, avail_bitfield_bytes
    global auth_pool_max_size, auth_queue_size, hash_size
    
    logging.debug("Using JAM spec: %s", _current_spec)
    spec = SPECS[_current_spec]
    
    # Base constants from spec
    validators_count = spec['validators_count']
    epoch_length = spec['epoch_length']
    max_tickets_per_block = spec['max_tickets_per_block']
    
    # Derived constants
    validators_per_core = 3
    core_count = validators_count // validators_per_core
    validators_super_majority = validators_count // 3 * 2 + 1
    avail_bitfield_bytes = (core_count + 7) // 8
    
    # Fixed constants
    auth_pool_max_size = 8
    auth_queue_size = 80
    hash_size = 32

# Initialize constants with current spec
_update_constants()
