"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import click
from pathlib import Path
from shutil import copytree
from os import path
import yaml
from tools.envedit import envedit as edenv_envedit
from tools.resimport import resimport as edenv_resimport


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

    # Configure project.yaml
    config_path = Path(f"{name}/project.yaml")
    if not config_path.exists():
        click.echo(f"Error: Could not find {name}/project.yaml.", err=True)
        return
    config = {}
    with open(f"{name}/project.yaml", "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        config["project"] = name
    with open(f"{name}/project.yaml", "w") as file:
        yaml.dump(config, file)

    click.echo("Done.")


@main.command()
def list():
    # Open configuration file
    config_path = Path("project.yaml")
    if not config_path.exists():
        click.echo("Error: Could not find project.yaml.", err=True)
        return
    with open("project.yaml", "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

        # List environments in project
        click.echo("Environments in this project:")
        envs = config["envs"]
        if envs is None:
            click.echo("None")
        else:
            for env in envs:
                click.echo(f"{env}")


@main.command()
def envedit():
    edenv_envedit.main()


@main.command()
@click.argument("files", nargs=-1, type=click.File('rb'))
@click.pass_context
def resimport(ctx, files):
    ctx.forward(edenv_resimport.resimport)

if __name__ == "__main__":
    main()
