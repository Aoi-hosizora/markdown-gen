import re
import urllib.parse


class CenterImageOption:
    """
    Option for --center_image
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        if self.do_option:
            center_image_re = re.compile(r'!\[(.*?)\]\((.+?)\)')
            content = center_image_re.sub(r'<p align="center"><img src="\2" alt="\1" /></p>', content)

        return content


class EnPunctuation:
    """
    Option for --en_punctuation
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        if self.do_option:
            punctuations_1 = [['，', ', '], ['。', '. '], ['、', ', '], ['：', ': '], ['；', '; '], ['？', '? '], ['！', '! '], ['—', '-']]
            punctuations_2 = [['“', ' "'], ['”', '" '], ['（', ' ('], ['）', ') '], ['【', ' \\['], ['】', '\\] '], ['《', ' <'], ['》', '> ']]
            for k, v in punctuations_1:
                content = re.sub(f' *' + k + f' *', v, content)
            for k, v in punctuations_2:
                if v[0] == ' ':
                    content = re.sub(f'\n *' + k + f' *', '\n' + v[1:], content)
                content = re.sub(f' *' + k + f' *', v, content)
            content = re.sub(f'[ \t]*\n', '\n', content)

        return content


class KatexImageOption:
    """
    Option for --katex_image
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> (str, str):
        def sub_parse(content: str, *, is_block: bool = False) -> str:
            # alt
            alt_katex = katex.strip(" \t\n$").replace('\n', ' ')
            # src
            new_katex = alt_katex
            new_katex = new_katex.replace('\\R', '\\mathbb{R}').replace('\\N', '\\mathbb{N}').replace('\\Z', '\\mathbb{Z}').replace('\\C', '\\mathbb{C}')
            new_katex = new_katex.replace('\\llbracket', '\u27E6').replace('\\rrbracket', '\u27E7')
            new_katex = new_katex.replace('\\argmax', '\\arg\\!\\!\\max').replace('\\argmin', '\\arg\\!\\!\\min')
            if new_katex.count('\\\\') != 0:
                new_katex = '\\begin{gathered} %s \\end{gathered}' % new_katex
            new_katex = ('\\large ' if is_block else '') + new_katex
            new_katex = urllib.parse.quote(new_katex)

            return alt_katex, new_katex

        if self.do_option:
            # style
            block_css = 'background-color: #FFFFFF; padding: 5px 8px; margin: 5px 0'
            inline_css = 'background-color: #FFFFFF; padding: 2px 1px; margin: -3px 0'

            # block
            equation_block_re = re.compile(r'((?<!\\)\$\$(?:.+?)(?<!\\)\$\$)', re.DOTALL)
            old_katexes = equation_block_re.findall(content)
            new_katexes = [katex for katex in old_katexes]
            for idx, katex in enumerate(new_katexes):
                alt_katex, new_katex = sub_parse(katex, is_block=True)
                new_katexes[idx] = '<div align="center"><image alt="{}" src="https://math.now.sh?from={}" style="{}" /></div>'.format(alt_katex, new_katex, block_css)
            for idx, old_katex in enumerate(old_katexes):
                content = content.replace(old_katex, new_katexes[idx])

            # inline
            equation_block_re = re.compile(r'((?<!\\)\$.+?(?<!\\)\$)')
            old_katexes = equation_block_re.findall(content)
            new_katexes = [katex for katex in old_katexes]
            for idx, katex in enumerate(new_katexes):
                alt_katex, new_katex = sub_parse(katex, is_block=False)
                new_katexes[idx] = '<image alt="{}" src="https://math.now.sh?inline={}" style="{}" />'.format(alt_katex, new_katex, inline_css)
            for idx, old_katex in enumerate(old_katexes):
                content = content.replace(old_katex, new_katexes[idx])

        return content
