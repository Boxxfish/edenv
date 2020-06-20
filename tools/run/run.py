"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import time

import click
import yaml

from tools.run import player


@click.command()
@click.option("-i", "--interactive/--no-interactive", default=False)
@click.option("-e", "--environment", type=str, default="")
@click.option("-c", "--config", type=click.File('r'))
@click.option("-t", "--trials", type=int, default=-1)
@click.option("-v", "--visualize", type=int, default=1)
def run(interactive, environment, config, trials, visualize):
    if interactive:
        pass

    # Read config file
    if config is not None:
        config_file = yaml.load(config, Loader=yaml.FullLoader)
        cfg_environment = config_file["environment"] if "environment" in config_file else ""
        cfg_pj_script = config_file["project_script"] if "project_script" in config_file else ""
        cfg_trials = config_file["trials"] if "trials" in config_file else -1
        cfg_visualize = config_file["visualize"] if "visualize" in config_file else 1
        run_trials(cfg_environment, cfg_trials, cfg_visualize, cfg_pj_script)
    else:
        if environment == "":
            return
        run_trials(environment, trials, visualize)


# Runs the player n number of trials
# If "trials" is -1, run forever
def run_trials(environment, trials, visualize, pj_script=None):
    if pj_script is not None:
        pass

    if trials == -1:
        i = 0
        while True:
            if pj_script is not None:
                pass
            run_player(environment, i % visualize != 0)
            i = (i + 1) % visualize
    else:
        for i in range(trials):
            if pj_script is not None:
                pass
            run_player(environment, i % visualize != 0)


# Runs the player and returns trial data
def run_player(environment, headless=False):
    trial_data = {}
    if headless:
        player.run_headless(environment, trial_data)
    else:
        player.run(environment, trial_data)
    return trial_data


if __name__ == "__main__":
    run()
