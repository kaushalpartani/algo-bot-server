from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import pendulum
import pathlib
import random
from pydantic import BaseModel
from typing import Optional, List
import argparse
from ..problem_set_interface import ProblemSetInterface, ProblemSetOptions

class Leetcode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    url: str = Field(default=None)

class LeetcodeOptions(ProblemSetOptions):
    """
    Config options for the leetcode problem set
    """
    difficulty: Optional[str] = None

    def model_post_init(self, __context):
        if not self.difficulty:
            self.difficulty = random.choice(["easy", "medium", "hard"])
        
        valid_difficulties = ["easy", "medium", "hard"]
        if self.difficulty not in valid_difficulties:
            self.difficulty = random.choice(valid_difficulties)

class LeetcodePS(ProblemSetInterface):
    def __init__(self):
        self.url_base = "https://leetcode.com"
        self.transport = AIOHTTPTransport(url="https://leetcode.com/graphql/", headers={"Cookie": "", "x-csrftoken": ""})
        self.client = Client(transport=self.transport, fetch_schema_from_transport=False)
        
        self.parser = argparse.ArgumentParser(description="LeetCode Problem Set")
        self.parser.add_argument("--difficulty", "-d", choices=["easy", "medium", "hard"], 
                                help="Select difficulty level for random problem generation")

    def _get_random_problem(self) -> str:
        current_dir = pathlib.Path(__file__).parent
        query_path = current_dir / "queries" / "leetcode-random-problem.graphql"
        
        query = None
        with open(query_path, "r") as f:
            query = gql(f.read())
        
        variables = {
            "filtersV2": {
                "filterCombineType": "ALL",
                "difficultyFilter": {
                    "difficulties": [self.options.difficulty.upper()],
                    "operator": "IS"
                },
                "premiumFilter": {
                    "premiumStatus": ["NOT_PREMIUM"],
                    "operator": "IS"
                }
            }
        }
        
        result = self.client.execute(query, variable_values=variables)
        try:
            print(result)
            question = result["randomQuestionV2"]["titleSlug"]
        except KeyError as e:
            return "Unable to fetch problem from LeetCode"
        return f"{self.url_base}/problems/{question}"

    def process_command(self, options: str) -> str:
        """
        Processes a command for the leetcode problem set. If it's not valid, returns the help string instead of the problem url.
        Returns the string content to be included in the message response.

        Args:
            options(str): the command line options passed in by the user
        """
        try:
            args = self.parser.parse_args(options.split())
            self.options = LeetcodeOptions(**vars(args))
        except (SystemExit, Exception) as e:
            print(e)
            return self.parser.format_help()

        return self._get_random_problem()
