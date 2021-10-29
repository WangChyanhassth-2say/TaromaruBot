from .artifact_analyse_config import charlist, A_all, headerlist, text2image, save_radar, get_result
from nonebot.adapters.cqhttp import Bot, Event, Message
from nonebot.typing import T_State
from nonebot import on_command
from random import randint
import time
import re
import os


artifact_analyse = on_command("圣遗物词条", priority=5)


@artifact_analyse.got('Char', prompt='请输入角色名汪')
async def got_Char(bot: Bot, event: Event, state: T_State):
    Char = state["Char"]
    return Char

@artifact_analyse.got('An', prompt='请输入圣遗物后三位主属性简称汪，顺序为[沙漏杯子头],如:攻火爆')
async def got_An(bot: Bot, event: Event, state: T_State):
    An = state["An"]
    return An

@artifact_analyse.got('QQ', prompt='请输入武器白值汪')
async def got_QQ(bot: Bot, event: Event, state: T_State):
    QQ = state["QQ"]
    return QQ

@artifact_analyse.got('tlist', prompt='请按以下顺序输入【圣遗物界面】数据[生攻防精暴爆充]，空格分开汪:')
async def got_tlist(bot: Bot, event: Event, state: T_State):
    tlist = state["tlist"]
    return tlist


@artifact_analyse.handle()
async def _ana(bot: Bot, event: Event, state: T_State):
    Char = await got_Char(bot,event,state)
    An = await got_An(bot,event,state)
    QQ = await got_QQ(bot,event,state)
    tlist = await got_tlist(bot,event,state)
    try:
        tlist = tlist.split(' ')
        QQ = int(QQ)
    except:
        await artifact_analyse.finish('输入可能有误汪，请自行检查或联系汪酱并重新开始', at_sender=True)
    result = ''
    await artifact_analyse.send('稍等汪...')
    if Char in charlist and len(An) == 3 and len(tlist) == 7:
        result = get_result(Char, An, QQ, tlist)
        if result != '':
            await artifact_analyse.finish(message=Message(result), at_sender=True)
        else:
            await artifact_analyse.finish('输入可能有误汪，请自行检查或联系汪酱并重新开始', at_sender=True)
    else:
        await artifact_analyse.finish('输入可能有误汪，请自行检查或联系汪酱并重新开始', at_sender=True)

