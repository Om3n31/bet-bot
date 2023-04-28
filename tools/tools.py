import secrets
import base64
from discord import Message
from typing import List

def generate_hash(n: int):
    return base64.b64encode(secrets.token_bytes(n)).decode('utf-8')

def get_cmd_from_message(message: Message) -> str:
    return message.content.split(' ')[0]

def get_content_from_message(message: Message, has_amount: bool) -> str:
    mentions = get_mentions_from_message(message)
    if has_amount:
        dirty_message = message.content.split(' ')[:-1]
    else:
        dirty_message = message.content.split(' ')[1:]
    return ' '.join([x for x in dirty_message if x not in mentions])

def get_amount_from_message(message: Message) -> float:
    content = get_content_from_message(message, False)
    return float(content.split(' ')[-1])
        

def get_mentions_from_message(message: Message) -> List[str]:
    return [m.mention for m in message.mentions]
