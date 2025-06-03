import pendulum
import random

class AdventOfCodePS:
    def __init__(self):
        start_year = 2015
        end_year = pendulum.now().year
        self.valid_years = range(start_year, end_year) # don't allow for the current year until it's passed
        self.valid_days = range(1, 26) # valid days for advent of code
        self.url_base = "https://adventofcode.com/"
    
    def _get_random_problem(self):
        return f"{self.url_base}{random.choice(self.valid_years)}/day/{random.choice(self.valid_days)}"


