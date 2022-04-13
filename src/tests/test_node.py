import asyncio
import random
import unittest

from adamnite.node import Node, TIMEOUT
from adamnite.serialization import BYTE_ORDER, INT_SIZE


PORT = random.randint(6101, 6198)


class TestNode(unittest.TestCase):
    node = Node(port=PORT)
    loop = asyncio.get_event_loop()
    loop.create_task(node.start_serving())

    def test_server_serving(self):
        async def run_test(port=PORT):
            try:
                await connect(port)
            except ConnectionError:
                return False
            return True
        self.assertTrue(self.loop.run_until_complete(run_test()))
        self.assertFalse(self.loop.run_until_complete(run_test(6199)))
        self.assertTrue(0 < len(self.node.peers))
        self.assertEqual(self.node.export_peers()[0].ip, '::ffff:127.0.0.1')

    def test_peer_responding(self):
        async def run_test():
            reader, writer = await connect(PORT)
            size = 4
            writer.write(size.to_bytes(INT_SIZE, BYTE_ORDER))
            writer.write(b'PING')
            message = await asyncio.wait_for(reader.read(4), timeout=TIMEOUT)
            return message
        self.assertEqual(self.loop.run_until_complete(run_test()), b'PONG')


async def connect(port=6101):
    conn = asyncio.open_connection("127.0.0.1", port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
    except ConnectionError:
        raise ConnectionError
    return reader, writer
