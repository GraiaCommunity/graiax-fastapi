from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graia.amnesia.builtins.asgi import UvicornASGIService
from graia.broadcast import Broadcast
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from httpx import AsyncClient
from launart import Launart, Service

from graiax.fastapi import FastAPIBehaviour, FastAPIService
from graiax.fastapi.saya.schema import RouteSchema

fastapi = FastAPI()

fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi.get("/main")
async def main():
    return "@fastapi.get('/main')"


def test_main():
    class MainLaunchable(Service):
        id = "test"

        @property
        def required(self):
            return set()

        @property
        def stages(self):
            return {"blocking"}

        async def launch(self, _: Launart):
            async with self.stage("blocking"):
                with saya.module_context():
                    channel = saya.require("tests.schema")

                assert len([c for c in channel.content if isinstance(c.metaclass, RouteSchema)]) == 4

                async with AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:9000/")
                    assert response.json() == {"code": 200, "message": "Hello World!"}
                    response = await client.get("http://127.0.0.1:9000/nothing")
                    assert response.status_code == 404

                with saya.module_context():
                    saya.reload_channel(channel)

                assert len([c for c in channel.content if isinstance(c.metaclass, RouteSchema)]) == 4

                async with AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:9000/")
                    assert response.json() == {"code": 200, "message": "Hello World!"}
                    response = await client.get("http://127.0.0.1:9000/nothing")
                    assert response.status_code == 404

                # launart.status.exiting = True

    launart = Launart()
    bcc = Broadcast()
    saya = Saya(bcc)
    saya.install_behaviours(FastAPIBehaviour(fastapi))
    saya.install_behaviours(BroadcastBehaviour(bcc))
    launart.add_component(FastAPIService(fastapi))
    launart.add_component(UvicornASGIService("127.0.0.1", 9000, {"": fastapi}))  # type: ignore
    launart.add_component(MainLaunchable())
    launart.launch_blocking()
