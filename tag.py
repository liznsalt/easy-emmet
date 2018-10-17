def tag(name, *contents, cls=None, **attrs):
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(f' {attr}="{value}"'
                            for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''

    if contents:
        return '\n'.join(f'<{name}{attr_str}>{content}</{name}>'
                            for content in contents)
    else:
        return f'<{name}{attr_str}/>'
