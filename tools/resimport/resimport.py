"""
Resource importer for EDEnv.

@author Ben Giacalone
"""
import click


@click.command()
@click.argument("files", nargs=-1, type=click.File('r'))
def resimport(files):
    for file in files:
        # Output type of file being imported
        click.echo(f"File name: {file.name}")


if __name__ == "__main__":
    resimport()
