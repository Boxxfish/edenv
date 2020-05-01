"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import click
from pathlib import Path
from shutil import copytree
from os import path

@click.group()
def main():
    pass

@main.command()
@click.argument("name")
def init(name):
    click.echo(f"Creating project \"{name}\"...")

    # Copy project folder from template directory
    project_path = Path(name)
    source_path = Path(path.realpath(__file__)).parent.parent.parent / "project"
    if project_path.is_dir():
        click.echo(f"Error: Could not create directory \"{name}\".", err=True)
        return
    copytree(source_path, project_path)

    click.echo("Done.")


@main.command()
def list():
    click.echo("list")


if __name__ == "__main__":
    main()
