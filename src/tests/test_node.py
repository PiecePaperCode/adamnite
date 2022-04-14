import asyncio
import random
import unittest

from adamnite.node import Node
from adamnite.peer import Peer, TIMEOUT
from adamnite.serialization import serialize

PORT = random.randint(6101, 6199)


class TestNode(unittest.TestCase):
    node = Node(port=PORT)
    node.peers = {Peer('::ffff:127.0.0.1', PORT)}
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
        self.assertTrue(0 < len(self.node.connected_peers))
        self.assertEqual(self.node.export_peers()[0].ip, '::ffff:127.0.0.1')

    def test_peers_finding_each_other(self):
        port2 = random.randint(6200, 6300)
        node2 = Node(port2)
        node2.peers.add(Peer('::ffff:127.0.0.1', PORT))
        self.loop.create_task(node2.start_serving())
        port3 = random.randint(6300, 6400)
        node3 = Node(port3)
        node3.peers.add(Peer('::ffff:127.0.0.1', port2))
        self.loop.create_task(node3.start_serving())
        port4 = random.randint(6400, 6500)
        node4 = Node(port4)
        node4.peers.add(Peer('::ffff:127.0.0.1', port3))
        self.loop.create_task(node4.start_serving())

        async def until():
            while len(self.node.connected_peers) != 3:
                await asyncio.sleep(TIMEOUT)

        self.loop.run_until_complete(asyncio.wait_for(until(), 20))
        self.assertEqual(len(self.node.connected_peers), 3)


async def connect(port=6101):
    conn = asyncio.open_connection("127.0.0.1", port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
        writer.write(serialize(0))
    except ConnectionError:
        raise ConnectionError
    return reader, writer
