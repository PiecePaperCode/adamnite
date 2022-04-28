import asyncio
import os

from adamnite.cli import CommandLine
from adamnite.node import Node


if __name__ == '__main__':
    port = 6102
    if "PORT" in os.environ:
        port = int(os.environ['PORT'])
    node = Node(port=port)
    loop = asyncio.get_event_loop()
    loop.create_task(node.start_serving())
    cli = CommandLine(node)
    loop.create_task(cli.start_serving())
    loop.run_forever()
