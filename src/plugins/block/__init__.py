import os
import json
import random
from io import BytesIO
from PIL import Image
from base64 import b64encode
from nonebot import on_notice, on_message
from nonebot.adapters.cqhttp import Bot, Message,  PokeNotifyEvent, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me

last_message = ''
filepath = 'src/data/block_data/icon'
poke = on_notice(rule=to_me(), block=False, priority=9)
block_repeat = on_message(block=False, priority=9)
with open(os.path.join(filepath[:-5],'names.json')) as fp:
    load = json.load(fp)

@poke.handle()
async def _poke(bot: Bot, event: PokeNotifyEvent, state: dict) -> None:
    global load
    global filepath
    pic_name = random.choice(load['poke_list'])
    image = Image.open(os.path.join(filepath, pic_name))
    bio = BytesIO()
    image.save(bio, format='PNG')
    base64_str = 'base64://' + b64encode(bio.getvalue()).decode()
    image.close()
    msg = f"[CQ:image,file={base64_str}]"

    await poke.finish(message=Message(msg), at_sender=False)

@block_repeat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global load
    global filepath
    global last_message
    pic_name = random.choice(load['block_repeat_list'])
    image = Image.open(os.path.join(filepath, pic_name))
    bio = BytesIO()
    image.save(bio, format='PNG')
    base64_str = 'base64://' + b64encode(bio.getvalue()).decode()
    image.close()
    message = str(event.get_message())
    if message == last_message:
        tem = "打断汪" + random.randint(1, 3) * '!' + f"[CQ:image,file={base64_str}]"
        last_message = tem
        await block_repeat.finish(message=Message(tem))
    else:
        last_message = message
    
