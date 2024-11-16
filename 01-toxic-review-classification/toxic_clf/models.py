from statistics import mean, stdev

import pandas as pd
from datasets import Dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from tqdm import tqdm
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

from toxic_clf.log import output_train_logs
from toxic_clf.metrics import compute_metrics, compute_transformer_metrics

classic_models = {
    "logistic_regression": LogisticRegression(random_state=42),
    "random_forest": RandomForestClassifier(
        max_depth=10, class_weight="balanced", random_state=42
    ),
}

vectorizers = {
    "count": CountVectorizer,
    "tfidf": TfidfVectorizer,
}


def train_classic_model(
    X_train_vec, y_train, X_test_vec, y_test, model_type, random_state
):
    model = classic_models[model_type]

    skf = StratifiedKFold(n_splits=10, random_state=random_state, shuffle=True)
    scores = []
    for train_index, val_index in tqdm(skf.split(X_train_vec, y_train)):
        X_fold_train, X_fold_val = (
            X_train_vec[train_index],
            X_train_vec[val_index],
        )
        y_fold_train, y_fold_val = (
            y_train.iloc[train_index],
            y_train.iloc[val_index],
        )

        model.fit(X_fold_train, y_fold_train)
        y_fold_pred = model.predict(X_fold_val)
        fold_acc = accuracy_score(y_fold_val, y_fold_pred)
        scores.append(fold_acc)

    mean_acc = mean(scores)
    std_acc = stdev(scores)
    print(f"Mean Accuracy: {mean_acc}")
    print(f"Mean Standard Deviation: {std_acc}")

    y_pred = model.predict(X_test_vec)
    del model

    metrics = compute_metrics(y_test, y_pred)
    output_train_logs(model_type, metrics)


def train_transformer_model(
    X_train, y_train, X_test, y_test, model_type, checkpoint
):
    def tokenize_function(examples):
        return tokenizer(
            examples["text"], padding="max_length", truncation=True
        )

    tokenizer = AutoTokenizer.from_pretrained(model_type)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_type if not checkpoint else checkpoint, num_labels=2
    )

    train_data = Dataset.from_pandas(
        pd.DataFrame({"text": X_train, "labels": y_train})
    )
    test_data = Dataset.from_pandas(
        pd.DataFrame({"text": X_test, "labels": y_test})
    )
    train_data = train_data.map(tokenize_function, batched=True)
    test_data = test_data.map(tokenize_function, batched=True)

    training_args = TrainingArguments(
        output_dir=f"./trained-{model_type}",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_dir=f"./logs-{model_type}",
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=test_data,
        compute_metrics=compute_transformer_metrics,
    )
    if not checkpoint:
        trainer.train()
    metrics = trainer.evaluate()
    del model

    output_train_logs(model_type, metrics)


def classifier(
    dataset,
    model_type,
    vectorizer="tfidf",
    test_size=0.2,
    checkpoint=None,
    random_state=42,
):
    dataset = dataset.to_pandas()
    X_train, X_test, y_train, y_test = train_test_split(
        dataset["message"],
        dataset["is_toxic"],
        test_size=test_size,
        random_state=random_state,
    )

    if model_type in classic_models:
        vectorizer = vectorizers[vectorizer](
            stop_words="english", ngram_range=(1, 2), lowercase=True
        )
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)
        train_classic_model(
            X_train_vec, y_train, X_test_vec, y_test, model_type, random_state
        )
    elif model_type in ["roberta-base", "microsoft/codebert-base"]:
        train_transformer_model(
            X_train, y_train, X_test, y_test, model_type, checkpoint
        )
    else:
        raise ValueError(
            f"""Model type '{model_type}' not recognized. Choose from
                'logistic_regression', 'random_forest', 'roberta-base',
                'microsoft/codebert-base'."""
        )


def predict(model, comment):
    pass
