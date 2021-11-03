#!/usr/bin/env python
# -*- coding: utf-8 -*-

# single script challenge submission template

if __name__ == "__main__":
    
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Test NW Matcher')
    parser.add_argument('--MIDIfile', '-i',
                        help='path to MIDI input file',
                        default="",
                        type=str)    
    parser.add_argument('--outdir', '-o',
                        help='Output text file directory',
                        type=str,
                        default=".")
    args = parser.parse_args()


    script_name = os.path.basename(__file__).split(".")[0]
    midi_name = os.path.basename(args.MIDIfile).split(".")[0]
    DUMMY_KEY = "A"     # from the list of 24 key signatures

    with open(os.path.join(args.outdir, script_name+"_"+ midi_name+ "_results.txt"), "w") as f:
        f.write(str(DUMMY_KEY))