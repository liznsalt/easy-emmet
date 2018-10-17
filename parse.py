# 没处理括号情况
from lex import EMMET_SYNTAX
NODE_ATTR = ['.', '[', '{']


class EmmetTree:
    def __init__(self, name, content=None, sons=None, cls=None, **attrs):
        self.name = name
        self.sons = []
        self.attrs = {}
        if sons is not None:
            for son in sons:
                self.sons.append(son)

        if content is not None:
            attrs['contents'] = [content]
        if cls is not None:
            attrs['cls'] = cls
        if not attrs:
            attrs = {}
        self.attrs = attrs

    def add_sons(self, sons):
        for son in sons:
            self.sons.append(son)

    def __repr__(self):
        if self.sons and self.attrs:
            return f'<{self.name} attrs={self.attrs} sons={self.sons}>'
        elif not self.sons and self.attrs:
            return f'<{self.name} attrs={self.attrs}>'
        elif self.sons and not self.attrs:
            return f'<{self.name} sons={self.sons}>'
        else:
            return f'<{self.name}>'

    def has_son(self):
        return len(self.sons) > 0


def parse_node(string):
    # return EmmetTree(string)
    node_name = ''
    content = ''
    attrs = {}
    for c in string:
        if c in '[{':
            string = string[len(node_name):]
            break
        else:
            node_name += c
    
    if string[0] == '[':
        end_index = string.find(']')
        attrs_str = string[1:end_index].split()
        for attr in attrs_str:
            if '=' in attr:
                key, value = attr.split('=')
            else:
                key = attr
                value = ''
            attrs[key] = value
        string = string[end_index+1:]
    
    if len(string) > 0 and string[0] == '{':
        content = string[1:-1]

    if content:
        return EmmetTree(node_name, content=content, **attrs)
    else:
        return EmmetTree(node_name, **attrs)

def parse(tokens: list):
    if tokens == []:
        return []

    emmet_tree_list = []
    # if tokens[0] == '(':
    #     return parse(tokens[1:]), tokens[1:]
    while len(tokens):
        # if tokens[0] == ')':
        #     if len(tokens) == 1 or tokens[1] != '*':
        #         return emmet_tree_list + parse(tokens[1:]), tokens[1:]
        #     else:
        #         return (emmet_tree_list + parse(tokens[1:])) * int(tokens[2]), tokens[3:]
        if tokens[0] == '+':
            tokens = tokens[1:]
            continue

        node = parse_node(tokens[0])
        if len(tokens) == 1:
            emmet_tree_list.append(node)
            return emmet_tree_list, []
        # 处理 > + *
        if tokens[1] == '>':
            son_list, rest = parse(tokens[2:])
            node.add_sons(son_list)
            emmet_tree_list.append(node)
            tokens = rest
        elif tokens[1] == '+':
            emmet_tree_list.append(node)
            tokens = tokens[2:]
        elif tokens[1] == '*':
            for _ in range(int(tokens[2])):
                emmet_tree_list.append(node)
            tokens = tokens[3:]

    return emmet_tree_list, []
