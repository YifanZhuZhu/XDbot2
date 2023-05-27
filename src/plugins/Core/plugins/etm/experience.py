from .item import Item
from . import exp

class Experience(Item):
    def on_register(self):
        self.item_id = "exp"
        self.data = {
            "display_name": "VimCoin",
            "display_message": "XDbot2 通用货币"
        }
        if self.user_id:
            exp.add_exp(self.user_id, self.count)
            self.count = 0
        
