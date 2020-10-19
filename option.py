import re


class CenterImageOption:
    """
    Option for --center_image
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        if self.do_option:
            center_image_re = re.compile(r'!\[(.*?)\]\((.+?)\)')
            content = center_image_re.sub(r'<div align="center"><img src="\2" alt="\1" /></div>', content)

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
            punctuations_2 = [['“', ' "'], ['”', '" '], ['（', ' ('], ['）', ') '], ['【', ' ['], ['】', '] '], ['《', ' <'], ['》', '> ']]
            for k, v in punctuations_1:
                content = re.sub(f' *' + k + f' *', v, content)
            for k, v in punctuations_2:
                if v[0] == ' ':
                    content = re.sub(f'\n *' + k + f' *', '\n' + v[1:], content)
                content = re.sub(f' *' + k + f' *', v, content)

        return content


class KatexSvgOption:
    """
    Option for --katex_svg
    """

    def __init__(self, do_option: bool):
        self.do_option: bool = not not do_option

    def parse(self, content: str) -> str:
        if self.do_option:
            pass

        return content
