import pendulum
import random
from pydantic import BaseModel
from typing import Optional, Dict
import argparse
from ..problem_set_interface import ProblemSetInterface, ProblemSetOptions

class AdventOfCodeOptions(ProblemSetOptions):
    """
    Config options for the aoc problem set
    """
    year: Optional[int] = None
    day: Optional[int] = None

    def model_post_init(self, __context):
        if not self.year:
            self.year = random.choice(range(2015, pendulum.now().year))
        
        if not self.day:
            self.day = random.choice(range(1, 26))

        if self.year < 2015:
            self.year = 2015
        
        if self.year >= pendulum.now().year:
            self.year = pendulum.now().year - 1

class AdventOfCodePS(ProblemSetInterface):
    def __init__(self):
        self.url_base = "https://adventofcode.com/"
        
        self.parser = argparse.ArgumentParser(description="Advent of Code Problem Set")
        self.parser.add_argument("--year", "-y", help="Select a specific year for random problem generation")

    def _get_random_problem(self) -> str:
        return f"{self.url_base}{self.options.year}/day/{self.options.day}"

    def process_command(self, options: str) -> str:
        """
        Processes a command for the advent of code problem set. If it's not valid, returns the help string instead of the problem url.
        Returns the string content to be included in the message response.

        Args:
            options(str): the command line options passed in by the user
        """
        try:
            args = self.parser.parse_args(options.split())
            self.options = AdventOfCodeOptions(**vars(args))
        except (SystemExit, Exception) as e:
            print(e)
            return self.parser.format_help()

        return self._get_random_problem()
    


        

