import unittest

from adamnite.peer import Peer, ConnectedPeer


class TestPeer(unittest.TestCase):
    def test_peer(self):
        self.assertEqual(
            Peer("127.0.0.1", 6101),
            Peer("127.0.0.1", 6101)
        )
        self.assertNotEqual(
            Peer("127.0.0.1", 6101),
            Peer("127.0.0.1", 6102)
        )

    def test_connected_peer(self):
        self.assertEqual(
            ConnectedPeer(None, "127.0.0.1", 6101, None, None),
            ConnectedPeer(None, "127.0.0.1", 6101, None, None),
        )
        self.assertNotEqual(
            ConnectedPeer(None, "127.0.0.1", 6101, None, None),
            ConnectedPeer(None, "127.0.0.1", 6102, None, None),
        )

    def test_connected_peer_equals_peer(self):
        self.assertEqual(
            ConnectedPeer(None, "127.0.0.1", 6101, None, None),
            Peer("127.0.0.1", 6101)
        )
        self.assertNotEqual(
            ConnectedPeer(None, "127.0.0.1", 6101, None, None),
            Peer("127.0.0.1", 6102)
        )
        connected_peers = {ConnectedPeer(None, "127.0.0.1", 6101, None, None)}
        inside = Peer("127.0.0.1", 6101) in connected_peers
        self.assertTrue(inside)
        not_inside = Peer("127.0.0.1", 6102) in connected_peers
        self.assertFalse(not_inside)
