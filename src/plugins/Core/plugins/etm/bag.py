from . import items
import json
from .item_basic_data import BASIC_DATA
from nonebot_plugin_apscheduler import scheduler
from nonebot import require

require("nonebot_plugin_apscheduler")
bags = {}# items.json2items(json.load(open("data/etm/bags.json")))

def get_bags():
    data = json.load(open("data/etm/bags.json"))
    for user, bag in list(data.items()):
        bags[user] = items.json2items(bag, user)
get_bags()

@scheduler.scheduled_job("cron", second="*/30", id="save_bags")
def save_bags():
    bag_data = {}
    for user_id, bag in list(bags.items()):
        bag_data[user_id] = []
        for item in bag:
            if item.count > 0:
                # 处理nbt
                nbt = item.data.copy()
                for key in list(BASIC_DATA.keys()):
                    try:
                        if nbt[key] == BASIC_DATA[key]:
                            nbt.pop(key)
                    except BaseException:
                        pass
                for key in list(item.basic_data.keys()):
                    try:
                        if nbt[key] == item.basic_data[key]:
                            nbt.pop(key)
                    except BaseException:
                        pass
                bag_data[user_id].append({
                    "id": item.item_id,
                    "count": item.count,
                    "data": nbt.copy()
                })
    json.dump(bag_data, open("data/etm/bags.json", "w"))
    get_bags()
    
def get_user_bag(user_id):
    try:
        return bags[user_id]
    except KeyError:
        bags[user_id] = []
        return bags[user_id]

def _add_item(user_id, item):
    try:
        bags[user_id].append(item)
    except KeyError:
        bags[user_id] = [item]

def add_item(user_id, item_id, item_count = 1, item_data = {}):
    try:
        for item in bags[user_id]:
            if item.item_id == item_id:
                item_count -= item.add(item_count, item_data)
        if item_count > 0:
            _add_item(user_id, items.ITEMS[item_id](item_count, item_data, user_id))
    except KeyError:
        bags[user_id] = []
        add_item(user_id, item_id, item_count, item_data)

def use_item(user_id, item_pos, count, argv = ""):
    return bags[user_id][item_pos].use(count, argv)
