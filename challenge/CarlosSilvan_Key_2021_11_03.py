#!/usr/bin/env python
# -*- coding: utf-8 -*-

# single script challenge submission template

if __name__ == "__main__":

    import argparse
    import os

    parser = argparse.ArgumentParser(description='Test Key Estimation')
    parser.add_argument('--MIDIfile', '-i',
                        help='path to MIDI input file',
                        default="",
                        type=str)
    parser.add_argument('--outdir', '-o',
                        help='Output text file directory',
                        type=str,
                        default=".")
    args = parser.parse_args()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    midi_name = os.path.splitext(os.path.basename(args.MIDIfile))[0]
    DUMMY_KEY = "A"     # from the list of 24 key signatures

    outfile = os.path.join(
        args.outdir,
        f"{script_name}_{midi_name}_results.txt"
    )

    with open(outfile, "w") as f:
        f.write(str(DUMMY_KEY))
