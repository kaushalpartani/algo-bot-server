from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
import requests
from bs4 import BeautifulSoup
import json
import random

class CSES(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    url: str = Field(default=None)
    category: str = Field(default=None)

class CSESPSet:
    """
    return a list of dicts, each dict corresponds to a db record. Eventually will need to batch and send to db.
    Note, CSES is still adding problems, so this will need to be done semi-regularly
    """
    model = CSES

    def __init__(self):
        self.url_base = "https://cses.fi"
        self.pset_url = f"{self.url_base}/problemset/list/"
    
    def _get_random_problem(self, topic=None):
        pset = self._get_pset()
        print(topic)
        
        if topic:
            pset = filter(lambda x: x["category"].lower() == topic, pset)
        
        return random.choice(pset)["url"]


    def _get_pset(self):
        response = requests.get(self.pset_url)
        if response.status_code != 200:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return
        
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
                    "category": f"{cat.text}"
                }
                return_list.append(problem_dict)

        return return_list



