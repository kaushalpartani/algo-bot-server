from typing import Union, List, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from problem_sets.leetcode import LeetcodePS
from problem_sets.cses import CSESPSet
from problem_sets.advent_of_code import AdventOfCodePS
from enum import Enum


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class ZulipInnerMessage(BaseModel):
    avatar_url: Optional[str]
    client: str
    content: str
    display_recipient: Union[str, List[dict]]
    id: int
    is_me_message: bool
    reactions: List[dict]
    recipient_id: int
    rendered_content: str
    sender_email: str
    sender_full_name: str
    sender_id: int
    sender_realm_str: str
    stream_id: Optional[int] = None
    subject: str
    submessages: List[dict]
    timestamp: int
    topic_links: List[dict]
    type: str

class ZulipResponse(BaseModel):
    bot_email: str
    bot_full_name: str
    data: str
    message: ZulipInnerMessage
    token: str
    trigger: str


app = FastAPI()


@app.post("/")
def process_message(message: ZulipResponse):
    content = message.data.lower()
    difficulty = None
    
    if "leetcode" in content:
        if "easy" in content:
            difficulty = LCDifficulty.easy
        elif "medium" in content:
            difficulty = LCDifficulty.medium
        elif "hard" in content:
            difficulty = LCDifficulty.hard
        else:
            return {
                "content": "no response"
            }
        lc_ps = LeetcodePS()
        problem_url = lc_ps._get_random_problem(difficulty.value.upper())
        return {
            "content": f"Here's a random {difficulty.value} LeetCode problem: {problem_url}"
        }
    elif "cses" in content:
        cses_ps = CSESPSet()
        problem_url = cses_ps._get_random_problem()
        return {
            "content": f"Here's a random CSES problem: {problem_url}"
        }
    elif ("advent of code" in content) or ("aoc" in content):
        aoc_ps = AdventOfCodePS()
        problem_url = aoc_ps._get_random_problem()
        return {
            "content": f"Here's a random Advent of Code problem: {problem_url}"
        }


    return {
        "content": "empty"
    }

@app.get("/hello")
def hello():
    return "hello!"


class LCDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

@app.get("/lc-random-problem/{difficulty}")
def get_random_lc_problem(difficulty: LCDifficulty):
    lc_ps = LeetcodePS()
    return RedirectResponse(lc_ps._get_random_problem(difficulty.value.upper()))

@app.get("/cses-random-problem")
def get_random_cses_problem():
    cses_ps = CSESPSet()
    return RedirectResponse(cses_ps._get_random_problem())

@app.get("/aoc-random-problem")
def get_random_aoc_problem():
    aoc_ps = AdventOfCodePS()
    return RedirectResponse(aoc_ps._get_random_problem())


    

        

