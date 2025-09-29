# tests.py
from chain import merkle_root, Block, BlockHeader, mine_block, validate_chain
from chain import sha256_hex
import time, json, sys

# Data contoh (harus sama persis untuk cocok dengan hash di bawah)
T1 = {"from":"Alice","to":"Bob","amt":10}
T2 = {"from":"Bob","to":"Carol","amt":5}
T3 = {"from":"Carol","to":"Dave","amt":2}
T4 = {"from":"Dave","to":"Alice","amt":1}
TXS = [T1,T2,T3,T4]

# Fungsi untuk debug - hitung hash manual
def H(tx): 
    return sha256_hex(json.dumps(tx, sort_keys=True).encode())

# Hitung ulang semua hash
def calculate_expected_hashes():
    h1 = H(T1)
    h2 = H(T2) 
    h3 = H(T3)
    h4 = H(T4)
    
    h12 = sha256_hex(bytes.fromhex(h1) + bytes.fromhex(h2))
    h34 = sha256_hex(bytes.fromhex(h3) + bytes.fromhex(h4))
    root = sha256_hex(bytes.fromhex(h12) + bytes.fromhex(h34))
    
    print("=== DEBUG HASHES ===")
    print(f"H1:  {h1}")
    print(f"H2:  {h2}")
    print(f"H3:  {h3}") 
    print(f"H4:  {h4}")
    print(f"H12: {h12}")
    print(f"H34: {h34}")
    print(f"ROOT: {root}")
    print("====================")
    
    return {
        "H1": h1, "H2": h2, "H3": h3, "H4": h4,
        "H12": h12, "H34": h34, "ROOT": root
    }

def test_merkle_root_matches_expected():
    # Gunakan hash yang dihitung ulang
    exp = calculate_expected_hashes()
    
    root = merkle_root(TXS)
    print(f"Calculated root: {root}")
    print(f"Expected root:   {exp['ROOT']}")
    
    assert root == exp["ROOT"], f"Merkle root mismatch: {root} != {exp['ROOT']}"

def test_pow_and_chain_validation():
    genesis = Block(BlockHeader(0, time.time(), "0"*64, "0"*64, 0, 3), [])
    blk = mine_block(genesis, TXS, difficulty=3)
    assert validate_chain([genesis, blk]), "Chain should be valid"

# Acceptance test untuk proof 
from chain import merkle_proof, verify_proof

def test_merkle_proof_T3():
    root = merkle_root(TXS)
    proof = merkle_proof(TXS, index=2)  # T3 = index 2 (0-based)
    assert verify_proof(T3, proof, root), "Proof(T3) should verify to ROOT"

if __name__ == "__main__":
    try:
        test_merkle_root_matches_expected()
        test_pow_and_chain_validation()
        test_merkle_proof_T3()  
        print("All checks passed.")
    except AssertionError as e:
        print("TEST FAIL:", e)
        sys.exit(1)



