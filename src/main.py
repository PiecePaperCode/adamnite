import asyncio
import logging
import os

from adamnite.node import Node, Peer

logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    port = 6101
    if "PORT" in os.environ:
        port = int(os.environ['PORT'])
    node = Node(port=port)
    loop = asyncio.get_event_loop()
    loop.create_task(node.start_serving())
    loop.run_forever()
