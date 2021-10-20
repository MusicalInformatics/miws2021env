import numpy as np
from sklearn.datasets import make_blobs

def generate_example_sequences(lenX=100, centers=3, n_features=5,
                               maxreps=4, minreps=1, noise_scale=0.01):
    X, _ = make_blobs(n_samples=lenX, centers=centers,
                      n_features=n_features)
    n_reps = np.random.randint(minreps, maxreps, len(X))
    y_idxs = [rp * [i] for i, rp in enumerate(n_reps)]
    y_idxs = np.array([el for reps in y_idxs for el in reps], dtype=int)
    Y = X[y_idxs] + 10 * np.random.randn()
    # add some noise
    Y += noise_scale * np.random.randn(*Y.shape)
    ground_truth_path = np.column_stack((y_idxs, np.arange(len(Y))))
    return X, Y, ground_truth_path
