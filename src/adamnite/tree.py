from adamnite.crypto import sha512


# https://en.wikipedia.org/wiki/Merkle_tree#/media/File:Hash_Tree.svg
def merkle_tree(data_blocks: list):
    root: [bytes] = [
        sha512(of=item)
        for item in data_blocks
    ]
    while len(root) != 1:
        level = []
        if not len(root) % 2 == 0:
            root.append(root[-1])
        for i in range(0, len(root), 2):
            leaf = sha512(
                root[i] + root[i + 1]
            )
            level.append(bytes(leaf))
        root = level
    return root.pop()


def radix_tree():
    return {}
