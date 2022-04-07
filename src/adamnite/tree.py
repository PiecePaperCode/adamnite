import hashlib


# https://en.wikipedia.org/wiki/Merkle_tree#/media/File:Hash_Tree.svg
def merkle_tree(data_blocks: list):
    root: [bytes] = [
        hash_sha512(of=item)
        for item in data_blocks
    ]
    while len(root) != 1:
        level = []
        if not even(len(root)):
            root.append(root[-1])
        for i in range(0, len(root), 2):
            leaf = hash_sha512(
                root[i] + root[i + 1]
            )
            level.append(bytes(leaf))
        root = level
    return root.pop()


def radix_tree():
    return {}



def even(number):
    if number % 2 == 0:
        return True
    else:
        return False
