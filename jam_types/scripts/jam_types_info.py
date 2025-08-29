#!/usr/bin/env python3
"""
JAM Types information tool.
"""

import argparse
import sys
from jam_types.spec import get_current_spec, SPECS


def main():
    """Display information about jam_types."""
    parser = argparse.ArgumentParser(description="Display jam_types information")
    parser.add_argument("--spec", help="Show information for specific spec")
    args = parser.parse_args()
    
    if args.spec:
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


if __name__ == "__main__":
    main()
