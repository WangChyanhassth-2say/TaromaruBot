import time
import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event, Message
from .Artifact import artifact_obtain, ARTIFACT_LIST, Artifact

artifact_random = on_command("来个圣遗物", priority=5)

@artifact_random.got('step', prompt='请输入+4或+20进行强化汪')
async def got_step(bot: Bot, event: Event, state: T_State):
    step = state["step"]
    if step not in ['+4','+20','＋4','＋20']:
        await artifact_random.finish('输入有误,请重新开始汪')
    try:
        true_step = int(step[1:])
        return true_step
    except:
        await artifact_random.finish('输入有误,请重新开始汪')
        

    
@artifact_random.handle()
async def when_it_comes_to_artifact(bot: Bot, event: Event, state: T_State):
    
    mes = ''
    r_suit_name = random.choice(artifact_obtain)
    r_artifact_name = random.choice(ARTIFACT_LIST[r_suit_name]["element"])
    artifact = Artifact(r_artifact_name)
    strengthen_level = 0
    
    step = await got_step(bot,event,state)
        
    mes += artifact.get_artifact_CQ_code()
    await artifact_random.send(Message(mes), at_sender=True)
    
    while True:
        origin_level = strengthen_level
        strengthen_level += int(step)
        for i in range(origin_level,strengthen_level):
            artifact.strengthen()
        mes = ''
        mes += artifact.get_artifact_CQ_code()
        await artifact_random.send(Message(mes), at_sender=True)
        if strengthen_level >= 20:
            time.sleep(2)
            await artifact_random.finish('强化成功汪')

