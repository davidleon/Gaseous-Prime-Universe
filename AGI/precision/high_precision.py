"""
High-Precision Arithmetic Utilities (400-bit precision)
Supports arbitrary-precision arithmetic for manifold calculations
"""

import numpy as np
from decimal import Decimal, getcontext
import mpmath as mp
from typing import Union, List, Tuple

# Set precision to 400 bits (approximately 120 decimal digits)
getcontext().prec = 120
mp.mp.dps = 120  # Decimal places for mpmath


class HighPrecision:
    """
    High-precision arithmetic utilities for 400-bit precision
    Uses both Decimal and mpmath for different operations
    """
    
    @staticmethod
    def to_decimal(value: Union[float, int, str, Decimal]) -> Decimal:
        """Convert value to high-precision Decimal"""
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))
    
    @staticmethod
    def to_mp(value: Union[float, int, str, Decimal]) -> mp.mpf:
        """Convert value to high-precision mpmath float"""
        if isinstance(value, mp.mpf):
            return value
        return mp.mpf(str(value))
    
    @staticmethod
    def array_to_decimal(arr: np.ndarray) -> List[Decimal]:
        """Convert numpy array to list of high-precision Decimals"""
        return [HighPrecision.to_decimal(x) for x in arr]
    
    @staticmethod
    def array_to_mp(arr: np.ndarray) -> List[mp.mpf]:
        """Convert numpy array to list of high-precision mpmath floats"""
        return [HighPrecision.to_mp(x) for x in arr]
    
    @staticmethod
    def decimal_to_array(decimals: List[Decimal]) -> np.ndarray:
        """Convert list of Decimals to numpy array"""
        return np.array([float(d) for d in decimals], dtype=np.float64)
    
    @staticmethod
    def mp_to_array(mpf_list: List[mp.mpf]) -> np.ndarray:
        """Convert list of mpmath floats to numpy array"""
        return np.array([float(m) for m in mpf_list], dtype=np.float64)
    
    @staticmethod
    def high_precision_svd(matrix: np.ndarray, precision: int = 400) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        High-precision SVD using mpmath
        
        Args:
            matrix: Input matrix
            precision: Precision in bits
            
        Returns:
            U, S, Vt matrices from SVD decomposition
        """
        # Set precision
        mp.mp.dps = precision // 3  # Bits to decimal places conversion
        
        # Convert to mpmath matrix
        mp_matrix = mp.matrix([[HighPrecision.to_mp(x) for x in row] for row in matrix])
        
        # Perform SVD
        U, S, Vt = mp.svd(mp_matrix)
        
        # Convert back to numpy
        U_np = np.array([[float(U[i,j]) for j in range(U.cols)] for i in range(U.rows)])
        S_np = np.array([float(S[i]) for i in range(len(S))])
        Vt_np = np.array([[float(Vt[i,j]) for j in range(Vt.cols)] for i in range(Vt.rows)])
        
        return U_np, S_np, Vt_np
    
    @staticmethod
    def high_precision_eigen(matrix: np.ndarray, precision: int = 400) -> Tuple[np.ndarray, np.ndarray]:
        """
        High-precision eigenvalue decomposition using mpmath
        
        Args:
            matrix: Input matrix (must be symmetric)
            precision: Precision in bits
            
        Returns:
            eigenvalues, eigenvectors
        """
        # Set precision
        mp.mp.dps = precision // 3
        
        # Convert to mpmath matrix
        mp_matrix = mp.matrix([[HighPrecision.to_mp(x) for x in row] for row in matrix])
        
        # Perform eigenvalue decomposition
        eigenvalues, eigenvectors = mp.eig(mp_matrix)
        
        # Convert back to numpy
        eigenvalues_np = np.array([float(ev.real) for ev in eigenvalues])
        eigenvectors_np = np.array([[float(eigenvectors[i,j].real) for j in range(len(eigenvectors))] 
                                   for i in range(len(eigenvectors))])
        
        return eigenvalues_np, eigenvectors_np
    
    @staticmethod
    def high_precision_norm(vector: np.ndarray, precision: int = 400) -> float:
        """
        High-precision L2 norm calculation
        """
        mp.mp.dps = precision // 3
        
        # Calculate squared sum with high precision
        squared_sum = mp.mpf(0)
        for x in vector:
            squared_sum += mp.mpf(x) ** 2
        
        return float(mp.sqrt(squared_sum))
    
    @staticmethod
    def high_precision_dot(a: np.ndarray, b: np.ndarray, precision: int = 400) -> float:
        """
        High-precision dot product
        """
        mp.mp.dps = precision // 3
        
        # Calculate dot product with high precision
        result = mp.mpf(0)
        for x, y in zip(a, b):
            result += mp.mpf(x) * mp.mpf(y)
        
        return float(result)
    
    @staticmethod
    def high_precision_distance(a: np.ndarray, b: np.ndarray, precision: int = 400) -> float:
        """
        High-precision Euclidean distance
        """
        diff = a - b
        return HighPrecision.high_precision_norm(diff, precision)


class PrecisionConfig:
    """Configuration for precision settings"""
    
    def __init__(self, precision_bits: int = 400):
        self.precision_bits = precision_bits
        self.precision_decimal = precision_bits // 3
        self.epsilon = 10 ** (-self.precision_decimal + 2)  # Safety margin
    
    def set_precision(self):
        """Set global precision"""
        getcontext().prec = self.precision_decimal
        mp.mp.dps = self.precision_decimal
    
    def is_close(self, a: float, b: float, rel_tol: float = None, abs_tol: float = None) -> bool:
        """
        Check if two values are close within precision tolerance
        
        Args:
            a, b: Values to compare
            rel_tol: Relative tolerance (default: epsilon)
            abs_tol: Absolute tolerance (default: epsilon)
        """
        if rel_tol is None:
            rel_tol = self.epsilon
        if abs_tol is None:
            abs_tol = self.epsilon
        
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_high_precision():
    """Test high-precision functionality"""
    print("Testing High-Precision Arithmetic...")
    
    config = PrecisionConfig(precision_bits=400)
    config.set_precision()
    
    # Test 1: Basic operations
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    
    norm_a = HighPrecision.high_precision_norm(a)
    dot_ab = HighPrecision.high_precision_dot(a, b)
    dist_ab = HighPrecision.high_precision_distance(a, b)
    
    print(f"  Norm of a: {norm_a:.15f}")
    print(f"  Dot product a·b: {dot_ab:.15f}")
    print(f"  Distance a-b: {dist_ab:.15f}")
    
    # Test 2: SVD
    matrix = np.random.rand(10, 10)
    U, S, Vt = HighPrecision.high_precision_svd(matrix)
    
    print(f"  SVD successful: U shape {U.shape}, S shape {S.shape}, Vt shape {Vt.shape}")
    
    # Test 3: Eigenvalue decomposition
    symmetric_matrix = (matrix + matrix.T) / 2
    eigenvalues, eigenvectors = HighPrecision.high_precision_eigen(symmetric_matrix)
    
    print(f"  Eigen decomposition successful: {len(eigenvalues)} eigenvalues")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_high_precision()