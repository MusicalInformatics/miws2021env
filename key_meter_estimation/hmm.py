# -*- coding: utf-8 -*-
"""
Hidden Markov Models

This module contains case classes to define Hidden Markov Models.
"""
import numpy as np
from collections import defaultdict


class TransitionModel(object):
    """
    Base class for implementing a Transition Model
    """
    def __init__(self, use_log_probabilities=True):
        self.use_log_probabilities = use_log_probabilities

    def __call__(self, i=None, j=None, *args, **kwargs):
        raise NotImplementedError


class ObservationModel(object):
    """
    Base class for implementing an Observation Model
    """
    def __init__(self, use_log_probabilities=True):
        self.use_log_probabilities = use_log_probabilities

    def __call__(self, observation, *args, **kwargs):
        raise NotImplementedError()


class HiddenMarkovModel(object):
    """
    Hidden Markov Model

    Parameters
    ----------
    observation_model : ObservationModel
        A model for computiong the observation (emission) probabilities.
    transition_model: TransitionModel
        A model for computing the transition probabilities.
    state_space: iterable (optional)
        Labels of the states (e.g., a list of strings containing
        the names of each state).

    Attributes
    ----------
    observation_model: ObservationModel
    transition_model: TransitionModel
    n_states: int
        Number of states
    state_space: np.array
    """

    def __init__(self, observation_model,
                 transition_model, state_space=None):

        self.observation_model = observation_model
        self.transition_model = transition_model
        self.n_states = self.transition_model.n_states
        if state_space is not None:
            self.state_space = np.asarray(state_space)
        else:
            self.state_space = np.arange(self.n_states)

    def find_best_sequence(self, observations, log_probabilities=True):
        best_sequence, sequence_likelihood = viterbi_algorithm(
            hmm=self,
            observations=observations,
            log_probabilities=log_probabilities)
        return best_sequence, sequence_likelihood


# alias
HMM = HiddenMarkovModel


def viterbi_algorithm(hmm, observations, log_probabilities=True):
    """
    Find the most probable sequence of latent variables given
    a sequence of observations

    Parameters
    ----------
    observations: iterable
       An iterable containing observations. The type of each
       element depends on input types accepted by the
       `hmm.observation_model`
    log_probabilities: Bool (optional)
       If True, uses log probabilities to compute the Viterbi
       recursion (better for numerical stability). Default is True.

    Returns
    -------
    path: np.ndarray
        The most probable sequence of latent variables
    likelihood: float
        The likelihood (either the probability or the
        log proability if `log_probabilities` is True)
        of the best sequence.
    """
    # Set whether to use log probabilities in transition and
    # observation models
    hmm.transition_model.use_log_probabilities = log_probabilities
    hmm.observation_model.use_log_probabilities = log_probabilities
    # Initialize matrix for holding the best sub-sequence
    # (log-)likelihood
    omega = np.zeros((len(observations), hmm.n_states))
    # Initialize dictionary for tracking the best paths
    path = defaultdict(lambda: list())

    # Initiate for i == 0
    obs_prob = hmm.observation_model(observations[0])

    if log_probabilities:
        omega[0, :] = obs_prob + hmm.transition_model.init_distribution
    else:
        omega[0, :] = obs_prob * hmm.transition_model.init_distribution

    # Initialize path
    for i in range(hmm.n_states):
        path[i].append(i)

    # Viterbi recursion
    for i, obs in enumerate(observations[1:], 1):
        obs_prob = hmm.observation_model(obs)
        for j in range(hmm.n_states):
            if log_probabilities:
                prob, state = max(
                    [(omega[i - 1, k] + hmm.transition_model(k, j), k)
                     for k in range(hmm.n_states)],
                    key=lambda x: x[0]
                )
                omega[i, j] = obs_prob[j] + prob

            else:
                prob, state = max(
                    [(omega[i - 1, k] * hmm.transition_model(k, j), k)
                     for k in range(hmm.n_states)],
                    key=lambda x: x[0]
                )
                omega[i, j] = obs_prob[j] * prob
            # keep track of the best state
            path[j].append(state)

    # Get index of the best state
    best_sequence_idx = omega[-1, :].argmax()
    # Get best path (backtracking!)
    best_sequence = np.array(path[best_sequence_idx][::-1], dtype=int)
    if hmm.state_space is not None:
        best_sequence = hmm.state_space[best_sequence]
    # likelihood of the path
    path_likelihood = omega[-1, best_sequence_idx]

    return best_sequence, path_likelihood


class ConstantTransitionModel(object):
    """
    Constant Transition Model

    This transition model represents the case were the
    transition proabilities do not change over time (i.e.,
    they are static). In this case, the transition probabilities
    can be represented by a transition matrix

    Parameters
    ----------
    transition_probabilities: np.ndarray
        A (n_states, n_states) matrix where component
        [i, j] represents the probability of going to state j
        coming from state i.
    init_distribution: np.ndarray or None (optional)
        A 1D vector of length n_states defining the initial
        probabilities of each state
    normalize_init_distribution: Bool (optional)
        If True, the initial distribution will be normalized.
        Default is False.
    use_log_probabilities: Bool (optional)
        If True, use log proabilities instead of norm proabilities
        (better for numerical stability)
    """

    def __init__(
            self,
            transition_probabilities,
            init_distribution=None,
            normalize_init_distribution=False,
            normalize_transition_probabilities=False,
            use_log_probabilities=True
    ):
        super().__init__()
        self.use_log_probabilities = use_log_probabilities
        self.transition_probabilities = transition_probabilities
        self.n_states = len(transition_probabilities)

        if init_distribution is None:
            self.init_distribution = (
                1.0 / float(self.n_states) *
                np.ones(self.n_states, dtype=float)
            )
        else:
            self.init_distribution = init_distribution

        if normalize_init_distribution:
            # Normalize initial distribution
            self.init_distribution /= np.maximum(
                np.sum(self.init_distribution), 1e-10
            )

        if normalize_transition_probabilities:
            self.transition_probabilities /= np.sum(
                self.transition_probabilities, 1,
                keepdims=True
            )

    @property
    def init_distribution(self):
        if self.use_log_probabilities:
            return self._log_init_dist
        else:
            return self._init_dist

    @init_distribution.setter
    def init_distribution(self, init_distribution):
        self._init_dist = init_distribution
        self._log_init_dist = np.log(self._init_dist)

    @property
    def transition_probabilities(self):
        if self.use_log_probabilities:
            return self._log_transition_prob
        else:
            return self._transition_prob

    @transition_probabilities.setter
    def transition_probabilities(self, transition_probabilities):
        self._transition_prob = transition_probabilities
        self._log_transition_prob = np.log(self._transition_prob)

    def __call__(self, i=None, j=None):
        if i is None and j is None:
            return self.transition_probabilities
        elif i is not None and j is None:
            return self.transition_probabilities[i, :]
        elif i is None and j is not None:
            return self.transition_probabilities[:, j]
        else:
            return self.transition_probabilities[i, j]


if __name__ == '__main__':

    class CategoricalStringObservationModel(ObservationModel):

        def __init__(
                self,
                observation_probabilities,
                observations=None,
                use_log_probabilities=True
        ):
            super().__init__(use_log_probabilities=use_log_probabilities)

            self.observation_probabilities = observation_probabilities

            if observations is not None:
                self.observations = list(observations)
            else:
                self.observations = [
                    str(i) for i in len(observation_probabilities)
                ]

        @property
        def observation_probabilities(self):
            if self.use_log_probabilities:
                return self._log_obs_prob
            else:
                return self._obs_prob

        @observation_probabilities.setter
        def observation_probabilities(self, observation_probabilities):
            self._obs_prob = observation_probabilities
            self._log_obs_prob = np.log(self._obs_prob)

        def __call__(self, observation, *args, **kwargs):
            idx = self.observations.index(observation)
            return self.observation_probabilities[idx]

    obs = ("normal", "cold", "dizzy")
    states = ("Healthy", "Fever")
    observation_probabilities = np.array([[0.5, 0.1],
                                          [0.4, 0.3],
                                          [0.1, 0.6]])
    transition_probabilities = np.array([[0.7, 0.3],
                                         [0.4, 0.6]])

    observation_model = CategoricalStringObservationModel(
        observation_probabilities,
        obs
    )

    init_distribution = np.array([0.6, 0.4])

    transition_model = ConstantTransitionModel(
        transition_probabilities,
        init_distribution)

    hmm = HMM(observation_model, transition_model, state_space=states)

    path, prob = hmm.find_best_sequence(obs, log_probabilities=True)
    print(path, prob)
