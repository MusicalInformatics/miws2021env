import partitura as pt

def addnote(midipitch, part, voice, start, end, idx):
    """
    adds a single note by midiptich to a part
    """
    offset = midipitch%12
    octave = int(midipitch-offset)/12
    name = [("C",0),
            ("C",1),
            ("D",0),
            ("D",1),
            ("E",0),
            ("F",0),
            ("F",1),
            ("G",0),
            ("G",1),
            ("A",0),
            ("A",1),
            ("B",0)]
    # print( id, start, end, offset)
    step, alter = name[int(offset)]
    part.add(pt.score.Note(id='n{}'.format(idx), step=step, 
                        octave=int(octave), alter=alter, voice=voice), 
                        start=start, end=end)


def partFromProgression(prog, quarter_duration = 4 ):
    part = pt.score.Part('P0', 'part from progression', quarter_duration=quarter_duration)
    for i, c in enumerate(prog.chords):
        for j, pitch in enumerate(c.pitches):
            addnote(pitch, part, j, i*quarter_duration, (i+1)*quarter_duration, str(j)+str(i))
    
    return part