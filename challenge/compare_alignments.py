# a helper function to compute precision, recall and f_score for alignments
from typing import List


def compare_alignments_(prediction: List[dict], ground_truth: List[dict], types: List[str]) -> (float, float, float):
    """
    Parameters
    ----------
    prediction: List of dictionaries containing the predicted alignments
    ground_truth: List of dictionaries containing the ground truth alignments
    types: List of alignment types to consider for evaluation (e.g ['match', 'deletion', 'insertion']

    Returns
    -------
    precision, recall, f score
    """

    pred_filtered = list(filter(lambda x: x['label'] in types, prediction))
    gt_filtered = list(filter(lambda x: x['label'] in types, ground_truth))

    filtered_correct = [pred for pred in pred_filtered if pred in gt_filtered]

    n_pred_filtered = len(pred_filtered)
    n_gt_filtered = len(gt_filtered)
    n_correct = len(filtered_correct)

    if n_pred_filtered > 0 or n_gt_filtered > 0:
        precision = n_correct / n_pred_filtered if n_pred_filtered > 0 else 0.
        recall = n_correct / n_gt_filtered if n_gt_filtered > 0 else 0
        f_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    else:
        # no prediction and no ground truth for a given type -> correct alignment
        precision, recall, f_score = 1., 1., 1.

    return precision, recall, f_score