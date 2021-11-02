"""
Helper methods
"""
import numpy as np
from sklearn.datasets import make_blobs

# Define random state for reproducibility
RNG = np.random.RandomState(1984)

def generate_example_sequences(lenX=100, centers=3, n_features=5,
                               maxreps=4, minreps=1, noise_scale=0.01):
    """
    Generates example pairs of related sequences. Sequence X are samples of
    an K-dimensional space around a specified number of centroids.
    Sequence Y is a non-constant "time-streched" version of X with some noise added.
    
    Parameters
    ----------
    lenX : int
        Number of elements in the X sequence
    centers: int
        Number of different centers ("classes") that the elements
        of the sequences represent
    n_features: int
        Dimensionality of the features ($K$) in the notation of the
        Notebook
    noise_scale: float
        Scale of the noise
        
    Returns
    -------
    X : np.ndarray
        Sequence X (a matrix where each row represents an element of the sequence)
    Y: np.ndarray
        Sequence Y
    ground_truth_path: np.ndarray
        Alignment between X and Y
    """ 
    
    X, _ = make_blobs(n_samples=lenX, centers=centers,
                      n_features=n_features)
    # Time stretching X! each element in sequence X is repeated a random number of times
    # and then we add some noise to spice things up :)
    n_reps = RNG.randint(minreps, maxreps, len(X))
    y_idxs = [rp * [i] for i, rp in enumerate(n_reps)]
    y_idxs = np.array([el for reps in y_idxs for el in reps], dtype=int)
    # Add a bias, so that Y has a different "scaling" than X
    Y = X[y_idxs] + 10 * RNG.randn()
    # add some noise
    Y += noise_scale * RNG.randn(*Y.shape)
    ground_truth_path = np.column_stack((y_idxs, np.arange(len(Y))))
    return X, Y, ground_truth_path
