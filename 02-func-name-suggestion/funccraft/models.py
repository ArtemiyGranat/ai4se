from collections.abc import Iterable
from functools import cache
from pprint import pprint

import datasets
import evaluate
import torch
from transformers import AutoTokenizer, T5ForConditionalGeneration

from funccraft.process import add_codet5p_prefix


@cache
def _init_metrics():
    return (evaluate.load('exact_match'), evaluate.load('rouge'))


def predict(dataset: datasets.Dataset, model: str) -> None:
    device = torch.device("cpu")

    tokenizer = AutoTokenizer.from_pretrained(model)
    model = T5ForConditionalGeneration.from_pretrained(model).to(device)
    model.eval()

    dataset = dataset.map(add_codet5p_prefix).select(range(1000))

    references = dataset["func_name"]
    inputs = tokenizer(
        dataset["body_without_comments"],
        return_tensors='pt',
        padding=True,
        truncation=True,
        max_length=80,
    ).to(device)
    outputs = model.generate(**inputs, max_length=80)
    predictions = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    del model

    correct_predictions = sum(
        ref in pred for ref, pred in zip(references, predictions)
    )
    print(f'Correct predictions: {correct_predictions}\n')

    cleaned_predictions = [
        (pred.split(" ")[1].split("(")[0] if len(pred.split(" ")) > 1 else pred)
        for pred in predictions
    ]

    print(cleaned_predictions)
    print(references)
    eval_results = run_evaluate(predictions=predictions, references=references)

    print('*' * 80)
    print('Evaluation results:')
    pprint(eval_results)
    print('*' * 80)


def run_evaluate(
    predictions: Iterable[str], references: Iterable[str]
) -> dict[str, float]:
    em, rouge = _init_metrics()
    em_score = em.compute(predictions=predictions, references=references)
    rouge_scores = rouge.compute(predictions=predictions, references=references)

    return {**rouge_scores, **em_score}
