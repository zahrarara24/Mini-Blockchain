from chain import Block, BlockHeader, mine_block, validate_chain, merkle_root, merkle_proof, verify_proof
import time, argparse

def sample_txs():
    return [
        {"from":"Alice","to":"Bob","amt":10},
        {"from":"Bob","to":"Carol","amt":5},
        {"from":"Carol","to":"Dave","amt":2},
        {"from":"Dave","to":"Alice","amt":1},
    ]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--difficulty", type=int, default=3)
    args = ap.parse_args()

    genesis = Block(BlockHeader(0, time.time(), "0"*64, "0"*64, 0, args.difficulty), [])
    txs = sample_txs()
    blk = mine_block(genesis, txs, difficulty=args.difficulty)
    chain = [genesis, blk]

    root = merkle_root(txs)
    proof_T3 = merkle_proof(txs, 2)

    print("\n=== Transactions in Block ===")
    for tx in txs:
        print(f" From: {tx['from']}  ->  To: {tx['to']}  Amount: {tx['amt']}")

    print("\n=== Block Information ===")
    print("Block hash:", blk.header.hash())
    print("Valid chain?", validate_chain(chain))
    print("Merkle root:", root)
    print("Proof(T3):", proof_T3)
    print("Verify T3:", verify_proof(txs[2], proof_T3, root))
