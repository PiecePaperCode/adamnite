import asyncio
import os

from adamnite.node import Node

if __name__ == '__main__':
    port = 6109
    if "PORT" in os.environ:
        port = int(os.environ['PORT'])
    node = Node(port=port)
    loop = asyncio.get_event_loop()
    loop.create_task(node.start_serving())
    loop.run_forever()
