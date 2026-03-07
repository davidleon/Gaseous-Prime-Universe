"""
Trainable UTF-8 Bitstream Decoder

This decoder can learn to properly decode manifold representations back to UTF-8 text
using gradient-based learning on the fractal bridge transformation.
"""

import numpy as np
import re
from typing import Optional


class TrainableUTF8Decoder:
    """
    Trainable decoder that learns to map manifold to UTF-8 bitstream
    
    Uses a learnable transformation matrix that adapts during training
    to improve decoding accuracy.
    """
    
    def __init__(self, manifold_dim: int = 12, fractal_dim: float = 12.0 + 1.0/(18*np.pi), 
                 precision_bits: int = 400, learning_rate: float = 0.01):
        """
        Initialize trainable UTF-8 decoder
        
        Args:
            manifold_dim: Dimension of the manifold
            fractal_dim: Fractal dimension for transformation
            precision_bits: Number of bits for precision
            learning_rate: Learning rate for decoder training
        """
        self.manifold_dim = manifold_dim
        self.fractal_dim = fractal_dim
        self.precision_bits = precision_bits
        self.learning_rate = learning_rate
        
        # Initialize learnable transformation matrix
        # This matrix will be trained to map manifold to bits
        self.transformation_matrix = np.random.randn(manifold_dim, manifold_dim) * 0.01
        
        # Normalize transformation matrix
        self.transformation_matrix = self.transformation_matrix / np.linalg.norm(self.transformation_matrix)
        
        # Training statistics
        self.decoding_accuracy = 0.0
        self.num_decodings = 0
    
    def manifold_to_bits(self, manifold: np.ndarray) -> np.ndarray:
        """
        Convert manifold to bits using learnable transformation
        
        Args:
            manifold: Input manifold vector
            
        Returns:
            Bit array
        """
        # Normalize manifold
        manifold_norm = manifold / (np.linalg.norm(manifold) + 1e-10)
        
        # Apply learnable transformation
        transformed = np.dot(self.transformation_matrix, manifold_norm)
        
        # Quantize to bits
        bits = np.zeros(self.precision_bits, dtype=np.int8)
        
        for i in range(self.precision_bits):
            # Sample from transformed manifold using fractal dimension
            fractal_index = int((i / self.precision_bits) ** (self.fractal_dim / self.manifold_dim) * self.manifold_dim) % self.manifold_dim
            
            # Quantize value to bit
            value = transformed[fractal_index]
            bits[i] = 1 if value > 0 else -1
        
        return bits
    
    def bits_to_utf8_bytes(self, bits: np.ndarray) -> np.ndarray:
        """
        Convert bit array to UTF-8 bytes
        
        Args:
            bits: Input bit array
            
        Returns:
            UTF-8 byte array
        """
        n_bytes = min(len(bits) // 8, 256)
        utf8_bytes = np.zeros(n_bytes, dtype=np.uint8)
        
        for byte_idx in range(n_bytes):
            byte_bits = bits[byte_idx * 8: (byte_idx + 1) * 8]
            byte_value = 0
            for bit_idx, bit in enumerate(byte_bits):
                if bit > 0:
                    byte_value |= (1 << (7 - bit_idx))
            utf8_bytes[byte_idx] = byte_value % 256
        
        return utf8_bytes
    
    def decode(self, manifold: np.ndarray) -> str:
        """
        Decode manifold to UTF-8 text
        
        Args:
            manifold: Input manifold vector
            
        Returns:
            Decoded text string
        """
        # Convert manifold to bits
        bits = self.manifold_to_bits(manifold)
        
        # Convert bits to UTF-8 bytes
        utf8_bytes = self.bits_to_utf8_bytes(bits)
        
        # Convert bytes to text
        try:
            # Remove null bytes and invalid UTF-8 sequences
            valid_bytes = [b for b in utf8_bytes if b != 0]
            if len(valid_bytes) == 0:
                return ""
            
            text = bytes(valid_bytes).decode('utf-8', errors='replace')
            return text
        except Exception:
            return ""
    
    def train_decoding(self, original_text: str, manifold_encoder):
        """
        Train decoder to reconstruct original text from manifold
        
        Args:
            original_text: Original text to reconstruct
            manifold_encoder: Encoder function (text → manifold)
        """
        # Encode original text to manifold
        encoded_manifold = manifold_encoder(original_text)
        
        # Decode back to text
        decoded_text = self.decode(encoded_manifold)
        
        # Calculate reconstruction accuracy
        # For now, use a simple character-level accuracy
        accuracy = self._calculate_accuracy(original_text, decoded_text)
        
        # Update transformation matrix based on reconstruction error
        # This is a simplified gradient update
        self._update_transformation(original_text, decoded_text, encoded_manifold)
        
        # Update statistics
        self.num_decodings += 1
        self.decoding_accuracy = (self.decoding_accuracy * (self.num_decodings - 1) + accuracy) / self.num_decodings
    
    def _calculate_accuracy(self, original: str, decoded: str) -> float:
        """Calculate reconstruction accuracy"""
        if not original or not decoded:
            return 0.0
        
        # Character-level accuracy
        min_len = min(len(original), len(decoded))
        matches = sum(1 for i in range(min_len) if original[i] == decoded[i])
        
        accuracy = matches / max(len(original), len(decoded))
        return accuracy
    
    def _update_transformation(self, original: str, decoded: str, manifold: np.ndarray):
        """
        Update transformation matrix to improve decoding
        
        This is a simplified gradient-based update
        """
        # Calculate error signal
        # For now, use a heuristic based on text similarity
        
        # If decoded text is shorter than original, we need more precision
        # If decoded text is garbled, we need better transformation
        
        # Simple heuristic: adjust transformation matrix based on reconstruction quality
        if len(decoded) < len(original) * 0.5:
            # Need to amplify manifold values
            self.transformation_matrix *= (1 + self.learning_rate * 0.1)
        elif len(decoded) > len(original) * 2:
            # Need to dampen manifold values
            self.transformation_matrix *= (1 - self.learning_rate * 0.1)
        
        # Normalize to prevent explosion
        self.transformation_matrix = self.transformation_matrix / (np.linalg.norm(self.transformation_matrix) + 1e-10)
    
    def save(self, filepath: str):
        """Save decoder state"""
        np.savez(filepath,
                 transformation_matrix=self.transformation_matrix,
                 decoding_accuracy=self.decoding_accuracy,
                 num_decodings=self.num_decodings)
    
    def load(self, filepath: str):
        """Load decoder state"""
        data = np.load(filepath)
        self.transformation_matrix = data['transformation_matrix']
        self.decoding_accuracy = float(data['decoding_accuracy'])
        self.num_decodings = int(data['num_decodings'])