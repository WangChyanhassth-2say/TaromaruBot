from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, Message

from .run import run

runcode = on_command('code', priority=5)


@runcode.handle()
async def _(bot: Bot, event: Event):
    code = str(event.get_message()).strip()
    res = await run(code)
    await runcode.send(message=Message(res), at_sender=True)
