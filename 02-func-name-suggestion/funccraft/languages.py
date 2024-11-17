import tree_sitter_python as tspython

AVAILABLE_LANGUAGES = {
    "python": tspython.language(),
}

# TODO: Fix python query
QUERIES = {
    "python": """(function_definition
          name: (identifier) @name
          body: (block
            (expression_statement(string))
            (_)? @body-without-comments
          ) @body
        )
    """,
}
