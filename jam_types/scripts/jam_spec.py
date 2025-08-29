#!/usr/bin/env python3
"""
JAM specification management tool.
"""

import argparse
import sys
from jam_types.spec import get_current_spec, set_spec, SPECS


def main():
    """Manage JAM specifications."""
    parser = argparse.ArgumentParser(description="Manage JAM specifications")
    parser.add_argument("action", choices=["list", "show", "set"], help="Action to perform")
    parser.add_argument("spec_name", nargs="?", help="Specification name")
    args = parser.parse_args()
    
    if args.action == "list":
        print("Available specifications:")
        for spec_name in SPECS.keys():
            current = " (current)" if spec_name == get_current_spec() else ""
            print(f"  {spec_name}{current}")
    
    elif args.action == "show":
        spec_name = args.spec_name or get_current_spec()
        if spec_name not in SPECS:
            print(f"Error: Unknown spec '{spec_name}'")
            sys.exit(1)
        
        spec_info = SPECS[spec_name]
        print(f"Specification: {spec_name}")
        for key, value in spec_info.items():
            print(f"  {key}: {value}")
    
    elif args.action == "set":
        if not args.spec_name:
            print("Error: spec_name required for 'set' action")
            sys.exit(1)
        
        if args.spec_name not in SPECS:
            print(f"Error: Unknown spec '{args.spec_name}'. Available: {list(SPECS.keys())}")
            sys.exit(1)
        
        set_spec(args.spec_name)
        print(f"Set current spec to: {args.spec_name}")


if __name__ == "__main__":
    main()
