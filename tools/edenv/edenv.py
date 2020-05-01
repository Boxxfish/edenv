"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import click

@click.group()
def main():
    pass


@main.command()
def init():
    click.echo("init")


@main.command()
def list():
    click.echo("list")


if __name__ == "__main__":
    main()
