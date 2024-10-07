import csv
import os

import matplotlib.pyplot as plt
import seaborn as sns

TRAIN_CSV_HEADER = [
    "Model Type",
    "Accuracy",
    "F1 Score",
    "Precision",
    "Recall",
]


def get_metric_field(model_type, metric):
    if model_type in ["roberta-base", "microsoft/codebert-base"]:
        return f"eval_{metric}"
    else:
        return metric


def output_train_logs(
    model_type,
    metrics,
    stdout=True,
    log_dir="logs",
    log_file="train_logs.csv",
):
    os.makedirs(log_dir, exist_ok=True)

    acc = round(metrics[get_metric_field(model_type, "accuracy")], 4)
    f1 = round(metrics[get_metric_field(model_type, "f1")], 4)
    precision = round(metrics[get_metric_field(model_type, "precision")], 4)
    recall = round(metrics[get_metric_field(model_type, "recall")], 4)
    classif_report = metrics[get_metric_field(model_type, "classif_report")]
    conf_matrix = metrics[get_metric_field(model_type, "conf_matrix")]

    if stdout:
        print("Accuracy:", acc)
        print("F1 Score:", f1)
        print("Precision:", precision)
        print("Recall:", recall)
        print("Classification Report:\n", classif_report)

    log_data = [model_type, acc, f1, precision, recall]
    try:
        with open(f"{log_dir}/{log_file}", "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            if csv_file.tell() == 0:
                writer.writerow(TRAIN_CSV_HEADER)
            writer.writerow(log_data)
    except IOError:
        print("I/O error occurred while writing to CSV file.")

    conf_matrix_model_name = model_type.replace("/", "_").replace("-", "_")
    conf_matrix_file = f"{log_dir}/conf_matrix_{conf_matrix_model_name}.png"
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues")
    plt.title(f"Confusion Matrix - {model_type.capitalize()}")
    plt.savefig(conf_matrix_file)
    plt.show()
