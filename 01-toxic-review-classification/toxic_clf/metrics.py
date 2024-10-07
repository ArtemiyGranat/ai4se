import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def compute_metrics(labels, preds):
    acc = accuracy_score(labels, preds)
    precision = precision_score(labels, preds)
    f1 = f1_score(labels, preds)
    recall = recall_score(labels, preds)
    classif_report = classification_report(labels, preds)
    conf_matrix = confusion_matrix(labels, preds)

    return {
        "accuracy": acc,
        "f1": f1,
        "precision": precision,
        "recall": recall,
        "classif_report": classif_report,
        "conf_matrix": conf_matrix,
    }


def compute_transformer_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)

    return compute_metrics(labels, preds)
