
MAJOR_KEYS = [
    "C",
    "G",
    "D",
    "A",
    "E",
    "B",
    "F#",
    "C#",
    "G#",
    "D#",
    "A#",
    "E#"
]

MINOR_KEYS_u = [k+"m" for k in MAJOR_KEYS]
MINOR_KEYS = MINOR_KEYS_u[3:] + MINOR_KEYS_u[:3]


def compare_keys_(prediction_key: str, ground_truth_key: str) -> (int):
    """
    Parameters
    ----------
    prediction_key: string of predicted key
    ground_truth_key: string of ground truth key

    Returns
    -------
    score integer
    """

    if prediction_key in MAJOR_KEYS and ground_truth_key in MAJOR_KEYS:
        pidx = MAJOR_KEYS.index(prediction_key)
        gidx = MAJOR_KEYS.index(ground_truth_key)
        return min((gidx-pidx)%12,(pidx-gidx)%12)
    elif prediction_key in MINOR_KEYS and ground_truth_key in MINOR_KEYS:
        pidx = MINOR_KEYS.index(prediction_key)
        gidx = MINOR_KEYS.index(ground_truth_key)
        return min((gidx-pidx)%12,(pidx-gidx)%12)
    elif prediction_key in MAJOR_KEYS and ground_truth_key in MINOR_KEYS:
        pidx = MAJOR_KEYS.index(prediction_key)
        gidx = MINOR_KEYS.index(ground_truth_key)
        return min((gidx-pidx)%12,(pidx-gidx)%12)+1
    elif prediction_key in MINOR_KEYS and ground_truth_key in MAJOR_KEYS:
        pidx = MINOR_KEYS.index(prediction_key)
        gidx = MAJOR_KEYS.index(ground_truth_key)
        return min((gidx-pidx)%12,(pidx-gidx)%12)+1
    else: 
        raise Exception("input keys need to be in the following format:",MAJOR_KEYS,MINOR_KEYS ) 


