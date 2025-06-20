import random
import argparse
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
from ..problem_set_interface import ProblemSetInterface, ProblemSetOptions
from ..no_usage_help_formatter import NoUsageHelpFormatter


class CSESOptions(ProblemSetOptions):
    """
    Config options for the CSES problem set
    """
    topic: Optional[str] = None

    def model_post_init(self, __context):
        if self.topic:
            self.topic = self.topic.lower()

class CSESPSet(ProblemSetInterface):
    """
    return a list of dicts, each dict corresponds to a db record. Eventually will need to batch and send to db.
    Note, CSES is still adding problems, so this will need to be done semi-regularly
    """
    def __init__(self):
        self.url_base = "https://cses.fi"
        self.pset_url = f"{self.url_base}/problemset/list/"
        
        self.parser = argparse.ArgumentParser(description="CSES Problem Set", formatter_class=NoUsageHelpFormatter)
        self.parser.add_argument("--topic", "-t", help="Select a specific topic/category for random problem generation")

    def _get_random_problem(self) -> str:
        pset = self._get_pset()
        valid_topics = '\n'.join(set([x["category"] for x in pset]))
        print(valid_topics)
        
        if self.options.topic:
            pset = list(filter(lambda x: x["category"].lower() == self.options.topic, pset))
            if not pset:
                return f"No problems found for topic: {self.options.topic}. Valid options:\n ```{valid_topics}```"
        
        if not pset:
            return "No problems available"
        
        return random.choice(pset)["url"]

    def process_command(self, options: str) -> str:
        """
        Processes a command for the CSES problem set. If it's not valid, returns the help string instead of the problem url.
        Returns the string content to be included in the message response.

        Args:
            options(str): the command line options passed in by the user
        """
        try:
            args = self.parser.parse_args(options.split())
            self.options = CSESOptions(**vars(args))
        except (SystemExit, Exception) as e:
            print(e)
            return self.parser.format_help()

        return self._get_random_problem()

    def _get_pset(self):
        response = requests.get(self.pset_url)
        if response.status_code != 200:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return []
        
        return_list = []
        soup = BeautifulSoup(response.text, 'html.parser')
        
        categories = soup.find_all('h2')

        for cat in categories:
            problem_list = cat.find_next("ul")
            problems = problem_list.find_all('a')

            for problem in problems:
                problem_dict = {
                    "id": problem["href"].split("/")[-1],
                    "url": f"{self.url_base}{problem['href']}",
                    "category": f"{cat.text.replace(' ', '_')}"
                }
                return_list.append(problem_dict)
            
        return return_list



