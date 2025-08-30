#!/usr/bin/env python3
"""
JAM Types information tool.
"""

import argparse
import sys
import inspect
from jam_types.spec import get_current_spec, SPECS
import jam_types.block
import jam_types.crypto
import jam_types.fuzzer
import jam_types.history
import jam_types.simple
import jam_types.types
import jam_types.work

def get_all_types():
    """Get all types defined in jam_types modules."""
    modules = [
        jam_types.block,
        jam_types.crypto,
        jam_types.fuzzer,
        jam_types.history,
        jam_types.simple,
        jam_types.types,
        jam_types.work
    ]
    
    all_types = {}
    for module in modules:
        module_name = module.__name__.split('.')[-1]
        types_in_module = []
        
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__ == module.__name__:
                types_in_module.append(name)
        
        if types_in_module:
            all_types[module_name] = sorted(types_in_module)
    
    return all_types

def main():
    """Display information about jam_types."""
    parser = argparse.ArgumentParser(description="Display jam_types information")
    parser.add_argument("--spec", help="Show information for specific spec")
    parser.add_argument("--types", action="store_true", help="Show all defined types")
    args = parser.parse_args()
    
    if args.types:
        all_types = get_all_types()
        print("All types defined in jam_types modules:")
        for module_name, types_list in all_types.items():
            print(f"\n{module_name}:")
            for type_name in types_list:
                print(f"  {type_name}")
    elif args.spec:
        if args.spec not in SPECS:
            print(f"Error: Unknown spec '{args.spec}'. Available specs: {list(SPECS.keys())}")
            sys.exit(1)
        spec_info = SPECS[args.spec]
        print(f"Spec: {args.spec}")
        for key, value in spec_info.items():
            print(f"  {key}: {value}")
    else:
        current_spec = get_current_spec()
        print(f"Current spec: {current_spec}")
        print(f"Available specs: {list(SPECS.keys())}")
        print("\nUse --types to see all defined types")


if __name__ == "__main__":
    main()
