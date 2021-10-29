import re
import os
import time
import base64
from PIL import Image
from io import BytesIO
from nonebot import on_endswith
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event, Message

filepath = './src/data/daily_material_icon'
namelist = ['武器突破材料','角色天赋材料']
daily_material = on_endswith("天刷什么", priority=5)
days_info = {'今天':0, 
             '明天':1,
             '后一天':1,
             '后天':2,
             '大后天':3,
             '大大后天':4,
             '昨天':-1,
             '前一天':-1,
             '前天':-2,
             '大前天':-3,
             '大大前天':-4}

def get_day(daylist):
    global days_info
    global namelist
    base = time.time()-14400
    for i in daylist:
        try:
            base += days_info[i] * 86400
        except:
            return '太郎丸不认识{}汪'.format(i)
    base = time.strftime('%w',time.localtime(base))
    if base == "0":
        return "好像是周日，所有材料副本都开放汪"
    elif base in ["1","4"]:
        png_name = ['{}_周一周四.png'.format(name) for name in namelist]
    elif base in ["2","5"]:
        png_name = ['{}_周二周五.png'.format(name) for name in namelist]
    elif base in ["3","6"]:
        png_name = ['{}_周三周六.png'.format(name) for name in namelist]
    
    bio = BytesIO()
    image = Image.open(os.path.join(filepath, png_name[0]))
    image.save(bio, format='PNG')
    base64_str0 = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    bio = BytesIO()
    image = Image.open(os.path.join(filepath, png_name[1]))
    image.save(bio, format='PNG')
    base64_str1 = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    image.close()
    
    return f"[CQ:image,file={base64_str0}][CQ:image,file={base64_str1}]"


@daily_material.handle()
async def handle_daily_material(bot:Bot, event:Event):
    error = 0
    day = str(event.get_message()).strip()[:-3]
    if '的' in day:
        daylist = re.split('[的]',day)
    else:
        daylist = [day]
    
    await daily_material.send(Message('让太郎丸看看汪...'))
    try:
        msg = get_day(daylist)
        await daily_material.finish(message=Message(msg))
    except Exception as e:
        print(e)
        #await daily_material.finish(message=Message('出了点问题，请找汪酱问一问汪'))
