import numpy as np
import partitura

from scipy.stats import mode

from hmm import HMM, ConstantTransitionModel, ObservationModel
from key_profiles import build_key_profile_matrix, KEYS


class KeyProfileObservationModel(ObservationModel):
    """
    Use Key Profiles (pitch class distributions) for computing
    observation probabilities.

    Parameters
    ----------
    key_profile_matrix: {'kp', 'kk' 'cbms'}
       Empirical pitch class distributions (see definition
        in `key_profiles.py`)
    """
    def __init__(self, key_profile_matrix="kp"):
        super().__init__()
        if isinstance(key_profile_matrix, str):
            self.key_profile_matrix = build_key_profile_matrix(
                key_profile_matrix
            )
        elif isinstance(key_profile_matrix, np.ndarray):
            assert key_profile_matrix.shape == (24, 12)
            self.key_profile_matrix = key_profile_matrix

    def __call__(self, observation):

        if not self.use_log_probabilities:
            p_obs_given_key = np.array(
                [
                    np.prod((kp ** observation) *
                            (1 - kp) ** (1 - observation))
                    for kp in self.key_profile_matrix
                ]
            )
            return p_obs_given_key
        elif self.use_log_probabilities:

            log_p_obs_given_key = np.array(
                [
                    np.sum(
                        (
                            observation * np.log(kp + 1e-10)
                            + np.log1p(-(kp + 1e-10)) * (1 - observation)
                        )
                    )
                    for kp in self.key_profile_matrix
                ]
            )
            return log_p_obs_given_key


def compute_transition_probabilities(inertia_param=0.8):
    """
    Matrix of transition probabilities

    Parameters
    ----------
    intertia_param : float
        Parameter between 0 and 1 indicating how likely it is that
        we will stay on the same key

    Notes
    -----
    * This is a very naive assumption, but so you should definitely explore
    other transition probabilities
    """
    modulation_prob = (1 - inertia_param) / 23.0
    A = modulation_prob * (np.ones(24) - np.eye(24)) \
        + inertia_param * np.eye(24)

    return A


def key_identification(
    fn,
    key_profiles="kp",
    inertia_param=0.8,
    piano_roll_resolution=16,
    win_size=2,
    debug=False,
):
    """
    Temperley's Probabilistic Key Identification

    Parameters
    ----------
    fn : filename
        MIDI file
    key_profiles: {"kp", "kk", "cbms"}
        Key profiles to use in the KeyProfileObservationModel
        (see definition in `key_profiles.py`)
    intertia_param: float
        Parameter between 0 and 1 indicating how likely it is that
        we will stay on the same key
    piano_roll_resolution: int
        Resolution of the piano roll (i.e., how many cells per second)
    win_size: float
        Window size in seconds

    Returns
    -------
    key : str
        The estimated key of the piece
    log_lik:
        The log-likelihood of the estimated key
    """
    # build observation model
    observation_model = KeyProfileObservationModel(
        key_profile_matrix=key_profiles
    )

    # Compute transition model
    transition_probabilities = compute_transition_probabilities(
        inertia_param=inertia_param
    )
    transition_model = ConstantTransitionModel(transition_probabilities)

    hmm = HMM(
        observation_model=observation_model,
        transition_model=transition_model
    )
    # Load score
    ppart = partitura.load_performance_midi(fn)
    # note_array = ppart.note_array

    # Compute piano roll
    piano_roll = partitura.utils.compute_pianoroll(
        ppart, time_div=piano_roll_resolution
    ).toarray()

    # Number of windows in the piano roll
    n_windows = int(
        np.ceil(piano_roll.shape[1] / (piano_roll_resolution * win_size))
    )

    # window size in cells
    window_size = win_size * piano_roll_resolution

    # Constuct observations (these are non-overlapping windows,
    # but you can test other possibilities)
    observations = np.zeros((n_windows, 12))
    for win in range(n_windows):
        idx = slice(win * window_size, (win + 1) * window_size)
        segment = piano_roll[:, idx].sum(1)
        dist = np.zeros(12)
        pitch_idxs = np.where(segment != 0)[0]
        for pix in pitch_idxs:
            dist[pix % 12] += segment[pix]
        # Normalize pitch class distribution
        if dist.sum() > 0:
            # avoid NaN for empty segments
            dist /= dist.sum()

        observations[win] = dist

    # Compute the sequence
    path, log_lik = hmm.find_best_sequence(observations)

    key_idx = int(mode(path).mode[0])

    key = KEYS[key_idx]

    return key, log_lik


def wtc_num_to_key(i):
    mode_idx = np.mod(np.mod(i, 48) // 2, 2)
    if mode_idx == 0:
        wtc_key = KEYS[np.mod(i, 48) // 4]
    else:
        wtc_key = KEYS[np.mod(i, 48) // 4 + 12]
    return wtc_key
