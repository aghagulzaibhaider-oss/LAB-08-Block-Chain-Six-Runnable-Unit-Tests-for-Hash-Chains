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

#Step 2: Run the full test suite
!python3 solution.py
#Expected: Ran 6 tests ... OK

#Step 3: Run one test on its own
!python3 solution.py ReviewTests.test_tamper_rejected
!python3 solution.py ReviewTests.test_chain_length
#Expected: Ran 1 test ... OK for each.

#Step 4: Syntax check
!python3 -m py_compile solution.py && echo "Syntax OK"
#This only checks syntax, not behavior.

#Step 5: See the chain and the tampering yourself
from solution import create_chain, verify
import pprint

chain = create_chain()
pprint.pprint(chain)
print("Valid before tampering:", verify(chain))

chain[1]['event'] = 'issue C-999'      # tamper with block 1
print("Valid after tampering :", verify(chain))

chain = create_chain()
chain[2]['previous_hash'] = 'fake'     # break the link
print("Valid after broken link:", verify(chain))
#Expected: True, then False, then False.

#Step 6: Save a transcript for submission
!python3 solution.py > transcript.txt 2>&1
!cat transcript.txt
#unittest writes its summary to stderr, so 2>&1 is needed to capture it. Download transcript.txt from the Colab file panel on the left.

#Step 7: Cell 2: Result table as an image (optional)
import matplotlib.pyplot as plt

rows = [
    ["test_valid_chain", "pass", "pass"],
    ["test_tamper_rejected", "pass", "pass"],
    ["test_broken_link_rejected", "pass", "pass"],
    ["test_chain_length", "pass", "pass"],
    ["test_genesis_previous_hash", "pass", "pass"],
    ["test_hash_is_repeatable", "pass", "pass"],
]
fig, ax = plt.subplots(figsize=(8, 2.6))
ax.axis("off")
t = ax.table(cellText=rows, colLabels=["Test", "Expected", "Actual"], loc="center", cellLoc="center")
t.auto_set_font_size(False); t.set_fontsize(10); t.scale(1, 1.4)
plt.savefig("result_table.png", dpi=150, bbox_inches="tight")
plt.show()

#Run both after your earlier cells, so solution.py already exists. Then put the images in your PDF 
#under the test output. Use either the diagram or the table; the lab only asks for one 
#("result table/diagram"), but including both is fine.


