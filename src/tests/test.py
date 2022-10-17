import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graia.amnesia.builtins.uvicorn import UvicornService
from graia.saya import Saya
from launart import Launart, Launchable

from graiax.fastapi import FastAPIBehaviour, FastAPIService

launart = Launart()
saya = Saya()
fastapi = FastAPI()

fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

saya.install_behaviours(FastAPIBehaviour(fastapi))

with saya.module_context():
    saya.require("tests.schema")


@fastapi.get("/main")
async def main():
    return "main"


class Test(Launchable):
    id = "test"

    @property
    def required(self):
        return set()

    @property
    def stages(self):
        return {"blocking"}

    async def launch(self, _: Launart):
        async with self.stage("blocking"):
            await asyncio.sleep(10)


launart.add_service(FastAPIService(fastapi))
launart.add_service(UvicornService())
launart.add_launchable(Test())

launart.launch_blocking()
