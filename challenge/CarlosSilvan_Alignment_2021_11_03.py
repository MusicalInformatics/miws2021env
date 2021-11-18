#!/usr/bin/env python
# -*- coding: utf-8 -*-

# single script challenge submission template

if __name__ == "__main__":

    import argparse
    import os
    import partitura as pt

    parser = argparse.ArgumentParser(description="Test NW Matcher")
    parser.add_argument(
        "--matchfile",
        "-i",
        help="path to the match input file",
        default="",
        type=str
    )
    parser.add_argument(
        "--outdir",
        "-o",
        help="Output text file directory",
        type=str,
        default="."
    )
    args = parser.parse_args()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    match_name = os.path.splitext(os.path.basename(args.matchfile))[0]

    # replace the dummy with your computation
    DUMMY_performedpart, DUMMY_alignment, DUMMY_part = pt.load_match(
        os.path.join(
            "..",
            "introduction",
            "example_data",
            "Chopin_op10_no3_p01.match"
        ),
        create_part=True,
    )

    outfile = os.path.join(
        args.outdir,
        f"{script_name}_{match_name}_results.match"
    )

    pt.save_match(
        alignment=DUMMY_alignment,
        ppart=DUMMY_performedpart,
        spart=DUMMY_part,
        out=outfile,
    )
