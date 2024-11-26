import tree_sitter_python as tspython
import tree_sitter_ruby as tsruby

AVAILABLE_LANGUAGES = {
    "python": tspython.language(),
    "ruby": tsruby.language(),
}

QUERIES = {
    "python": """(function_definition
        name: (identifier) @name
        body: (block) @body
    )
    (expression_statement
        (string) @docstring
    )
    (comment) @comment
    """,
    "ruby": """(method
        name: (setter (identifier))? @name
        (identifier)? @name_without_setter
        body: (body_statement) @body
    )
    (comment) @comment
    """,
}

FIELDS = {
    "python": {
        "name": ["name"],
        "body": ["body"],
        "comment": ["docstring", "comment"],
    },
    "ruby": {
        "name": ["name_without_setter", "name"],
        "body": ["body"],
        "comment": ["comment"],
    },
}
