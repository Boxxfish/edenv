"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import click

@click.command()
@click.option("-i", "--interactive/--no-interactive", default=False)
@click.option("-c", "--config", type=click.File('r'))
@click.option("-t", "--trials", type=int, default=-1)
@click.option("-v", "--visualize", type=int, default=10)
def run(interactive, config, trials, visualize):
    if interactive:
        pass

    if trials == -1:
        pass
    else:
        pass


if __name__ == "__main__":
    run()
