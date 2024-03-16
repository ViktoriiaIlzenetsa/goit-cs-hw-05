import argparse
import asyncio
import logging

from aiopath import AsyncPath
from aioshutil import copyfile

parser = argparse.ArgumentParser(description = "Copy file in folder")
parser.add_argument("-s", "--source", required = True)
parser.add_argument("-o", "--output", default = "dist")
args = vars(parser.parse_args())

source = AsyncPath(args["source"])
output = AsyncPath(args["output"])

async def read_folder(path):
    async for file in path.iterdir():
        if await file.is_dir():
            await read_folder(file)
        else:
            await copy_file(file)


async def copy_file(file):
    folder = output / file.name.split('.')[-1]
    try:
        await folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, folder/ file.name)
    except OSError as e:
        logging.error(e)

if __name__ == "__main__":
    format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    asyncio.run(read_folder(source))
    
    print(f"All files copied to {output}")

