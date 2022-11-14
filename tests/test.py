from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graia.amnesia.builtins.uvicorn import UvicornService
from graia.saya import Saya
from httpx import AsyncClient
from launart import Launart, Launchable

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
    return "main"


def test_main():
    class MainLaunchable(Launchable):
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
                assert (
                    len(
                        [
                            c
                            for c in channel.content
                            if isinstance(c.metaclass, RouteSchema)
                        ]
                    )
                    == 3
                )
                async with AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:8000/")
                    assert response.json() == {"code": 200, "message": "Hello World!"}
                    response = await client.get("http://127.0.0.1:8000/nothing")
                    assert response.status_code == 404
                with saya.module_context():
                    saya.reload_channel(channel)
                assert (
                    len(
                        [
                            c
                            for c in channel.content
                            if isinstance(c.metaclass, RouteSchema)
                        ]
                    )
                    == 3
                )
                async with AsyncClient() as client:
                    response = await client.get("http://127.0.0.1:8000/")
                    assert response.json() == {"code": 200, "message": "Hello World!"}
                    response = await client.get("http://127.0.0.1:8000/nothing")
                    assert response.status_code == 404

    launart = Launart()
    saya = Saya()
    saya.install_behaviours(FastAPIBehaviour(fastapi))
    launart.add_service(FastAPIService(fastapi))
    launart.add_service(UvicornService())
    launart.add_launchable(MainLaunchable())
    launart.launch_blocking()
