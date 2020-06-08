"""
Resource importer for EDEnv.
Imports resources like models and exports them into JSON resource files.

@author Ben Giacalone
"""
import click
from tools.resimport.model_importer import ModelImporter


@click.command()
@click.argument("files", nargs=-1, type=click.File('rb'))
def resimport(files):
    for file in files:
        click.echo(f"File name: {file.name}")

        # Determine type of asset
        asset_type = None
        if ModelImporter.is_type(file):
            asset_type = "model"

        if asset_type is None:
            click.echo("Error: Could not determine asset type", err=True)
            return

        click.echo(f"Asset type: {asset_type}")

        # Export asset
        if asset_type == "model":
            ModelImporter.export(file)

        click.echo(f"Successfully imported {file.name}")
        click.echo("----------------------")


if __name__ == "__main__":
    resimport()
