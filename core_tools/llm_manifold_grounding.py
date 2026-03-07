import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

def test_llm_manifold_ilda():
    """
    ILDA Phase: Grounding the LLM Manifold.
    1. Metric Verification (Hessian Symmetry/PSD)
    2. Dissipation Extraction (Entropy Gradient dS/dt)
    3. Precipitation Measurement (Crystallization Rate)
    """
    print("🧬 ILDA GROUNDING: LLM MANIFOLD EXTRACTION")
    print("-" * 65)

    # 1. Setup Toy Network (12 parameters for '12D' simulation)
    class ToyLLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.w = nn.Parameter(torch.randn(12))
        def forward(self, x):
            return torch.sum(x * self.w)

    net = ToyLLM()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    x = torch.randn(12)
    target = torch.tensor(1.0)

    # Metrics storage
    losses = []
    entropies = []
    
    print("Phase I: Dissipation (Training)")
    for step in range(100):
        optimizer.zero_grad()
        output = net(x)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        # Entropy approximation: H = -sum(p log p) -> here simplified to variance/loss
        entropies.append(np.log(loss.item() + 1e-9))

    # 2. Measure Entropy Gradient (dS/dt)
    ds_dt = np.gradient(entropies)
    avg_ds_dt = np.mean(ds_dt)
    print(f"Average Entropy Gradient (dS/dt): {avg_ds_dt:.6f}")
    
    # 3. Measure Crystallization (Knowledge Gain)
    # K = 1 - exp(-lambda * n)
    crystallization = 1.0 - (np.array(losses) / (losses[0] + 1e-9))
    final_k = crystallization[-1]
    print(f"Final Crystallization (K):        {final_k:.6f}")

    # 4. Metric Verification (Hessian at local minimum)
    loss = criterion(net(x), target)
    grads = torch.autograd.grad(loss, net.parameters(), create_graph=True)
    flat_grads = torch.cat([g.view(-1) for g in grads])
    
    hessian = []
    for g in flat_grads:
        h_row = torch.autograd.grad(g, net.parameters(), retain_graph=True)
        hessian.append(torch.cat([hr.view(-1) for hr in h_row]))
    
    H = torch.stack(hessian).detach().numpy()
    is_symmetric = np.allclose(H, H.T, atol=1e-5)
    eigs = np.linalg.eigvals(H)
    is_psd = np.all(eigs >= -1e-7)

    print("-" * 65)
    print(f"Hessian Symmetry:  {'✅ PASS' if is_symmetric else '❌ FAIL'}")
    print(f"Hessian PSD:       {'✅ PASS' if is_psd else '❌ FAIL'}")
    
    if avg_ds_dt < 0 and final_k > 0.9:
        print("✅ ILDA SUCCESS: Manifold is Dissipative and Crystallizing.")
        print(f"   Signature: dS/dt = {avg_ds_dt:.4f} | K = {final_k:.4f}")
    else:
        print("❌ ILDA FAILED: System is not descending to ground state.")

if __name__ == "__main__":
    test_llm_manifold_ilda()
