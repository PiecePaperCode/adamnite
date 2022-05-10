import asyncio
import aioconsole

from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from adamnite.account import Wallet, PublicAccount
from adamnite.node import Node
from adamnite.transaction import Transaction


class CommandLine:
    def __init__(self, node: Node):
        self.node = node
        self.wallet = Wallet(self.node.block_chain)
        self.loop = asyncio.get_event_loop()
        self.layout = Layout()

        self.layout.split(
            Layout(name="header", size=2),
            Layout(size=4, name="main"),
            Layout(size=2, name="address"),
            Layout(size=2, name="sender"),
        )
        self.layout["header"].update(
            Text("Adamnite CLI Client", justify="left", style='red')
        )
        self.layout["main"].split(
            Text(f"Balance 0"),
            Text(f"Connections 0"),
            Text(f"Block Height 0"),
        )
        self.layout["address"].update(
            Text(
                f"Receive Adress {Wallet.accounts[0].public_account().address}",
                justify="left"
            ),
        )
        self.layout['sender'].split(
            Text("Send [1] + Enter", style='blue'),
        )

    async def start_serving(self):
        self.loop.create_task(self.update_stats())
        self.loop.create_task(self.transaction_sender())

    async def update_stats(self):
        with Live(
                self.layout,
                refresh_per_second=1,
        ):
            while True:
                self.layout["main"].split(
                    Text(f"Balance {self.wallet.balance()}"),
                    Text(f"Connections {len(self.node.connected_peers)}"),
                    Text(f"Block Height {self.node.block_chain.height}"),
                )
                await asyncio.sleep(5)

    async def transaction_sender(self):
        self.layout['sender'].split(
            Text("Send [1] + Enter", style='blue'),
        )
        selection = await aioconsole.ainput()
        if selection != '1':
            self.loop.create_task(self.transaction_sender())
            return
        self.layout["sender"].split(
            Text("Type your Amount?", style='blue'),
        )
        amount = await aioconsole.ainput()
        self.layout["sender"].split(
            Text(f"send {amount} NITE to", style='blue'),
            Text(f"type receiver address and press Enter", style='blue'),
        )
        receiver = await aioconsole.ainput()
        self.layout["sender"].split(
            Text(f"send {amount} NITE to {receiver}", style='blue'),
            Text(f"Send[1] Abord[9]", style='blue'),
        )
        selection = await aioconsole.ainput()
        if selection == '9':
            self.loop.create_task(self.transaction_sender())
            return
        self.node.block_chain.pending_transactions.append(
            Transaction(
                sender=Wallet.accounts[0],
                receiver=PublicAccount(address=bytes(receiver, 'utf-8')),
                amount=int(amount)
            )
        )
        Wallet().export_wallet('resources/wallet.nite')
        self.loop.create_task(self.transaction_sender())
