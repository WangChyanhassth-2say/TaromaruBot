from PIL import Image,ImageFont,ImageDraw,ImageMath
from io import BytesIO
from .config import SECONDARY_LEVEL_PROBABILITY,CONSUME_STRENGTHEN_POINTS
import os
import json
import random
import base64

FILE_PATH = './src/data/artifact_random_data'
ARTIFACT_LIST = {}
ARTIFACT_PROPERTY = []
PROPERTY_LIST = {}

artifact_obtain = []
flower,feather,hourglass,cup,crown = (0,1,2,3,4)

back_image = Image.open(os.path.join(FILE_PATH,"icon", 'background.png'))
ttf_path = os.path.join(FILE_PATH,"zh-cn.ttf")

def init_json():

    global ARTIFACT_LIST
    global ARTIFACT_PROPERTY
    global PROPERTY_LIST
    global artifact_obtain

    with open(os.path.join(FILE_PATH,"artifact_list.json"),"r",encoding="UTF-8") as f:
        ARTIFACT_LIST = json.load(f)

    with open(os.path.join(FILE_PATH,"artifact_property.json"),"r",encoding="UTF-8") as f:
        ARTIFACT_PROPERTY = json.load(f)

    with open(os.path.join(FILE_PATH,"property_list.json"),"r",encoding="UTF-8") as f:
        PROPERTY_LIST = json.load(f)

    for suit_name in ARTIFACT_LIST.keys():
        
        artifact_obtain.append(suit_name)
        
init_json()



class Artifact(object):
    def __init__(self, property = None):

        if property.__class__.__name__ == "str":
            self._name_init(property)
        elif property.__class__.__name__ == "dict":
            self._dict_init(property)
        else:
            raise ValueError("你需要提供圣遗物名称字符串或一个字典对象")

    def _name_init(self,_name):
        self.name = _name
        self.suit_name = self.get_suit_name(self.name)
        self.level = 0
        self.artifact_type = self.get_artifact_type(self.suit_name,self.name)
        self.main = self.get_random_main()
        self.initial_secondary = {}
        self.strengthen_secondary_list = []
        self.initialize_secondary()

    def _dict_init(self,property):
        for key in property.keys():
            self.__dict__[key] = property[key]

    def __getitem__(self, key):
        return self.__dict__[key]

    @staticmethod
    def get_suit_name(_name):
        for suit in ARTIFACT_LIST.keys():
            for name in ARTIFACT_LIST[suit]["element"]:
                if name == _name:
                    return suit

    @staticmethod
    def get_artifact_type(suit,name):
        for i in range(5):
            if name == ARTIFACT_LIST[suit]["element"][i]:
                return i

    @staticmethod
    def number_to_str(number):
        if number < 1 :
            number = number*100
            return ('%.1f'% number) + "%"
        else:
            return str(int(number))

    def get_random_main(self):
        return random.choice(ARTIFACT_PROPERTY[self.artifact_type]["property_list"])

    def get_random_secondary(self):
        temp_set = set(ARTIFACT_PROPERTY[5]["property_list"])
        temp_set = temp_set.difference({self.main})
        temp_set = temp_set.difference(set(self.get_all_secondary_name()))
        return random.choice(list(temp_set))

    def get_random_secondary_value(self,secondary_name):
        r = random.random()

        if r < SECONDARY_LEVEL_PROBABILITY[0]:
            return PROPERTY_LIST["secondary"][secondary_name]["level"][0]

        if r < ( SECONDARY_LEVEL_PROBABILITY[0] + SECONDARY_LEVEL_PROBABILITY[1] ):
            return PROPERTY_LIST["secondary"][secondary_name]["level"][1]

        if r < ( SECONDARY_LEVEL_PROBABILITY[0] + SECONDARY_LEVEL_PROBABILITY[1] + SECONDARY_LEVEL_PROBABILITY[2] ):
            return PROPERTY_LIST["secondary"][secondary_name]["level"][2]

        return PROPERTY_LIST["secondary"][secondary_name]["level"][3]

    def get_all_secondary_name(self):
        strengthen_secondary_list = [i["property"] for i in self.strengthen_secondary_list]
        temp_list = list(self.initial_secondary.keys())
        for i in strengthen_secondary_list:
            if not (i in temp_list):
                temp_list.append(i)
        return temp_list

    def get_main_value(self):
        if self.level == 20:
            return PROPERTY_LIST["main"][self.main]["max"]
        else:
            return PROPERTY_LIST["main"][self.main]["initial_value"] + self.level * PROPERTY_LIST["main"][self.main]["growth_value"]

    def get_secondary_property_value(self):
        secondary_property_value = {}
        for secondary in self.get_all_secondary_name():
            secondary_property_value[secondary] = 0
        for key in self.initial_secondary.keys():
            secondary_property_value[key] += self.initial_secondary[key]
        for i in self.strengthen_secondary_list:
            secondary_property_value[i["property"]] += i["value"]
        return secondary_property_value

    def initialize_secondary(self):
        number = random.randint(3,4)

        for _ in range(number):
            secondary = self.get_random_secondary()
            secondary_value = self.get_random_secondary_value(secondary)
            self.initial_secondary[secondary] = secondary_value

    def strengthen(self):

        if self.level >= 20:
            return

        self.level = self.level + 1
        secondary = ""
        secondary_value = 0
        strengthen_type = ""

        if self.level % 4 == 0:
            if len(self.initial_secondary) + len(self.strengthen_secondary_list) < 4:

                secondary = self.get_random_secondary()
                secondary_value = self.get_random_secondary_value(secondary)
                strengthen_type = "add"
                self.strengthen_secondary_list.append({"type": strengthen_type, "property": secondary, "value": secondary_value})

            else:
                temp_list = self.get_all_secondary_name()

                secondary = random.choice(temp_list)
                secondary_value = self.get_random_secondary_value(secondary)
                strengthen_type = "up"
                self.strengthen_secondary_list.append({"type": strengthen_type, "property": secondary, "value": secondary_value})

        return {"level":self.level,"strengthen_type":strengthen_type,"secondary":secondary,"secondary_value":secondary_value}

    def re_init(self):
        self._name_init(self.name)

    def get_artifact_dict(self):
        return self.__dict__

    def get_artifact_detail(self,start = 1):
        mes = self.get_artifact_CQ_code()
        mes += "\n\n"

        if start < 1:
            start = 1

        while start <= self.level:
            if (start % 4) == 0:
                strengthen_type = self.strengthen_secondary_list[int(start//4)-1]["type"]
                if strengthen_type == "up":
                    strengthen_type = "强化"
                else:
                    strengthen_type = "新增"

                secondary = self.strengthen_secondary_list[int(start//4)-1]["property"]
                secondary = PROPERTY_LIST["secondary"][secondary]["txt"]
                value = self.strengthen_secondary_list[int(start//4)-1]["value"]
                value = self.number_to_str(value)

                mes += f"第 {start} 级{strengthen_type}了 {secondary} ，强化值为 {value}\n"

            start += 1
        return mes

    def get_icon_path(self):
        name = f"{ARTIFACT_LIST[self.suit_name]['number']}_{self.artifact_type}.png"
        return os.path.join(FILE_PATH,"icon",name)

    def get_artifact_image(self):

        back = back_image.copy()

        icon = Image.open(self.get_icon_path())
        icon = icon.resize((180,180))

        icon_a = icon.getchannel("A")
        icon_a = ImageMath.eval("convert(a*b/256, 'L')", a=icon_a, b=icon_a)

        back.paste(icon, (220, 52), icon_a)

        draw = ImageDraw.Draw(back)
        main_property_value = self.get_main_value()
        secondary_property_value = self.get_secondary_property_value()
        draw.text((25, 10), self.name,                                       fill="#ffffffff",   font=ImageFont.truetype(ttf_path, size=28))
        draw.text((25, 60), ARTIFACT_PROPERTY[self.artifact_type]['name'],   fill="#ffffffff",   font=ImageFont.truetype(ttf_path, size=20))
        draw.text((25, 130), PROPERTY_LIST['main'][self.main]['txt'],        fill="#bfafa8",     font=ImageFont.truetype(ttf_path, size=20))
        draw.text((25, 153), self.number_to_str(main_property_value),        fill="#ffffffff",   font=ImageFont.truetype(ttf_path, size=32))
        draw.text((30, 260), f"+{self.level}",                               fill="#ffffffff",   font=ImageFont.truetype(ttf_path, size=18))

        x = 25
        y = 300
        for secondary in secondary_property_value.keys():
            name = PROPERTY_LIST["secondary"][secondary]["txt"]
            value = self.number_to_str( secondary_property_value[secondary] )
            draw.text((x, y), f"·{name}+{value}", fill="#495366", font=ImageFont.truetype(ttf_path, size=22))
            y += 32

        return back

    def get_artifact_CQ_code(self):
        image = self.get_artifact_image()
        bio = BytesIO()
        image.save(bio, format='PNG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()

        return f"[CQ:image,file={base64_str}]"



def calculate_strengthen_points(start = 1, end = 20):
    if end > 20:
        end = 20
    value = 0
    while start <= end:
        value += CONSUME_STRENGTHEN_POINTS[start]
        start += 1
    return value







