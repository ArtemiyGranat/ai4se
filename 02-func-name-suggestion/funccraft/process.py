def extract_func_info(fields, parser, query, row):
    func_string = row["whole_func_string"]
    tree = parser.parse(bytes(func_string, "utf-8"))
    captures = query.captures(tree.root_node)

    comments = []
    func_name = ""
    func_body = ""
    for capture, nodes in captures.items():
        for node in nodes:
            start, end = node.start_byte, node.end_byte
            extracted_string = func_string[start:end]

            if capture in fields["name"]:
                func_name = extracted_string
            elif capture in fields["body"]:
                func_body = extracted_string
            elif capture in fields["comment"]:
                comments.append(extracted_string)

    body_without_comments = func_body
    for comment in comments:
        body_without_comments = body_without_comments.replace(comment, "")

    return {
        "func_name": func_name,
        "func_body": func_body,
        "body_without_comments": body_without_comments,
    }


def add_codet5p_prefix(field, row):
    row[field] = (
        "def <extra_id_0> :" + row[field]
    )
    return row
