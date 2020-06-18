"""
Provides methods for interacting with the current trial.

@author Ben Giacalone
"""


class Trial:

    def __init__(self):
        self.data = {}
        self.trial_finished_callback = None

    # Finishes current trial
    def finish(self):
        self.trial_finished_callback()
