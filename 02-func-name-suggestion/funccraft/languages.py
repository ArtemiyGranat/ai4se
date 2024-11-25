import tree_sitter_python as tspython

AVAILABLE_LANGUAGES = {
    "python": tspython.language(),
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
}
