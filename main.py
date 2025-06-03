from typing import Union, List, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from problem_sets.leetcode import LeetcodePS
from enum import Enum


from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class ZulipInnerMessage(BaseModel):
    avatar_url: Optional[str]
    client: str
    content: str
    display_recipient: str
    id: int
    is_me_message: bool
    reactions: List[dict]
    recipient_id: int
    rendered_content: str
    sender_email: str
    sender_full_name: str
    sender_id: int
    sender_realm_str: str
    stream_id: Optional[int]
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
    print(message)
    return message

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



    

        

