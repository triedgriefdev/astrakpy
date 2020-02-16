from astrakpy.exceptions import AstrakError, AstrakServerSideError
from astrakpy.longpoll.longpoll import LongPoll
from aiohttp import ClientSession, ClientError
import asyncio
import ujson


class AstrakPy:
    def __init__(self, login: str = None, password: str = None, token: str = None):
        self.url = "http://afternoon-dusk-97603.herokuapp.com/"
        self.loop = asyncio.get_event_loop()
        self.login = login
        self.password = password
        self.token = token

    async def api_method(self, method: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        async with ClientSession(json_serialize=ujson.dumps) as client:
            async with client.post(
                self.url + method, data={"token": self.token, **params}
            ) as rq:
                try:
                    resp = await rq.json()
                    try:
                        if resp["code"] < 0:
                            raise AstrakError(f"[{resp['code']}] {resp['response']}")
                    except KeyError:
                        return resp
                except ClientError:
                    raise AstrakServerSideError(
                        "Something was wrong... Seems like server-side error."
                    )

    async def auth(self):
        if self.login is None:
            raise AstrakError("Login was None.")
        if self.password is None:
            raise AstrakError("Password was None.")

        self.token = (
            await self.api_method(
                "users/login", {"username": self.login, "password": self.password}
            )
        )["token"]

    def get_longpoll(self):
        return LongPoll(self)
