from os import path
import re
import click
import option


@click.group()
def main():
    """
    Main command group.
    """
    pass


@main.command()
@click.argument('input_file')
@click.option('--output', '-o', type=str, required=True)
@click.option('--force', type=bool, is_flag=True)
@click.option('--center_image', type=bool, is_flag=True)
@click.option('--en_punctuation', type=bool, is_flag=True)
@click.option('--katex_svg', type=bool, is_flag=True)
def generate(input_file: str, output: str, force: bool, center_image: bool, en_punctuation: bool, katex_svg: bool):
    """
    Generate markdown by options.
    """
    # =========
    # read file
    # =========
    if input_file == '':
        raise Exception('The input file name could not be empty.')
    elif not path.exists(input_file):
        raise Exception('The input file "{}" does not exist.'.format(input_file))
    elif not path.isfile(input_file):
        raise Exception('The input file "{}" is a directory.'.format(input_file))
    with open(input_file, 'r', encoding='utf-8') as fi:
        content = fi.read()

    # ===============
    # do option parse
    # ===============

    # 1. center image
    center_image_option = option.CenterImageOption(center_image)
    content = center_image_option.parse(content)

    # 2. english punctuation
    en_punctuation_option = option.EnPunctuation(en_punctuation)
    content = en_punctuation_option.parse(content)

    # 3. katex svg
    katex_svg_option = option.KatexSvgOption(katex_svg)
    content = katex_svg_option.parse(content)

    # ==========
    # write file
    # ==========
    if output == '':
        raise Exception('The output file name could not be empty.')
    elif path.exists(output):
        if not path.isfile(output):
            raise Exception('The output file "{}" is a directory.'.format(output))
        elif not force:
            raise Exception('The output file "{}" has been existed, please rename or use --force flag.'.format(output))
    with open(output, 'w+', encoding='utf-8') as fo:
        fo.write(content)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        click.echo('Error: {}'.format(ex))
        exit(1)
