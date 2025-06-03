from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import pendulum

class Leetcode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    url: str = Field(default=None)

class LeetcodePS:
    model = Leetcode

    def _get_pset(month, year):
        """
        Problemset to pull from leetcode. Instead of using the full pset, I use the problem of the day for the last year.
        """
        url_base = "https://leetcode.com"
        transport = AIOHTTPTransport(url="https://leetcode.com/graphql/", headers={"Cookie": "", "x-csrftoken": ""})
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = None
        with open("queries/leetcode-daily-problem.graphql", "r") as f:
            query = gql(f.read())
        result = client.execute(query, variable_values={"month": month, "year": year})
        try:
            challenges_list = result["dailyCodingChallengeV2"]["challenges"]
        except KeyError as e:
            return []
    
        challenges_cleaned = []
        for challenge in challenges_list:
            challenge_cleaned = {
                "id": challenge["question"]["questionFrontendId"],
                "url": f"{url_base}{challenge['link']}"
            }
            challenges_cleaned.append(challenge_cleaned)

        return challenges_cleaned


