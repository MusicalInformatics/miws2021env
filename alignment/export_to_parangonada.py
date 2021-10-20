import partitura
import pandas as pd
import numpy as np
import os


def save_csv_for_parangonada(outdir, part, ppart, align, zalign=None, feature = None):

    part = partitura.utils.music.ensure_notearray(part)
    ppart = partitura.utils.music.ensure_notearray(ppart)

        # ___ create np array for features
    ffields = [('velocity', '<f4'),
               ('timing', '<f4'),
               ('articulation', '<f4'),
               ('id', 'U256')]
    """ for all dicts create an appropriate entry in an array: match = 0, deletion  = 1, insertion = 2 """
    farray = []
    notes = list(part["id"])
    if feature is not None:
        # veloctiy, timing, articulation, note
        for no, i in enumerate(list(feature['id'])):    
            farray.append((feature['velocity'][no],feature['timing'][no],feature['articulation'][no], i))
    else:
        for no, i in enumerate(notes):     
            farray.append((0,0,0, i))

    featurearray = np.array(farray, dtype=ffields)

    #___ create np array for alignment
    fields = [('idx', 'i4'),
              ('matchtype', 'U256'),
              ('partid', 'U256'),
              ('ppartid', 'U256')]
    """ for all dicts create an appropriate entry in an array: match = 0, deletion  = 1, insertion = 2 """
    array = []
    for no, i in enumerate(align):
        #print(no, i)
        if i["label"]=="match":       
            array.append((no, "0", i["score_id"], str(i["performance_id"])))
        elif i["label"]=="insertion":
            array.append((no, "2", "undefined", str(i["performance_id"])))
        elif i["label"]=="deletion":
            array.append((no, "1", i["score_id"], "undefined"))

    alignarray = np.array(array, dtype=fields)

    """ for all dicts create an appropriate entry in an array: match = 0, deletion  = 1, insertion = 2 """
    zarray = []
    if zalign is not None: 
        for no, i in enumerate(zalign):
            #print(no, i)
            if i["label"]=="match":       
                zarray.append((no, "0", i["score_id"], str(i["performance_id"])))
            elif i["label"]=="insertion":
                zarray.append((no, "2", "undefined", str(i["performance_id"])))
            elif i["label"]=="deletion":
                zarray.append((no, "1", i["score_id"], "undefined"))
    else: # if no zalign is available, save the same alignment twice
        for no, i in enumerate(align):
            #print(no, i)
            if i["label"]=="match":       
                zarray.append((no, "0", i["score_id"], str(i["performance_id"])))
            elif i["label"]=="insertion":
                zarray.append((no, "2", "undefined", str(i["performance_id"])))
            elif i["label"]=="deletion":
                zarray.append((no, "1", i["score_id"], "undefined"))

    zalignarray = np.array(zarray, dtype=fields)

    pd.DataFrame(ppart).to_csv(outdir + os.path.sep+"ppart.csv", index= 0)
    pd.DataFrame(part).to_csv(outdir + os.path.sep+"part.csv", index= 0)  
    pd.DataFrame(alignarray).to_csv(outdir + os.path.sep+"align.csv", index= 0)  
    pd.DataFrame(zalignarray).to_csv(outdir + os.path.sep+"zalign.csv", index= 0)  
    pd.DataFrame(featurearray).to_csv(outdir + os.path.sep+"feature.csv", index= 0) 
    # np.savetxt(outdir + os.path.sep+"ppart.csv", ppart, delimiter= ",")
    # np.savetxt(outdir + os.path.sep+"part.csv", part, delimiter= ",")
    # np.savetxt(outdir + os.path.sep+"align.csv", alignarray, delimiter= ",")
    # np.savetxt(outdir + os.path.sep+"zalign.csv",zalignarray,  delimiter= ",")
    # np.savetxt(featurearray).to_csv(outdir + os.path.sep+"feature.csv",featurearray,  delimiter= ",")