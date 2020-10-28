import re
import urllib.parse
import md_toc
import utils


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


class EnPunctuationOption:
    """
    Option for --en_punctuation
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        if self.do_option:
            # replace
            punctuations_1 = [['，', ', '], ['。', '. '], ['、', ', '], ['：', ': '], ['；', '; '], ['？', '? '], ['！', '! '], ['—', '-']]
            punctuations_2 = [['“', ' "'], ['”', '" '], ['‘', ' \''], ['’', '\' '], ['（', ' ('], ['）', ') '], ['【', ' \\['], ['】', '\\] '], ['《', ' <'], ['》', '> ']]
            for k, v in punctuations_1:
                content = re.sub(r' *' + k + r' *', v, content)
            for k, v in punctuations_2:
                nv = v[1:] if v[0] == ' ' else v
                content = re.compile(r'\n( *)' + k + r' *', re.DOTALL).sub(r'\n\1' + nv, content)
                content = re.compile(r'(?<!\n) *' + k + r' *', re.DOTALL).sub(v, content)

            # adjust
            # test, test, (test, test) , "test, test", test, test
            punctuations_3 = [',', '.', ':', ';', '?', '!']
            punctuations_4 = [['"', '\'', '(', '\\[', '<'], ['"', '\'', ')', '\\]', '>']]
            for single_punctuation in punctuations_3:
                for double_punctuation in punctuations_4[0]:
                    content = content.replace(single_punctuation + '  ' + double_punctuation, single_punctuation + ' ' + double_punctuation)
                for double_punctuation in punctuations_4[1]:
                    content = content.replace(double_punctuation + ' ' + single_punctuation, double_punctuation + single_punctuation)
            content = re.sub(r'[ \t]*\n', '\n', content)

        return content


class KatexImageOption:
    """
    Option for --katex_image
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        def sub_parse(content: str, *, is_block: bool = False) -> (str, str):
            # alt
            alt_katex = katex.strip(' \t\n$').replace('\n', ' ')
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
            block_equation_re = re.compile(r'((?<!\\)\$\$(?:.+?)(?<!\\)\$\$)', re.DOTALL)
            old_katexes = block_equation_re.findall(content)
            new_katexes = [katex for katex in old_katexes]
            for idx, katex in enumerate(new_katexes):
                alt_katex, new_katex = sub_parse(katex, is_block=True)
                new_katexes[idx] = f'<div align="center"><image alt="{alt_katex}" src="https://math.now.sh?from={new_katex}" style="{block_css}" /></div>'
            for idx, old_katex in enumerate(old_katexes):
                content = content.replace(old_katex, new_katexes[idx])

            # inline
            inline_equation_re = re.compile(r'((?<!\\)\$.+?(?<!\\)\$)')
            old_katexes = inline_equation_re.findall(content)
            new_katexes = [katex for katex in old_katexes]
            for idx, katex in enumerate(new_katexes):
                alt_katex, new_katex = sub_parse(katex, is_block=False)
                new_katexes[idx] = f'<image alt="{alt_katex}" src="https://math.now.sh?inline={new_katex}" style="{inline_css}" />'
            for idx, old_katex in enumerate(old_katexes):
                content = content.replace(old_katex, new_katexes[idx])

        return content

class AddTocOption:
    """
    Option for --add_toc
    """

    def __init__(self, do_option: bool):
        self.do_option = not not do_option
    
    def parse(self, content: str) -> str:
        if self.do_option:
            new_content = '# TOC\n\n' + content
            toc = utils.build_toc(new_content)
            content = '# TOC\n\n' + toc + '\n' + content

        return content
