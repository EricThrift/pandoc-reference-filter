import pandocfilters as pf

latex_figure = """
\\begin{{figure}}[htbp]
\\label{{{label}}}
\\centering
\\includegraphics{{{filename}}}
\\caption{{{caption}}}
\\end{{figure}}"""


def latex(s):
    return pf.RawInline('latex', s)


def isfigure(key, value):
    return (key == 'Para' and len(value) == 2 and value[0]['t'] == 'Image')


def isattr(string):
    return string.startswith('{') and string.endswith('}')


def figure(key, value, format, metadata):
    # a figure is created when an image (which is an inline element)
    # is the only element in a paragraph. If we have a image and
    # some attr defined with {}, then the length of the paragraph
    # list will be 2.
    if isfigure(key, value) and isattr(value[1]['c']):
        image = value[0]
        attr = value[1]
        filename = image['c'][1][0]
        caption = pf.stringify(value[0]['c'][0])
        label = attr['c'].strip('{}')
        return pf.Para([latex(latex_figure.format(filename=filename,
                                                  caption=caption,
                                                  label=label))])

# latex_fig = latex_figure.format(label=1, filename=2, caption=3)
# print latex_fig
# print latex(latex_fig)
# print pf.Str(latex(latex_fig))
# exit()

if __name__ == '__main__':
    pf.toJSONFilter(figure)
