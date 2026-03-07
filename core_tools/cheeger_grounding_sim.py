import numpy as np
import networkx as nx

def compute_spectral_gap(G):
    """Computes the spectral gap (lambda_2) of the normalized Laplacian."""
    L = nx.normalized_laplacian_matrix(G).toarray()
    eigs = np.sort(np.linalg.eigvals(L))
    # Lambda_1 is always 0, lambda_2 is the spectral gap
    return eigs[1] if len(eigs) > 1 else 0

def compute_cheeger_constant(G):
    """
    Computes the Cheeger constant (h) of the graph.
    h(G) = min_{S} |boundary(S)| / min(vol(S), vol(V\S))
    This is an NP-hard problem, we'll approximate for small graphs.
    """
    nodes = list(G.nodes())
    n = len(nodes)
    h_min = float('inf')
    
    # Iterate through all possible partitions
    import itertools
    for i in range(1, n // 2 + 1):
        for subset in itertools.combinations(nodes, i):
            S = set(subset)
            boundary_size = 0
            vol_S = sum(G.degree(u) for u in S)
            vol_V_S = sum(G.degree(u) for u in (set(nodes) - S))
            
            for u, v in G.edges():
                if (u in S and v not in S) or (v in S and u not in S):
                    boundary_size += 1
            
            h = boundary_size / min(vol_S, vol_V_S)
            if h < h_min:
                h_min = h
    return h_min

def verify_cheeger_bound():
    print("🧬 ILDA ITERATION: GROUNDING IT-FROM-BIT (CHEEGER)")
    print("-" * 65)
    print(f"{'Graph Type':<20} | {'Phi (h)':<10} | {'Gamma (λ2)':<10} | {'h^2/2':<10} | {'Status'}")
    print("-" * 65)
    
    # Test on various logical topologies
    graphs = [
        ("Path(10)", nx.path_graph(10)),
        ("Cycle(10)", nx.cycle_graph(10)),
        ("Star(10)", nx.star_graph(9)),
        ("Complete(10)", nx.complete_graph(10)),
        ("Grid(3x3)", nx.grid_2d_graph(3, 3)),
        ("Hypercube(3D)", nx.hypercube_graph(3))
    ]
    
    for name, G in graphs:
        # Relabel nodes to integers
        G = nx.convert_node_labels_to_integers(G)
        phi = compute_cheeger_constant(G)
        gamma = compute_spectral_gap(G)
        lower_bound = (phi**2) / 2 # Using h^2/2 for discrete normalized Laplacian
        
        status = "✅ PASS" if gamma >= lower_bound - 1e-9 else "❌ FAIL"
        print(f"{name:<20} | {phi:<10.4f} | {gamma:<10.4f} | {lower_bound:<10.4f} | {status}")

if __name__ == "__main__":
    verify_cheeger_bound()
