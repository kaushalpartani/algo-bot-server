import argparse

class NoUsageHelpFormatter(argparse.HelpFormatter):
    """
    Custom help formatter so that the usage string isn't added to the response of the zulip message
    """
    def add_usage(self, usage, actions, groups, prefix=None):
        pass