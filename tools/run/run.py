"""
Main CLI app for EDEnv.

@author Ben Giacalone
"""
import importlib
import sys
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
    # Allow importing project scripts from project folder
    sys.path.append(".")

    if interactive:
        pass

    # Read config file
    if config is not None:
        config_file = yaml.load(config, Loader=yaml.FullLoader)
        cfg_environment = config_file["environment"] if "environment" in config_file else ""
        cfg_pj_script = "project_scripts." + config_file["project_script"] if "project_script" in config_file else ""
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
    # Create project script
    project_script = None
    if pj_script is not None:
        module_name = pj_script.split(".")[-1].title()
        module_name = module_name.replace("_", "")

        script_spec = importlib.util.find_spec(pj_script)
        if script_spec is None:
            click.echo(f"Error: Could not import project script \"{pj_script}\".", err=True)
            return

        module = __import__(pj_script, fromlist=[module_name])
        project_script_class = getattr(module, module_name)
        project_script = project_script_class()

        project_script.start_run()

    if trials == -1:
        i = 0
        interrupted = False
        while True:
            if interrupted:
                break

            trial_data = {}

            if project_script is not None:
                project_script.start_trial(trial_data)

            try:
                run_player(environment, trial_data, i % visualize != 0)
            except SystemExit as e:
                interrupted = True

            if project_script is not None:
                project_script.finish_trial(trial_data)

            i = (i + 1) % visualize
    else:
        interrupted = False
        for i in range(trials):
            if interrupted:
                break

            trial_data = {}

            if project_script is not None:
                project_script.start_trial(trial_data)

            try:
                run_player(environment, trial_data, i % visualize != 0)
            except SystemExit as e:
                interrupted = True

            if project_script is not None:
                project_script.finish_trial(trial_data)

    if project_script is not None:
        project_script.finish_run()


# Runs the player and returns trial data
def run_player(environment, trial_data, headless=False):
    if headless:
        player.run_headless(environment, trial_data)
    else:
        player.run(environment, trial_data)
    return trial_data


if __name__ == "__main__":
    run()
