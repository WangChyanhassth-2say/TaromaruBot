from nonebot import on_command
from .gacha import filepath , Gacha , POOL
from .gacha_arm import Gacha as Gacha_arm
from .gacha_nor import Gacha as Gacha_nor
from nonebot.adapters.cqhttp import Bot, Event, Message
import os
import json


group_pool = {
    # 这个字典保存每个群对应的卡池是哪个，群号字符串为key,卡池名为value，群号不包含在字典key里卡池按默认DEFAULT_POOL
}

def save_group_pool():
    with open(os.path.join(filepath,'gid_pool.json'),'w',encoding='UTF-8') as f:
        json.dump(group_pool,f,ensure_ascii=False)



# 检查gid_pool.json是否存在，没有创建空的
if not os.path.exists(os.path.join(filepath,'gid_pool.json')):
    save_group_pool()



# 读取gid_pool.json的信息
with open(os.path.join(filepath,'gid_pool.json'),'r',encoding='UTF-8') as f:
    group_pool = json.load(f)



role_rare_10 = on_command("角色限定池十连", priority=5)
@role_rare_10.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha()
    await role_rare_10.finish(Message(G.gacha_10()) , at_sender=True)

role_rare_90 = on_command("角色限定池一井", priority=5)
@role_rare_90.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha()
    await role_rare_90.finish(Message(G.gacha_90()) , at_sender=True)

army_10 = on_command("武器池十连", priority=5)
@army_10.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha_arm()
    await army_10.finish(Message(G.gacha_10()) , at_sender=True)

army_80 = on_command("武器池一井", priority=5)
@army_80.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha_arm()
    await army_80.finish(Message(G.gacha_80()) , at_sender=True)

normal_10 = on_command("常驻池十连", priority=5)
@normal_10.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha_nor()
    await normal_10.finish(Message(G.gacha_10()) , at_sender=True)

normal_90 = on_command("常驻池一井", priority=5)
@normal_90.handle()
async def _gacha(bot:Bot, event:Event):
    G = Gacha_nor()
    await normal_90.finish(Message(G.gacha_90()) , at_sender=True)
