from os import path
import re
import click


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
def generate(input_file: str, output: str, force: bool, center_image: bool, en_punctuation: bool):
    """
    Generate markdown by options.
    """
    force = not not force
    center_image = not not center_image
    en_punctuation = not not en_punctuation

    if input_file == '':
        raise Exception('The input file name could not be empty.')
    elif not path.exists(input_file):
        raise Exception('The input file "{}" does not exist.'.format(input_file))
    elif not path.isfile(input_file):
        raise Exception('The input file "{}" is a directory.'.format(input_file))

    with open(input_file, 'r', encoding='utf-8') as fi:
        # read
        content = fi.read()

        # 1. center image
        if center_image:
            center_image_re = re.compile(r'!\[(.*?)\]\((.+?)\)')
            content = center_image_re.sub(r'<div align="center"><img src="\2" alt="\1" /></div>', content)

        # 2. english punctuation
        if en_punctuation:
            punctuations = [
                ['，', ', '], ['。', '. '], ['、', ', '], ['：', ': '], ['；', '; '], ['？', '? '], ['！', '! '], ['—', '-'],
                ['“', ' "'], ['”', '" '], ['（', ' ('], ['）', ') '], ['【', ' ['], ['】', '] '], ['《', ' <'], ['》', '> '],
            ]
            for k, v in punctuations:
                content = re.sub(f' *' + k + f' *', v, content)

        # new line and space
        content = re.sub(f' \n', '\n', content)
        content = re.sub(f'\n ', '\n', content)

        # save
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
