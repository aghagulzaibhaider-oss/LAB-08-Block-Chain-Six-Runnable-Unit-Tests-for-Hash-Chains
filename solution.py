#!/usr/bin/env python3
"""Week 08: integrated blockchain validation using Python's unittest.

Run (Linux / Colab cell):
    python3 solution.py                                   # all 6 tests
    python3 solution.py ReviewTests.test_tamper_rejected  # one test
"""
import hashlib, json, unittest


def hash_block(b):
    """SHA-256 of a block. sort_keys=True makes the JSON (and hash) deterministic."""
    return hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()


def create_chain():
    """Build a 3-block chain: genesis -> issue C-001 -> revoke C-001."""
    blocks = []
    previous = '0' * 64                      # genesis has no parent: 64 zeros
    for height, text in enumerate(['genesis', 'issue C-001', 'revoke C-001']):
        b = {'height': height, 'previous_hash': previous, 'event': text}
        b['hash'] = hash_block(b)            # hash is computed WITHOUT the 'hash' field
        blocks.append(b)
        previous = b['hash']                 # next block links to this one
    return blocks


def verify(blocks):
    """True only if every block's hash is correct AND every link matches."""
    for i, b in enumerate(blocks):
        body = {k: v for k, v in b.items() if k != 'hash'}
        if hash_block(body) != b['hash']:    # check 1: data was not modified
            return False
        if i and b['previous_hash'] != blocks[i - 1]['hash']:  # check 2: link intact
            return False
    return True


class ReviewTests(unittest.TestCase):
    def test_valid_chain(self):
        self.assertTrue(verify(create_chain()))

    def test_tamper_rejected(self):          # negative test: change data
        chain = create_chain()
        chain[1]['event'] = 'issue C-999'
        self.assertFalse(verify(chain))

    def test_broken_link_rejected(self):     # negative test: break the link
        chain = create_chain()
        chain[2]['previous_hash'] = 'fake'
        self.assertFalse(verify(chain))

    def test_chain_length(self):             # extension 1
        self.assertEqual(len(create_chain()), 3)

    def test_genesis_previous_hash(self):    # extension 2
        self.assertEqual(create_chain()[0]['previous_hash'], '0' * 64)

    def test_hash_is_repeatable(self):       # determinism
        self.assertEqual(hash_block({'x': 1}), hash_block({'x': 1}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
