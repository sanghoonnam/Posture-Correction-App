import asyncio
from asyncio import AbstractEventLoop
from typing import Optional

from dingtalkchatbot.chatbot import DingtalkChatbot


class DingBot:
    """Ding bot"""

    def __init__(
            self,
            token: str,
            loop: Optional[AbstractEventLoop] = None
    ):
        """
        :param token:
        :param loop:
        """
        self._loop = loop or asyncio.get_event_loop()
        self.bot = DingtalkChatbot(f'https://oapi.dingtalk.com/robot/send?access_token={token}')

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    async def send(self, title: str, text: str) -> None:
        """
        Send something to bot
        :param title: str
        :param text: str
        :return: None
        """
        await self.loop.run_in_executor(None, self.bot.send_markdown, title, text)


async def main() -> None:
    """unit test"""
    bot = DingBot('token')
    await bot.send('Hello world', '### Hello world\n'
                                  '> I sand massage to ding talk. Wonderful!!!')


if __name__ == '__main__':
    asyncio.run(main())
