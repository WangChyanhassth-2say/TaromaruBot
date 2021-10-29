from random import randint
from nonebot import on_keyword
from nonebot.adapters.cqhttp import Bot, Event

keywords = {'乖','屑','机器人','bot','狗','太郎丸','骂','哟','在','呀','你','冲','歪','汪'}
dog_chat = on_keyword(keywords, priority=10)

@dog_chat.handle()
async def bark(bot:Bot, event:Event):
	await dog_chat.finish(message = ''.join(['汪'*randint(0,3) + '!'*randint(0,3) for i in range(3)]))
