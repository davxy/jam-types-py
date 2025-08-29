#!/usr/bin/env python3

from jam_types.fuzzer import Genesis, TraceStep, FuzzerMessage, FuzzerWireMessage, ScaleBytes, FuzzerReport
from jam_types import spec
import json
import argparse
import os
import re
import sys

def convert_to_json(filename, subsystem_type, spec_name = None):
    with open(filename, 'rb') as file:
        blob = file.read()
        scale_bytes = ScaleBytes(blob)
        dump = subsystem_type(data=scale_bytes)
        decoded = dump.decode()
        print(json.dumps(decoded, indent=4))


def main():
    spec.set_spec("tiny")

    type_mapping = {
        'genesis': Genesis,
        'traceStep': TraceStep,
        'message': FuzzerMessage,
        'wireMessage': FuzzerWireMessage,
        'report': FuzzerReport,
    }
    
    parser = argparse.ArgumentParser(description='Decode binary files to JSON', 
                                   formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('filename', help='Binary file to decode')
    type_help = "Type to use for decoding:\n"
    type_help += " * Report: fuzzer report (generally `report.bin`)\n"
    type_help += " * Genesis: trace genesis (generally `genesis.bin`)\n"
    type_help += " * TraceStep: trace step (generally `nnnnnnnn.bin`)\n"
    type_help += " * Message: fuzzer protocol message (with no length prefix)\n"
    type_help += " * WireMessage: fuzzer protocol message (with length prefix)\n"
    
    parser.add_argument('type', nargs='?', choices=type_mapping.keys(), help=type_help)
    
    args = parser.parse_args()
    
    if not args.type:
        # Infer type from filename
        filename = os.path.basename(args.filename)
        if filename == 'report.bin':
            inferred_type = 'Report'
        elif filename == 'genesis.bin':
            inferred_type = 'Genesis'
        elif re.match(r'^\d{8}\.bin$', filename):
            inferred_type = 'TraceStep'
        else:
            inferred_type = 'Message'
        print(f"Warning: No type specified, attempting to decode as {inferred_type} based on filename", file=sys.stderr)
        args.type = inferred_type

    decode_type = type_mapping[args.type]   
    convert_to_json(args.filename, decode_type)

if __name__ == '__main__':
    main()
