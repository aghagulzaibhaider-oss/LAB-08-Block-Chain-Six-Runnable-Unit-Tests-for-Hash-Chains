# Lab 08 – Six Runnable Unit Tests for Hash Chains

**Course:** Introduction to Blockchain
**Name:** ______________________  **ID:** ______________

## Purpose
This lab uses Python's built-in `unittest` module to check basic blockchain properties on a local
three-block chain (genesis -> issue C-001 -> revoke C-001). The tests show that a valid chain passes,
modified data fails, a broken previous-hash link fails, and the hash function is deterministic.

## Files
| File | Description |
|---|---|
| `solution.py` | Hash function, chain builder, verifier and six unit tests |
| `Lab_08_Colab.ipynb` | Optional ready-made Colab notebook |
| `transcript.txt` | Captured test output (stdout + stderr) |
| `chain_diagram.png` | Diagram of the three linked blocks |
| `result_table.png` | Table of test results |
| `Viva_Answers.md` | Answers to the three viva questions |

## How it works
- `hash_block(b)`: SHA-256 of the block as JSON with sorted keys, so the same block always gives the same hash.
- `create_chain()`: builds 3 blocks. Genesis has `previous_hash` of 64 zeros; each later block stores the previous block's hash.
- `verify(blocks)`: for every block, (1) recompute the hash and compare it with the stored hash, (2) check that `previous_hash` matches the previous block's hash. Returns `True` only if all checks pass.

## Tests
| Test | Checks |
|---|---|
| `test_valid_chain` | Untouched chain verifies (True) |
| `test_tamper_rejected` | Changed event data is detected (False) |
| `test_broken_link_rejected` | Broken previous-hash link is detected (False) |
| `test_chain_length` | Chain has exactly 3 blocks (extension) |
| `test_genesis_previous_hash` | Genesis previous hash is 64 zeros (extension) |
| `test_hash_is_repeatable` | Same input gives the same hash |

## How to run (Google Colab or Linux)
```
python3 solution.py                                   # all 6 tests
python3 solution.py ReviewTests.test_tamper_rejected  # one test
python3 -m py_compile solution.py                     # syntax check only
python3 solution.py > transcript.txt 2>&1             # save transcript (unittest writes to stderr)
```
In Colab, put `!` before each command and create the file first with `%%writefile solution.py`.

## Expected result
```
Ran 6 tests ... OK
```

## Notes
- Educational/simulated chain only. It does not model peers, consensus, network delays or finality.
- `py_compile` checks syntax only, not behaviour.
