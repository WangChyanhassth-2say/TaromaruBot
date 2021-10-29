from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageFont,ImageDraw,ImageMath
from io import BytesIO
import re
import os
import json
from random import randint
import base64
FILE_PATH = './src/data/artifact_analyse_data'

back_image = Image.open(os.path.join(FILE_PATH,'back_0.png')).convert('RGBA')
ttf_path = os.path.join(FILE_PATH,"zh-cn.ttf")

def text2image(char, text):

    #print('here we go')
    #print(char)
    #print(text)
    index = ' ' + ' | '.join(text.split('\n')[0:2]) + '|'
    #print(index)
    r = re.findall(r"\d+\.?\d*",index)
    #print(r)
    r[0], r[1], r[3], r[4] = r[1], r[0], r[4], r[3]
    text1 = '\n'.join(text.split('\n')[2:])
    for i in range(len(r)):
        r[i] = float(r[i])
    #print(r)
    #radar = save_radar(r)
    #print('ok radar')
    back = back_image.copy()
    r0,g0,b0,a0 = back_image.split()
    radar = save_radar(r).convert('RGBA')
    radar = radar.resize((470,420))
    r0,g0,b0,a0 = radar.split()
    #Image.show(radar)
    icon = Image.open(os.path.join(FILE_PATH, 'wish_icon',char+'.png')).convert('RGBA')
    r1,g1,b1,a1 = icon.split()
    #Image.show(icon)
    back.paste(icon,(96,400),mask = a1)
    back.paste(radar,(200,1350),mask = a0)
    
    draw = ImageDraw.Draw(back)

    draw.text((700,1550), text1,
              fill="#84210bff",
              font=ImageFont.truetype(ttf_path, size=30))
    draw.text((810,395), char,
              fill="#84210bff",
              font=ImageFont.truetype(ttf_path, size=40))

    bio = BytesIO()
    back.save(bio, format='PNG')
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    bio.close()
    return f"[CQ:image,file={base64_str}]"

def save_radar(data):

    #print('get in radar module')
    r = data.copy()
    for i in range(len(r)):
        if r[i]<= 5.0:
            r[i] = 5.0
        elif r[i]>= 20.0:
            r[i] = 20.0
    criterion = [1, 1, 1, 1, 1, 1, 1, 1] # 基准雷达图
    angles = np.linspace(0, 2 * np.pi, 7, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure(facecolor=None) # 创建画板并填充颜色
    ax = fig.add_subplot(111, polar=True)  # 设置坐标为极坐标
    # 绘制三个五边形
    floor = 0
    ceil = 19
    labels = np.array(['攻' + str(data[0]),'生' + str(data[1]),'防' + str(data[2]),'充' + str(data[3]),
                       '精' + str(data[4]),'暴' + str(data[5]),'爆' + str(data[6]),'攻' + str(data[0])])
    # 绘制五边形的循环
    temp = 1
    for i in np.arange(floor, ceil + 0.5 ,0.5):
        temp += 1
        if temp % 10 != 0:
            continue
        ax.plot(angles, [i] * (8), '-', lw= 0.5, color='black')
    for i in range(7):
        ax.plot([angles[i], angles[i+1]], [floor, ceil], '-',lw=0.5, color='black')
     # 绘制雷达图

    r.append(r[0])
    ax.plot(angles, r, '#00000000', lw=3, alpha=0.6)
    ax.fill(angles, r, facecolor='#00000000', alpha=0.35)


    # print(labels)
    ax.set_thetagrids(angles * 180 / np.pi, labels)
    ax.spines['polar'].set_visible(False)#不显示极坐标最外的圆形
    ax.set_theta_zero_location('N')#设置极坐标的起点（即0度）在正上方向
    ax.grid(False)# 不显示分隔线
    ax.set_yticks([]) # 不显示坐标间隔
    #ax.set_title('xxxxxxxxxxxx', va='bottom', fontproperties='SimHei')
    #ax.set_facecolor('#87ceeb') # 填充绘图区域的颜色
    # 保存文png图片
    #plt.subplots_adjust(left=0.09, right=1, wspace=0.25, hspace=0.25, bottom=0.13, top=0.91)
    buff_img = BytesIO()
    plt.savefig(buff_img, format='PNG', bbox_inches='tight', transparent=True)
    pil_img = Image.open(buff_img)
    plt.close()
    #buf = np.fromstring(plt.tostring_argb(), dtype=np.uint8)
    return pil_img


charlist = ['温迪', '琴', '魈', '风旅行者', '砂糖', '枫原万叶', '早柚',
            '达达利亚', '莫娜', '行秋', '芭芭拉', '珊瑚宫心海',
            '迪卢克', '可莉', '胡桃', '班尼特', '香菱', '安柏', '辛焱', '烟绯', '宵宫', '托马',
            '七七', '甘雨', '优菈', '重云', '迪奥娜', '凯亚', '罗莎莉亚', '神里绫华', '埃洛伊',
            '刻晴', '菲谢尔', '北斗', '雷泽', '丽莎', '雷电将军', '九条裟罗',
            '钟离', '阿贝多', '岩旅行者', '凝光', '诺艾尔']

A_all = [
            {'攻':'攻击力%','充':'充能效率','生':'生命值%','防':'防御力%','精':'元素精通'},
            {'水':'属性伤害','火':'属性伤害','草':'属性伤害','冰':'属性伤害','雷':'属性伤害','风':'属性伤害','岩':'属性伤害','物':'属性伤害','攻':'攻击力%','生':'生命值%','防':'防御力%','精':'元素精通'},
            {'爆':'暴击伤害','暴':'暴击率','治':'治疗加成','攻':'攻击力%','生':'生命值%','防':'防御力%','精':'元素精通'}
        ]

headerlist = [
                "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
                "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
                "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
                "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
            ]

def get_result(Char, An, QQ, tlist):
    try:
        opt = Options()
        opt.add_argument('User-Agent=' + headerlist[randint(0,19)])                           #每次调用start()都换一个随机headers
        opt.add_argument('--no-sandbox')                # 解决DevToolsActivePort文件不存在的报错
        opt.add_argument('--incognito')                 # 隐身模式（无痕模式）
        opt.add_argument('--disable-gpu')               # 谷歌文档提到需要加上这个属性来规避bug
        opt.add_argument('--hide-scrollbars')           # 隐藏滚动条，应对一些特殊页面
        opt.add_argument('blink-settings=imagesEnabled=false')      # 不加载图片，提升运行速度
        opt.add_argument('--ignore-certificate-errors') #防止报错
        opt.add_argument('--headless')                  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        
        global FILE_PATH
        driver_path = os.path.join(FILE_PATH,'chromedriver.exe')
        
        driver = Chrome(executable_path = driver_path, options = opt)
        
        driver.get('http://spongem.com/ajglz/ys/ys.html')
        

        A = []
        for t in range(len(An)):
            A.append(A_all[t][An[t]])
        
        
        driver.find_element_by_id("Char").send_keys(Char)
        driver.find_element_by_id("A1").send_keys(A[0])
        driver.find_element_by_id("A2").send_keys(A[1])
        driver.find_element_by_id("A3").send_keys(A[2])
        
        driver.find_element_by_id("QQ").send_keys(QQ)

        tlist = [x for x in tlist if x != '']
        #print(tlist)
        for i in range(1,8):
            id = 'T{}'.format(i)
            
            driver.find_element_by_id(id).send_keys(tlist[i-1])

        driver.find_element_by_id("result").click()
        result = driver.find_element_by_id("result").text
        driver.quit()
        if result.find('——') != -1:
            return text2image(Char, result.replace('（攻击0.4折算）','')[0:result.index('——')])
        else:
            return text2image(Char, result.replace('（攻击0.4折算）',''))
        
    except:
        driver.quit()
        return ''
