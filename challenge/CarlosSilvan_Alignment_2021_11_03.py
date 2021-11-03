#!/usr/bin/env python
# -*- coding: utf-8 -*-

# single script challenge submission template

if __name__ == "__main__":
    
    import argparse
    import os
    import partitura as pt

    parser = argparse.ArgumentParser(description='Test NW Matcher')
    parser.add_argument('--MIDIfile', '-i',
                        help='path to MIDI input file',
                        default="",
                        type=str)    
    parser.add_argument('--XMLfile', '-x',
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
    xml_name = os.path.basename(args.XMLfile).split(".")[0]
    
    # replace the dummy with your computation
    DUMMY_performedpart, DUMMY_alignment, DUMMY_part = \
        pt.load_match(os.path.join("..","introduction","example_data","Chopin_op10_no3_p01.match"), create_part = True)


    pt.save_match(DUMMY_alignment, DUMMY_performedpart, DUMMY_part, 
        os.path.join(args.outdir, script_name+"_"+ midi_name + xml_name + "_results.match"))
 