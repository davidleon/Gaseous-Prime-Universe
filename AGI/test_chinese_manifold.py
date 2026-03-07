#!/usr/bin/env python3
"""
Test if Chinese bitstream manifold is properly loaded
"""

import numpy as np
import os
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimal_truncation_training import OptimalTruncationLearner
from manifold.utf8_bitstream_decoder import UTF8BitstreamDecoder

# Initialize learner
learner = OptimalTruncationLearner(manifold_dim=12, learning_rate=0.01)

# Load Chinese manifold
manifold_path = '/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/chinese_bitstream_manifold.npz'
if os.path.exists(manifold_path):
    data = np.load(manifold_path)
    learner.knowledge_manifold = data['manifold']
    learner.skill_level = data['skill_level']
    
    print(f'✓ Chinese bitstream manifold loaded')
    print(f'  Skill level: {learner.skill_level:.2%}')
    print(f'  Completions learned: {data["completions_learned"]}')
    print(f'  Manifold: {learner.knowledge_manifold[:5]}...')
    
    # Test decoding with Chinese manifold
    print(f'\nTesting UTF-8 bitstream decoding:')
    decoder = UTF8BitstreamDecoder(manifold_dim=12)
    
    # Test Chinese text encoding
    test_text = "你好，世界"
    encoding = learner.encode_text(test_text)
    print(f'  Input: {test_text}')
    print(f'  Encoding: {encoding[:5]}...')
    print(f'  Norm: {np.linalg.norm(encoding):.4f}')
    
    # Test decoding
    decoded = decoder.decode(learner.knowledge_manifold, max_length=50)
    print(f'  Decoded: {decoded}')
else:
    print(f'✗ Chinese manifold not found: {manifold_path}')