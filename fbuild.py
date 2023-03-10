import asyncio
from asyncio.subprocess import PIPE, DEVNULL
from contextlib import closing
import sys

async def log_stream(stream: asyncio.StreamReader):
    while not stream.at_eof():
        print((await stream.readline()).decode("utf-8"), end='')

async def run():
    process = await asyncio.create_subprocess_exec(
        "FBuild.exe",
        *sys.argv[1:],
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=PIPE)

    await asyncio.create_task(log_stream(process.stdout))
    print('stdout closed')

    return await process.wait()  # wait for the child process to exit


loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)
with closing(loop):
    loop.run_until_complete(run())
