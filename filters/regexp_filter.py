from aiogram.filters import BaseFilter
from aiogram.types import Message
import re

class RegFilter(BaseFilter):  # [1]
    def __init__(self, reg: re.Pattern): # [2]
        self.reg = reg

    async def __call__(self, message: Message) -> bool:  # [3]
        return self.reg.match(message.text)