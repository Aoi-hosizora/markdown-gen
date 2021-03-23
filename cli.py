#!/usr/bin/env python

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
@click.option('--output', '-o',   type=str, required=True, help='Output file path.')
@click.option('--force',          type=bool, is_flag=True, help='Force to save.')
@click.option('--center_image',   type=bool, is_flag=True, help='Make images center.')
@click.option('--en_punctuation', type=bool, is_flag=True, help='Use English punctuations.')
@click.option('--katex_image',    type=bool, is_flag=True, help='Use image for katex equation.')
@click.option('--add_toc',        type=bool, is_flag=True, help='Add table of content.')
@click.option('--copy_image',     type=bool, is_flag=True, help='Copy image to current folder.')
def generate(input_file: str, output: str, force: bool, center_image: bool, en_punctuation: bool, katex_image: bool, add_toc: bool, copy_image: bool):
    """
    Generate markdown by options.
    """
    # =========
    # read file
    # =========
    if input_file == '':
        raise CommandException('The input file name could not be empty.')
    elif not path.exists(input_file):
        raise CommandException('The input file "{}" does not exist.'.format(input_file))
    elif not path.isfile(input_file):
        raise CommandException('The input file "{}" is a directory.'.format(input_file))
    with open(input_file, 'r', encoding='utf-8') as fi:
        content = fi.read()

    # ============
    # parse option
    # ============

    # 1. center image
    center_image_option = option.CenterImageOption(center_image)
    content = center_image_option.parse(content)

    # 2. english punctuation
    en_punctuation_option = option.EnPunctuationOption(en_punctuation)
    content = en_punctuation_option.parse(content)

    # 3. katex image
    katex_image_option = option.KatexImageOption(katex_image)
    content = katex_image_option.parse(content)

    # 4. add toc
    add_toc_option = option.AddTocOption(add_toc)
    content = add_toc_option.parse(content)

    # 5. copy image
    copy_image_option = option.CopyImageOption(copy_image)
    content = copy_image_option.parse(input_file, content)

    # ==========
    # write file
    # ==========
    if output == '':
        raise CommandException('The output file name could not be empty.')
    elif path.exists(output):
        if not path.isfile(output):
            raise CommandException('The output file "{}" is a directory.'.format(output))
        elif not force:
            raise CommandException('The output file "{}" has been existed, please rename or use --force flag.'.format(output))
    with open(output, 'w+', encoding='utf-8') as fo:
        fo.write(content)


class CommandException(Exception):
    """
    Represent an command exception.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message


if __name__ == '__main__':
    try:
        main()
    except CommandException as ex:
        click.echo('Error: {}'.format(ex.message))
        exit(1)
    else:
        raise ex
