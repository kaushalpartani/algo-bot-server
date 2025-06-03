from typing import Union, List, Optional
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


from fastapi import FastAPI
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

    

        

