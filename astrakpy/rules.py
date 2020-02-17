from abc import ABC, abstractmethod
from astrakpy.models.message import Message
import typing


class AbstractRule(ABC):
    title = None

    @abstractmethod
    async def check(self, message: Message, check_param: typing.Any) -> bool:
        pass


class TextRule(AbstractRule):
    title = "text"

    async def check(self, message: Message, text: str) -> bool:
        return message.text.lower() == text


class TextContainsRule(AbstractRule):
    title = "text_contains"

    async def check(self, message: Message, text: typing.Any) -> bool:
        return text in [word.lower() for word in message.text.split()]


standart_rules = {TextRule.title: TextRule, TextContainsRule.title: TextContainsRule}
