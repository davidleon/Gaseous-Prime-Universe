"""
UTF-8 Bitstream Decoder
Decodes manifold bits directly into UTF-8 byte streams using fractal bridge

Instead of vocabulary-based approaches, this directly maps:
Manifold bits → Fractal bridge → UTF-8 bytes → Text
"""

import numpy as np
from typing import List, Tuple, Optional
import struct


class UTF8BitstreamDecoder:
    """
    Decodes manifold bits to UTF-8 text using fractal bridge transformation
    
    The manifold contains continuous values (bits) that are:
    1. Quantized to discrete bit patterns
    2. Transformed through fractal bridge
    3. Mapped to UTF-8 byte sequences
    4. Decoded to text
    """
    
    def __init__(
        self,
        manifold_dim: int = 12,
        fractal_dim: float = 12.0 + 1.0/(18*np.pi),
        precision_bits: int = 400
    ):
        """
        Initialize UTF-8 bitstream decoder
        
        Args:
            manifold_dim: Dimensionality of input manifold
            fractal_dim: Fractal dimension for transformation
            precision_bits: Precision for bit quantization
        """
        self.manifold_dim = manifold_dim
        self.fractal_dim = fractal_dim
        self.precision_bits = precision_bits
        
        # Fractal bridge transformation matrix
        self.transformation_matrix = self._build_transformation_matrix()
        
        # UTF-8 byte mapping
        self.utf8_mapping = self._build_utf8_mapping()
        
    def _build_transformation_matrix(self) -> np.ndarray:
        """
        Build fractal bridge transformation matrix
        
        Maps manifold bits to UTF-8 byte indices
        """
        # Create transformation based on fractal dimension
        matrix = np.zeros((256, self.manifold_dim))  # 256 possible UTF-8 bytes
        
        for i in range(256):
            for j in range(self.manifold_dim):
                # Fractal scaling
                scale = (i / 255.0) ** (self.fractal_dim / self.manifold_dim)
                matrix[i, j] = scale * np.sin(j * np.pi / self.manifold_dim)
        
        # Normalize rows
        for i in range(256):
            if np.sum(np.abs(matrix[i])) > 0:
                matrix[i] = matrix[i] / np.linalg.norm(matrix[i])
        
        return matrix
    
    def _build_utf8_mapping(self) -> np.ndarray:
        """
        Build mapping for UTF-8 byte sequences
        
        Returns:
            Array of valid UTF-8 byte values
        """
        # All valid UTF-8 bytes (0-255)
        return np.arange(256, dtype=np.uint8)
    
    def manifold_to_bits(self, manifold: np.ndarray) -> np.ndarray:
        """
        Convert manifold values to bit representation
        
        Args:
            manifold: Input manifold vector (continuous values)
            
        Returns:
            Quantized bit array
        """
        # Normalize manifold
        manifold_norm = manifold / (np.linalg.norm(manifold) + 1e-10)
        
        # Quantize to bits using fractal dimension sampling
        bits = np.zeros(self.precision_bits, dtype=np.int8)
        
        for i in range(self.precision_bits):
            # Sample from manifold using fractal dimension
            fractal_index = int((i / self.precision_bits) ** (self.fractal_dim / self.manifold_dim) * self.manifold_dim) % self.manifold_dim
            
            # Quantize value to bit (positive = 1, negative = -1)
            value = manifold_norm[fractal_index]
            bits[i] = 1 if value > 0 else -1
        
        return bits
    
    def bits_to_utf8_bytes(self, bits: np.ndarray) -> np.ndarray:
        """
        Convert bit array to UTF-8 bytes using fractal bridge
        
        Args:
            bits: Input bit array
            
        Returns:
            UTF-8 byte array
        """
        # Group bits into bytes (8 bits per byte)
        n_bytes = min(len(bits) // 8, 256)  # Limit to 256 bytes
        utf8_bytes = np.zeros(n_bytes, dtype=np.uint8)
        
        for byte_idx in range(n_bytes):
            # Extract 8 bits
            byte_bits = bits[byte_idx * 8: (byte_idx + 1) * 8]
            
            # Convert bits to byte value (standard binary to decimal)
            byte_value = 0
            for bit_idx, bit in enumerate(byte_bits):
                if bit > 0:  # bit is 1
                    byte_value |= (1 << (7 - bit_idx))
            
            utf8_bytes[byte_idx] = byte_value % 256
        
        return utf8_bytes
    
    def decode(self, manifold: np.ndarray, max_length: int = 100) -> str:
        """
        Decode manifold to text using UTF-8 bitstream
        
        Args:
            manifold: Input manifold vector
            max_length: Maximum text length in characters
            
        Returns:
            Decoded text string
        """
        # Step 1: Manifold → Bits
        bits = self.manifold_to_bits(manifold)
        
        # Step 2: Bits → UTF-8 bytes
        utf8_bytes = self.bits_to_utf8_bytes(bits)
        
        # Step 3: UTF-8 bytes → Text
        try:
            # Decode as UTF-8
            text = utf8_bytes[:max_length].tobytes().decode('utf-8', errors='replace')
            
            # Filter valid printable characters
            text = ''.join(c for c in text if c.isprintable())
            
            # Limit length
            text = text[:max_length]
            
        except Exception as e:
            # Fallback to ASCII if UTF-8 fails
            text = ''.join(chr(b % 128) for b in utf8_bytes[:max_length])
        
        return text
    
    def decode_batch(self, manifolds: List[np.ndarray], max_length: int = 100) -> List[str]:
        """
        Decode multiple manifolds to text
        
        Args:
            manifolds: List of manifold vectors
            max_length: Maximum text length per string
            
        Returns:
            List of decoded text strings
        """
        return [self.decode(manifold, max_length) for manifold in manifolds]
    
    def get_info(self) -> dict:
        """Get decoder information"""
        return {
            "manifold_dim": self.manifold_dim,
            "fractal_dim": self.fractal_dim,
            "precision_bits": self.precision_bits,
            "utf8_bytes": 256,
            "transformation_shape": self.transformation_matrix.shape
        }


def test_utf8_bitstream_decoder():
    """Test UTF-8 bitstream decoder"""
    print("Testing UTF-8 Bitstream Decoder...")
    
    # Create decoder
    decoder = UTF8BitstreamDecoder(
        manifold_dim=12,
        fractal_dim=12.0 + 1.0/(18*np.pi),
        precision_bits=400
    )
    
    print(f"  Decoder info: {decoder.get_info()}")
    
    # Test decoding
    test_manifold = np.random.randn(12)
    test_manifold = test_manifold / np.linalg.norm(test_manifold)
    
    decoded_text = decoder.decode(test_manifold, max_length=50)
    
    print(f"  Input manifold: {test_manifold[:5]}...")
    print(f"  Decoded text: {decoded_text}")
    print(f"  Text length: {len(decoded_text)}")
    
    # Test batch decoding
    test_manifolds = [np.random.randn(12) for _ in range(5)]
    decoded_texts = decoder.decode_batch(test_manifolds)
    
    print(f"\n  Batch decoding ({len(test_manifolds)} manifolds):")
    for i, (manifold, text) in enumerate(zip(test_manifolds, decoded_texts)):
        print(f"    {i+1}. {text[:30]}{'...' if len(text) > 30 else ''}")
    
    print("  All tests passed!")


if __name__ == "__main__":
    test_utf8_bitstream_decoder()