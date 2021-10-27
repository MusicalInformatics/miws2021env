import numpy as np
import copy


def reflect(chord, point=0):
    base = chord[0]
    new_base = ((point + 7) - base) % 12
    if len(chord) > 1:
        rel_from_base = [(n - base) for n in chord[1:]]
        inv_rel = [(-rel)%12 for rel in rel_from_base]
        neg_chord = [new_base] + list(map(lambda x : (x + new_base)%12, inv_rel))
    else:
        neg_chord = [new_base]
    return neg_chord


def negative_harmony(note_array, point=0):
    na = copy.copy(note_array)
    for onset in np.unique(na["onset_beat"]):
        plist = na[np.where(na["onset_beat"] == onset)]["pitch"]
        pm = list(map(lambda y : (y%12, int(y/12)), plist))
        pc, mapping = zip(*pm)
        new_pc = reflect(chord=pc, point=point)
        new_pitches = [a + b*12 for a, b in zip(new_pc, mapping)]
        for i, index in enumerate(np.where(na["onset_beat"] == onset)[0]):
            na["pitch"][index] = new_pitches[i]
    return na


if __name__=="__main__":
    import partitura
    import os
    sfn = os.path.join(os.path.dirname(__file__), "samples", "Exercise_01.musicxml")
    part = partitura.load_musicxml(sfn)
    part = partitura.load_musicxml(partitura.EXAMPLE_MUSICXML)
    note_array = partitura.utils.ensure_notearray(part)
    print(note_array["pitch"])
    print(negative_harmony(note_array)["pitch"])

