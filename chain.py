 # chain.py
import hashlib, time, json
from dataclasses import dataclass
from typing import List

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def merkle_root(txs: List[dict]) -> str:
    # Daun = SHA-256(JSON tx, sort keys)
    level = [sha256_hex(json.dumps(tx, sort_keys=True).encode()) for tx in txs] or ["0"*64]
    # TODO: jika jumlah ganjil, duplikasi daun terakhir
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])  # duplikasi daun terakhir
        nxt = []
        for i in range(0, len(level), 2):
            left = bytes.fromhex(level[i])
            right = bytes.fromhex(level[i+1])
            nxt.append(sha256_hex(left + right))
        level = nxt
    return level[0]

@dataclass
class BlockHeader:
    index: int
    timestamp: float
    prev_hash: str
    merkle_root: str
    nonce: int
    difficulty: int

    def hash(self) -> str:
        data = f"{self.index}|{self.timestamp:.6f}|{self.prev_hash}|{self.merkle_root}|{self.nonce}|{self.difficulty}"
        return sha256_hex(data.encode())

@dataclass
class Block:
    header: BlockHeader
    txs: List[dict]

def mine_block(prev: Block, txs: List[dict], difficulty: int) -> Block:
    root = merkle_root(txs)
    nonce = 0
    target = "0"*difficulty
    while True:
        hdr = BlockHeader(
            index=prev.header.index + 1,
            timestamp=time.time(),
            prev_hash=prev.header.hash(),
            merkle_root=root,
            nonce=nonce,
            difficulty=difficulty
        )
        h = hdr.hash()
        if h.startswith(target):
            return Block(hdr, txs)
        nonce += 1  # bukti kerja sederhana

def validate_block(prev: Block, blk: Block) -> bool:
    # Link prev
    if blk.header.prev_hash != prev.header.hash(): 
        return False
    # PoW
    if not blk.header.hash().startswith("0"*blk.header.difficulty): 
        return False
    # Merkle
    if blk.header.merkle_root != merkle_root(blk.txs): 
        return False
    return True

def validate_chain(chain: List[Block]) -> bool:
    for i in range(1, len(chain)):
        if not validate_block(chain[i-1], chain[i]): 
            return False
    return True

# Tambahkan ke chain.py
from typing import Tuple

def merkle_proof(txs: List[dict], index: int):
    """Return list of (sibling_hash, position) from leaf->root.
    position: 'left' atau 'right' relatif terhadap hash yang kita pegang."""
    if not txs: 
        return []
    
    # Bangun level daun (hash tx) sambil simpan jejak indeks
    level = [sha256_hex(json.dumps(tx, sort_keys=True).encode()) for tx in txs]
    idx = index
    proof = []
    
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        
        pair_idx = idx ^ 1
        position = "right" if pair_idx > idx else "left"
        sibling = level[pair_idx]
        proof.append((sibling, position))
        
        # Naik level
        idx //= 2
        nxt = []
        for i in range(0, len(level), 2):
            nxt.append(sha256_hex(bytes.fromhex(level[i]) + bytes.fromhex(level[i+1])))
        level = nxt
    
    return proof

def verify_proof(leaf_tx: dict, proof: List[Tuple[str,str]], root_hex: str) -> bool:
    digest = sha256_hex(json.dumps(leaf_tx, sort_keys=True).encode())
    for sib, pos in proof:
        if pos == "right":
            digest = sha256_hex(bytes.fromhex(digest) + bytes.fromhex(sib))
        else: # 'left'
            digest = sha256_hex(bytes.fromhex(sib) + bytes.fromhex(digest))
    return digest == root_hex

# Demo minimal 
if __name__ == "__main__":
    genesis = Block(BlockHeader(0, time.time(), "0"*64, "0"*64, 0, 4), [])
    txs = [
        {"from":"Alice","to":"Bob","amt":10},
        {"from":"Bob","to":"Carol","amt":5},
        {"from":"Carol","to":"Dave","amt":2},
        {"from":"Dave","to":"Alice","amt":1},
    ]
    
    new_blk = mine_block(genesis, txs, difficulty=4)
    print("Block hash:", new_blk.header.hash())
    print("Valid chain?", validate_chain([genesis, new_blk]))
