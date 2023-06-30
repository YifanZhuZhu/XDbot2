from . import economy
import random
from .item import Item
from .. import _lang
from . import achievement, buff


class Dice(Item):
    def on_register(self):
        self.item_id = "dice"
        self.basic_data = {
            "display_name": "二十面骰子",
            "display_message": "打开后随机获得：50vi ~ -50vi",
            "maximum_stack": 32,
            "int": None
        }

    def use_item(self):
        user_id = self.user_id
        c = self.data["int"]*10+3 or random.randint(1, 200)
        if 192 <= c <= 200: # 20
            economy.add_vi(user_id, 50)
            return _lang.text("dice.20", [], self.user_id)
        elif 183 <= c <= 191: # 18-19
            economy.add_vi(user_id, 20)
            return _lang.text("dice.18..19", [random.randint(18,19)], self.user_id)
        elif 153 <= c <= 182: # 15-17
            economy.add_vi(user_id, 10)
            return _lang.text("dice.15..17", [random.randint(15,17)], self.user_id)
        elif 106 <= c <= 152: # 10-14
            economy.add_vi(user_id, 5)
            return _lang.text("dice.10..14", [random.randint(10,14)], self.user_id)
        elif 16 <= c <= 105: # 2-9
            return _lang.text("dice.2..9", [random.randint(2,9)], self.user_id)
        elif c <= 15: # 1
            achievement.increase_unlock_progress("什么欧皇", user_id)
            if buff.can_effect(user_id, "护符") and random.random() <= 0.75:
                buff.effect_buff(user_id, "护符")
                return _lang.text("dice.1-1", [1], self.user_id)
            else:
                economy._add_vi(user_id, -50)
                return _lang.text("dice.1-2", [1], self.user_id)
        elif c == -1:
            achievement.unlock("特性！特性", user_id)
            return _lang.text("dice.else", [c], self.user_id)
        else:
            # 笑死怎么可能掷出来啊（（（
            return _lang.text("dice.else", [c], self.user_id)
