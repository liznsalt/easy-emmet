EMMET_SYNTAX = ['+', '>', '*', '(', ')']


def lex_node(string):
    emmet_node = ''
    if string[0] in EMMET_SYNTAX:
        return None, string
    for c in string:
        if c in EMMET_SYNTAX:
            return emmet_node, string[len(emmet_node):]
        else:
            emmet_node += c
    return emmet_node, []


def lex_syntax(string):
    if string[0] in EMMET_SYNTAX:
        return string[0], string[1:]
    return None, string


def lex(string):
    tokens = []
    while len(string):
        emmet_node, string = lex_node(string)
        if emmet_node is not None:
            tokens.append(emmet_node)
            continue
        
        emmet_syntax, string = lex_syntax(string)
        if emmet_syntax is not None:
            tokens.append(emmet_syntax)
            continue
    return tokens
