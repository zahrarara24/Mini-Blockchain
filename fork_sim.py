# fork_sim.py
from dataclasses import dataclass
from typing import Dict, List, Optional
import time, json
from chain import Block, BlockHeader, mine_block, validate_block, merkle_root

# --- util "work": hitung jumlah nol heksadesimal di prefix hash, sebagai proxy work
def count_leading_hex_zero_nibbles(hexhash: str) -> int:
    n = 0
    for ch in hexhash:
        if ch == "0": 
            n += 1
        else: 
            break
    return n

def block_hash(b: Block) -> str:
    return b.header.hash()

def approx_block_work(b: Block) -> int:
    # proxy: semakin banyak '0' diawal hash, semakin besar "work"-nya
    return 16 ** count_leading_hex_zero_nibbles(block_hash(b))

@dataclass
class Node:
    blk: Block
    parent: Optional[str]    # hash parent
    work: int    # work blok ini
    cum_work: int    # work kumulatif dari genesis → blk

class ForkSim:
    def __init__(self, difficulty: int):
        # Genesis
        self.genesis = Block(BlockHeader(0, time.time(), "0"*64, "0"*64, 0, difficulty), [])
        ghash = block_hash(self.genesis)
        gnode = Node(self.genesis, None, approx_block_work(self.genesis), approx_block_work(self.genesis))
        self.nodes: Dict[str, Node] = { ghash: gnode }
        self.best_tip = ghash
        self.difficulty = difficulty

    def add_child(self, parent_hash: str, txs: List[dict]) -> str:
        parent = self.nodes[parent_hash].blk
        child = mine_block(parent, txs, difficulty=self.difficulty)
        assert validate_block(parent, child), "invalid child mined"
        chash = block_hash(child)
        work = approx_block_work(child)
        cum = self.nodes[parent_hash].cum_work + work
        self.nodes[chash] = Node(child, parent_hash, work, cum)
        
        # pilih tip terbaik (cum_work terbesar; tie-break: hash lexicographically)
        if (cum > self.nodes[self.best_tip].cum_work) or \
           (cum == self.nodes[self.best_tip].cum_work and chash < self.best_tip):
            self.best_tip = chash
        return chash

    def path_to_genesis(self, tip_hash: str) -> List[str]:
        path = []
        h = tip_hash
        while h:
            path.append(h)
            h = self.nodes[h].parent if h in self.nodes else None
        return list(reversed(path))  # genesis → tip

    def best_chain(self) -> List[str]:
        return self.path_to_genesis(self.best_tip)

def sample_txs(tag: str):
    # variasi kecil di payload agar hash blok berbeda
    return [
        {"from":"Alice","to":"Bob","amt":10,"tag":tag},
        {"from":"Bob","to":"Carol","amt":5,"tag":tag},
        {"from":"Carol","to":"Dave","amt":2,"tag":tag},
        {"from":"Dave","to":"Alice","amt":1,"tag":tag},
    ]

if __name__ == "__main__":
    sim = ForkSim(difficulty=3)
    g = sim.path_to_genesis(sim.best_tip)[0]  # hash genesis
    print("Genesis:", g[:12], "...")

    # === STEP 1: Dua cabang dari genesis (fork 1-blok) ===
    a1 = sim.add_child(g, sample_txs("A1"))
    b1 = sim.add_child(g, sample_txs("B1"))
    print("\nSetelah 2 cabang dari genesis:")
    print(" Tip A1:", a1[:12], "work:", sim.nodes[a1].work, "cum:", sim.nodes[a1].cum_work)
    print(" Tip B1:", b1[:12], "work:", sim.nodes[b1].work, "cum:", sim.nodes[b1].cum_work)
    print(" Best tip:", sim.best_tip[:12])
    print(" Best chain (genesis→tip):")
    for h in sim.best_chain():
        print(" ", h[:12])

    # === STEP 2: Tambah 1 blok lagi di cabang B (harus memicu REORG jika B menang kumulatif) ===
    b2 = sim.add_child(b1, sample_txs("B2"))
    print("\nSetelah B menambah 1 blok lagi (B2):")
    print(" Tip B2:", b2[:12], "work:", sim.nodes[b2].work, "cum:", sim.nodes[b2].cum_work)
    print(" Best tip:", sim.best_tip[:12], "(REORG terjadi jika best tip pindah dari A1 ke B2)")
    print(" Best chain (genesis→tip):")
    for h in sim.best_chain():
        print(" ", h[:12])