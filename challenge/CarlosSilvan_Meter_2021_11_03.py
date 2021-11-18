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

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    midi_name = os.path.splitext(os.path.basename(args.MIDIfile))[0]
    DUMMY_METER = 3     # from 2, 3, 4
    DUMMY_TEMPO = 100   # global average tempo in beats per minute

    outfile = os.path.join(
        args.outdir,
        f"{script_name}_{midi_name}_results.txt"
    )
    with open(outfile, "w") as f:
        f.write(str(DUMMY_METER)+"\n")
        f.write(str(DUMMY_TEMPO))
