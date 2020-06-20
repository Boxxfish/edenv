"""
A sample project script.

"""

class SampleProjectScript:

    def __init__(self):
        pass
    
    # Runs before any trials are run
    # Do initial run-wide setup here
    def start_run(self):
        pass
    
    # Runs right before trial
    def start_trial(self, trial_data):
        pass

    # Runs right after a trial
    def finish_trial(self, trial_data):
        pass

    # Runs after all trials are completed
    def finish_run(self):
        pass
