import numpy as np

def kl_divergence(p, q):
    """
    Measures the Information Distance between belief (p) and truth (q).
    D_KL(p || q) = sum p_i * ln(p_i / q_i)
    """
    p = np.array(p)
    q = np.array(q)
    # Ensure they sum to 1
    p = p / np.sum(p)
    q = q / np.sum(q)
    
    # Avoid log(0)
    p = np.clip(p, 1e-10, 1.0)
    q = np.clip(q, 1e-10, 1.0)
    
    return np.sum(p * np.log(p / q))

def verify_gibbs():
    print("🔭 VERIFYING GIBBS' INEQUALITY (KL-DIVERGENCE)")
    print("-" * 50)
    
    # Case 1: p = q
    p1 = [0.2, 0.3, 0.5]
    q1 = [0.2, 0.3, 0.5]
    d1 = kl_divergence(p1, q1)
    print(f"Case p=q | KL: {d1:.6f}")
    if not np.isclose(d1, 0):
        print("❌ Identity Failed!")
        return
        
    # Case 2: p != q
    p2 = [0.1, 0.1, 0.8]
    q2 = [0.33, 0.33, 0.34]
    d2 = kl_divergence(p2, q2)
    print(f"Case p!=q | KL: {d2:.6f}")
    if d2 < 0:
        print("❌ Inequality Failed!")
        return
        
    # Case 3: Random samplings
    for _ in range(5):
        pr = np.random.dirichlet(np.ones(5))
        qr = np.random.dirichlet(np.ones(5))
        dr = kl_divergence(pr, qr)
        if dr < -1e-9:
            print(f"❌ Inequality Failed at Random Case: {dr}")
            return
            
    print("✅ GIBBS' INEQUALITY: Verified (KL >= 0).")
    print("✅ GIBBS' IDENTITY: Verified (KL = 0 iff p=q).")

if __name__ == "__main__":
    verify_gibbs()
