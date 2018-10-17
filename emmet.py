from tag import tag
from parse import parse, EmmetTree
from lex import lex


def _emmet_tokens(tokens):
    emmet_string = ''

    for node in tokens:
        if not node.has_son():
            emmet_string += tag(node.name, **node.attrs)
        else:
            sons_content = ''.join([_emmet_tokens([son]) for son in node.sons])
            emmet_string += tag(node.name, sons_content, **node.attrs)    
    return emmet_string


def emmet(string):
    return _emmet_tokens(parse(lex(string))[0])
