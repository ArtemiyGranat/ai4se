#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 1.5cm),
)

#set text(
  size: 14pt
)

#set heading(
  numbering: "1.",
  supplement: [Раздел]
)

#show raw: set block(
  above: 1em,
  below: 2em,
)

#let clr-caption = rgb("777777")
#let que = [*(?)*]

#let cred(url) = link(
  url,
  text(
    fill: blue
  )[
    \[cred\]
  ],
)

#let caption(body) = text(fill: clr-caption)[
  #par[
    #body
  ]
]

#align(center)[
  #text(18pt)[*AI4SE. Лабораторная №1. Классификация токсичного код-ревью*]

  #text(16pt)[Гранат Артемий Максимович, МСП241]
]

= Описание решения

== Обработка данных

1. Удаление ссылок.
2. Раскрытие сокращений в их полные аналоги (например, I'd -> I would).
3. Обработка повторяющихся букв (например, hellooo -> hello).
4. Удаление специальных символов (все, кроме букв и цифр).
5. Восстановление сокрытой нецензурной лексики.
6. Удаление ключевых слов, связанных с программированием.

=== Идеи, не вошедшие в решение

1. Удаление стоп-слов.
2. Обработка предложений, записанных в PascalCase.

= Модели

1. Logistic Regression
2. Random Forest
3. roberta-base
4. microsoft/codebert-base

= Векторизаторы

1. `TfidfVectorizer`
2. `CountVectorizer`

= Метрики (TfidfVectorizer)

#let results = csv("train_logs_tfidf.csv")

#table(
  columns: 5,
  ..results.flatten(),
)

= Метрики (CountVectorizer)

#let results = csv("train_logs_count.csv")

#table(
  columns: 5,
  ..results.flatten(),
)

= Метрики трансформеров

#let results = csv("train_logs_transformers.csv")

#table(
  columns: 5,
  ..results.flatten(),
)

= Confusion Matrices

== Logistic Regression (TfidfVectorizer)

#figure(
  image("conf_matrix_logistic_regression.jpg", width: 60%),
)

== Random Forest (TfidfVectorizer)

#figure(
  image("conf_matrix_random_forest.png", width: 60%),
)

== Logistic Regression (CountVectorizer)

#figure(
  image("conf_matrix_logistic_regression_count.png", width: 60%),
)

== Random Forest (CountVectorizer)

#figure(
  image("conf_matrix_random_forest_count.png", width: 60%),
)

== roberta-base

#figure(
  image("conf_matrix_roberta-base.jpg", width: 60%),
)

== microsoft/codebert-base

#figure(
  image("conf_matrix_microsoft_codebert_base.png", width: 60%),
)

= Трудности

Из элементов, вызывающих трудности, можно выделить сам датасет --- слишком
мало записей, помеченных как токсичные, из-за чего модель относительно плохо
справляется с обнаружением токсичных комментариев.

Еще одной трудностью, не относящейся к содержанию задания, была проблема с
вычислительными мощностями --- имеющаяся машина не позволяла обучить
трансформеры на ней.
