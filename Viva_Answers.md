# Lab 08 – Viva Questions and Answers

**Name:** ______________________  **ID:** ______________

## Q1. Why run negative tests?
Negative tests show that the validation code rejects invalid states, not only that it accepts valid ones.
In this lab, `test_tamper_rejected` and `test_broken_link_rejected` prove that changing block data or
breaking a previous-hash link makes `verify()` return `False`. A verifier that only passed valid chains
could still wrongly accept tampered ones, so negative tests are needed to trust it.

## Q2. Do six tests prove consensus?
No. The six tests only check properties of one local three-block chain: hashing, linking, length and
tamper detection. They do not model multiple peers, malicious (Byzantine) participants, network delays,
agreement between nodes, or economic finality, which are what consensus depends on.

## Q3. Which earlier weeks are covered?
- Weeks 2 and 3: blocks and hashes (the structure and hashing used in this lab).
- Week 4: propagation risks (why tampering and bad data must be detected).
- Week 7: different permission models (the lab's chain is a simple local, permissionless-style example).
