from typing import Union, List, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from problem_sets.leetcode.leetcode import LeetcodePS
from problem_sets.cses.cses import CSESPSet
from problem_sets.advent_of_code.advent_of_code import AdventOfCodePS
from enum import Enum

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

DESCRIPTION = """
ProblemSetPicker, created by kaushal partani (s1 2025)

ProblemSetPicker is a zulip bot allowing for users to generate random problems from problem sets. 

The current supported base commands are:
```
{available_commands}
```
"""
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

class ZulipMessage(BaseModel):
    bot_email: str
    bot_full_name: str
    data: str
    message: ZulipInnerMessage
    token: str
    trigger: str

app = FastAPI()

def response_wrapper(content: str) -> dict:
    return {"content": content}

def help_handler() -> str:
    available_commands = "\n".join(PROBLEM_SET_MAPPING.keys())
    return DESCRIPTION.format(available_commands=available_commands)

SPECIAL_COMMANDS = {
    "help": help_handler
}

PROBLEM_SET_MAPPING = {
    "leetcode": LeetcodePS,
    "lc": LeetcodePS,
    "advent_of_code": AdventOfCodePS,
    "aoc": AdventOfCodePS,
    "cses": CSESPSet,
}

@app.post("/")
def process_message(message: ZulipMessage):
    content = message.data.lower().split(" ", 1)
    command = content[0]
    if len(content) > 1:
        options = content[1]
    else:
        options = ""

    if command in SPECIAL_COMMANDS:
        return response_wrapper(SPECIAL_COMMANDS[command]())
    elif command in PROBLEM_SET_MAPPING:
        problem_set_class = PROBLEM_SET_MAPPING[command]
        problem_set = problem_set_class()
        return response_wrapper(problem_set.process_command(options))
    else:
        return response_wrapper(f"Unknown command '{command}'. Try running the `help` command for more details.")

@app.get("/lc-random-problem")
def get_random_lc_problem(difficulty: Optional[str] = None):
    lc_ps = LeetcodePS()
    options = f"-d {difficulty}" if difficulty else ""
    return lc_ps.process_command(options)

@app.get("/cses-random-problem")
def get_random_cses_problem(topic: Optional[str] = None):
    cses_ps = CSESPSet()
    options = f"-t {topic}" if topic else ""
    return cses_ps.process_command(options)

@app.get("/aoc-random-problem")
def get_random_aoc_problem(year: Optional[str] = None):
    aoc_ps = AdventOfCodePS()
    options = f"-y {year}" if year else ""
    return aoc_ps.process_command(options)