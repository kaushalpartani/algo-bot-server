from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import pendulum
import pathlib

class Leetcode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    url: str = Field(default=None)

class LeetcodePS:
    model = Leetcode

    def __init__(self):
        self.url_base = "https://leetcode.com"
        self.transport = AIOHTTPTransport(url="https://leetcode.com/graphql/", headers={"Cookie": "", "x-csrftoken": ""})
        self.client = Client(transport=self.transport, fetch_schema_from_transport=False)

    def _get_random_problem(self, difficulty):
        current_dir = pathlib.Path(__file__).parent
        query_path = current_dir / "queries" / "leetcode-random-problem.graphql"
        
        query = None
        with open(query_path, "r") as f:
            query = gql(f.read())
        
        variables = {
            "filtersV2": {
                "filterCombineType": "ALL",
                "difficultyFilter": {
                    "difficulties": [difficulty],
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
            return []
        return f"{self.url_base}/problems/{question}"


    def _get_pset(self, month, year):
        """
        Problemset to pull from leetcode. Instead of using the full pset, I use the problem of the day for the last year.
        """
        # Get the directory where the current file is located
        current_dir = pathlib.Path(__file__).parent
        query_path = current_dir / "queries" / "leetcode-daily-problem.graphql"
        
        query = None
        with open(query_path, "r") as f:
            query = gql(f.read())
        result = self.client.execute(query, variable_values={"month": month, "year": year})
        try:
            challenges_list = result["dailyCodingChallengeV2"]["challenges"]
        except KeyError as e:
            return []
    
        challenges_cleaned = []
        for challenge in challenges_list:
            challenge_cleaned = {
                "id": challenge["question"]["questionFrontendId"],
                "url": f"{self.url_base}{challenge['link']}"
            }
            challenges_cleaned.append(challenge_cleaned)

        return challenges_cleaned
