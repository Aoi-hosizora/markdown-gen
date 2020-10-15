import click

@click.group()
def main():
    pass

@main.command()
@click.argument('arg')
@click.option('--opt', '-o', type=str)
def do(arg, opt):
    """
    do command
    :param arg: The arg text
    :param opt: The opt text
    """
    click.echo('arg: {}, opt: {}'.format(arg, opt))

@main.command()
def hello():
    """
    hello command
    """
    click.echo('This is markdown-gen cli.')

if __name__ == '__main__':
    main()
