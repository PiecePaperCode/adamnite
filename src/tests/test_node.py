import asyncio
import random
import unittest

from adamnite.account import PrivateAccount
from adamnite.blockchain import BlockChain
from adamnite.genesis import GENESIS_ACCOUNT, GENESIS_BLOCK
from adamnite.node import Node
from adamnite.peer import Peer, TIMEOUT
from adamnite.serialization import serialize
from adamnite.transaction import Transaction

PORT = random.randint(6101, 6299)


class TestNode(unittest.TestCase):

    def setUp(self) -> None:
        global PORT
        GENESIS_ACCOUNT.nonce = 1
        PORT = random.randint(6101, 7000)
        self.node = Node(port=PORT)
        self.node.block_chain = BlockChain(PrivateAccount(), GENESIS_BLOCK)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self.node.start_serving())

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

    def test_peers_synching_to_each_other(self):
        """
        A simulated network of 4 Nodes talking to each other.
        creating the node is necessary because the event loops need to be
        independent of each other on running tasks.
        """
        port2 = random.randint(6200, 6300)
        node2 = Node(port2)
        node2.peers.add(Peer('::ffff:127.0.0.1', PORT))
        node2.block_chain = BlockChain(GENESIS_ACCOUNT, GENESIS_BLOCK)
        receiver = PrivateAccount()
        node2.block_chain.pending_transactions.append(
            Transaction(
                sender=GENESIS_ACCOUNT,
                receiver=receiver.public_account(),
                amount=1
            )
        )
        node2.block_chain.pending_transactions.append(
            Transaction(
                sender=GENESIS_ACCOUNT,
                receiver=receiver.public_account(),
                amount=1
            )
        )
        self.loop.create_task(node2.start_serving())
        port3 = random.randint(6300, 6400)
        node3 = Node(port3)
        node3.peers.add(Peer('::ffff:127.0.0.1', port2))
        node3.block_chain = BlockChain(PrivateAccount(), GENESIS_BLOCK)
        self.loop.create_task(node3.start_serving())
        port4 = random.randint(6400, 6500)
        node4 = Node(port4)
        node4.peers.add(Peer('::ffff:127.0.0.1', port3))
        node4.block_chain = BlockChain(PrivateAccount(), GENESIS_BLOCK)
        self.loop.create_task(node4.start_serving())

        async def until():
            while len(self.node.connected_peers) < 3:
                await asyncio.sleep(0.5)

        self.loop.run_until_complete(asyncio.wait_for(until(), 20))
        self.assertEqual(1, node4.block_chain.height)
        self.assertEqual(0, len(node2.block_chain.pending_transactions))
        self.assertGreater(len(node4.connected_peers), 2)


async def connect(port=6101):
    conn = asyncio.open_connection("127.0.0.1", port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
        writer.write(serialize(0))
    except ConnectionError:
        raise ConnectionError
    return reader, writer
