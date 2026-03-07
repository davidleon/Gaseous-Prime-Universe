import math
import numpy as np
import matplotlib.pyplot as plt

def get_stopping_time(n):
    steps = 0
    curr = n
    while curr > 1:
        if curr % 2 == 0:
            curr //= 2
        else:
            curr = 3 * curr + 1
        steps += 1
        if steps > 100000: return -1 # Timeout
    return steps

def test_complexity_growth(max_power=7):
    print(f"📊 TESTING COLLATZ STOPPING TIME COMPLEXITY (N up to 10^{max_power})")
    print(f"{'N Range':<15} | {'Avg Steps':<15} | {'Steps / log2(N)':<15}")
    print("-" * 55)
    
    for p in range(2, max_power + 1):
        n_samples = 1000
        samples = np.random.randint(10**(p-1), 10**p, n_samples)
        times = [get_stopping_time(n) for n in samples]
        # Filter out timeouts
        valid_times = [t for t in times if t > 0]
        
        avg_steps = np.mean(valid_times)
        ratio = avg_steps / math.log2(10**p)
        
        print(f"10^{p-1} - 10^{p:<5} | {avg_steps:<15.2f} | {ratio:<15.4f}")

if __name__ == "__main__":
    test_complexity_growth()
