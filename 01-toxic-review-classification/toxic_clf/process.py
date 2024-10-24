import re

contraction_mapping = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "this's": "this is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "here's": "here is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
    "aint": "is not",
    "arent": "are not",
    "cant": "cannot",
    "cause": "because",
    "couldve": "could have",
    "couldnt": "could not",
    "didnt": "did not",
    "doesnt": "does not",
    "dont": "do not",
    "hadnt": "had not",
    "hasnt": "has not",
    "havent": "have not",
    "howdy": "how do you",
    "its": "it is",
    "lets": "let us",
    "maam": "madam",
    "maynt": "may not",
    "mightve": "might have",
    "mightnt": "might not",
    "mightntve": "might not have",
    "mustve": "must have",
    "mustnt": "must not",
    "mustntve": "must not have",
    "neednt": "need not",
    "needntve": "need not have",
    "oclock": "of the clock",
    "oughtnt": "ought not",
    "shouldve": "should have",
    "shouldnt": "should not",
    "werent": "were not",
    "yall": "you all",
    "youre": "you are",
    "youve": "you have",
}

profanity_patterns = {
    " fuck ": [
        "(f)(u|[^a-z0-9 ])(c|[^a-z0-9 ])(k|[^a-z0-9 ])([^ ])*",
        "(f)([^a-z]*)(u)([^a-z]*)(c)([^a-z]*)(k)",
        " f[!@#\$%\^\&\*]*u[!@#\$%\^&\*]*k",
        "f u u c",
        "(f)(c|[^a-z ])(u|[^a-z ])(k)",
        r"f\*",
        "feck ",
        " fux ",
        "f\*\*",
        "f\-ing",
        "f\.u\.",
        "f###",
        " fu ",
        "f@ck",
        "f u c k",
        "f uck",
        "f ck",
    ],
    " crap ": [
        " (c)(r|[^a-z0-9 ])(a|[^a-z0-9 ])(p|[^a-z0-9 ])([^ ])*",
        " (c)([^a-z]*)(r)([^a-z]*)(a)([^a-z]*)(p)",
        " c[!@#\$%\^\&\*]*r[!@#\$%\^&\*]*p",
        "cr@p",
        " c r a p",
    ],
    " ass ": [
        "[^a-z]ass ",
        "[^a-z]azz ",
        "arrse",
        " arse ",
        "@\$\$" "[^a-z]anus",
        " a\*s\*s",
        "[^a-z]ass[^a-z ]",
        "a[@#\$%\^&\*][@#\$%\^&\*]",
        "[^a-z]anal ",
        "a s s",
    ],
    " ass hole ": [" a[s|z]*wipe", "a[s|z]*[w]*h[o|0]+[l]*e", "@\$\$hole"],
    " bitch ": [
        "bitches",
        " b[w]*i[t]*ch",
        " b!tch",
        " bi\+ch",
        " b!\+ch",
        " (b)([^a-z]*)(i)([^a-z]*)(t)([^a-z]*)(c)([^a-z]*)(h)",
        " biatch",
        " bi\*\*h",
        " bytch",
        "b i t c h",
    ],
    " bastard ": ["ba[s|z]+t[e|a]+rd"],
    " transgender": ["transgender"],
    " gay ": ["gay", "homo"],
    " cock ": [
        "[^a-z]cock",
        "c0ck",
        "[^a-z]cok ",
        "c0k",
        "[^a-z]cok[^aeiou]",
        " cawk",
        "(c)([^a-z ])(o)([^a-z ]*)(c)([^a-z ]*)(k)",
        "c o c k",
    ],
    " dick ": [" dick[^aeiou]", "d i c k"],
    " suck ": [
        "sucker",
        "(s)([^a-z ]*)(u)([^a-z ]*)(c)([^a-z ]*)(k)",
        "sucks",
        "5uck",
        "s u c k",
    ],
    " cunt ": ["cunt", "c u n t"],
    " bull shit ": ["bullsh\*t", "bull\$hit", "bull sh.t"],
    " jerk ": ["jerk"],
    " idiot ": [
        "i[d]+io[t]+",
        "(i)([^a-z ]*)(d)([^a-z ]*)(i)([^a-z ]*)(o)([^a-z ]*)(t)",
        "idiots",
        "i d i o t",
    ],
    " dumb ": ["(d)([^a-z ]*)(u)([^a-z ]*)(m)([^a-z ]*)(b)"],
    " shit ": [
        "shitty",
        "(s)([^a-z ]*)(h)([^a-z ]*)(i)([^a-z ]*)(t)",
        "shite",
        "\$hit",
        "s h i t",
        "sh\*tty",
        "sh\*ty",
        "sh\*t",
    ],
    " shit hole ": ["shythole", "sh.thole"],
    " retard ": ["returd", "retad", "retard", "wiktard", "wikitud"],
    " rape ": ["raped"],
    " dumb ass": ["dumbass", "dubass"],
    " ass head": ["butthead"],
    " sex ": ["sexy", "s3x", "sexuality"],
    " nigger ": [
        "nigger",
        "ni[g]+a",
        " nigr ",
        "negrito",
        "niguh",
        "n3gr",
        "n i g g e r",
    ],
    " shut the fuck up": [" stfu", "^stfu"],
    " for your fucking information": [" fyfi", "^fyfi"],
    " get the fuck off": ["gtfo", "^gtfo"],
    " oh my fucking god ": [" omfg", "^omfg"],
    " what the hell ": [" wth", "^wth"],
    " what the fuck ": [" wtf", "^wtf"],
    " son of bitch ": [" sob ", "^sob "],
    " pussy ": [
        "pussy[^c]",
        "pusy",
        "pussi[^l]",
        "pusses",
        "(p)(u|[^a-z0-9 ])(s|[^a-z0-9 ])(s|[^a-z0-9 ])(y)",
    ],
    " faggot ": [
        "faggot",
        " fa[g]+[s]*[^a-z ]",
        "fagot",
        "f a g g o t",
        "faggit",
        "(f)([^a-z ]*)(a)([^a-z ]*)([g]+)([^a-z ]*)(o)([^a-z ]*)(t)",
        "fau[g]+ot",
        "fae[g]+ot",
    ],
    " mother fucker": [
        " motha f",
        " mother f",
        "motherucker",
        " mofo",
        " mf ",
    ],
    " whore ": ["wh\*\*\*", "w h o r e"],
    " haha ": [
        "ha\*\*\*ha",
    ],
}


def remove_url(row):
    url_regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return url_regex.sub(" ", row.message)


def expand_contraction(row):
    specials = ["’", "‘", "´", "`", "'"]

    for s in specials:
        row.message = row.message.replace(s, "'")
        row.message = " ".join(
            [
                (
                    contraction_mapping[t.lower()]
                    if t.lower() in contraction_mapping
                    else t
                )
                for t in row.message.split(" ")
            ]
        )
    return row.message


def remove_repetitions(row):
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    return pattern.sub(r"\1", row.message)


def remove_special_symbols(row):
    pattern = re.compile(r"[^a-zA-Z0-9_ ]")
    return pattern.sub(" ", row.message)


# TODO: Use regexes, not just default patterns
def resolve_profane_words(row):
    for target, patterns in profanity_patterns.items():
        for pat in patterns:
            row.message = row.message.replace(pat, target)
    return row.message


def remove_programming_keywords(row):
    with open("prepared-dataset/programming_keywords.txt", "r") as f:
        keywords = [line.strip() for line in f if line.strip()]

    words = row.message.split()
    filtered_words = [word for word in words if word.lower() not in keywords]

    return " ".join(filtered_words)
