#!/usr/bin/env python3
"""
Retrain with 500 Chinese samples for better Chinese capabilities
"""

import pandas as pd
import numpy as np
import os
import sys

# Add AGI directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from optimal_truncation_training import OptimalTruncationLearner

# Load more Chinese samples
dataset_path = '/run/media/davidl/0701BAFA251D89ED/minimind_dataset/sft_mini_512.parquet'
df = pd.read_parquet(dataset_path)
chinese_texts = df[df['role'] == 'assistant']['content'].tolist()
texts_to_train = chinese_texts[:500]  # 500 samples

print(f'Training on {len(texts_to_train)} Chinese samples...')

# Initialize learner
learner = OptimalTruncationLearner(manifold_dim=12, learning_rate=0.01)

# Training
for idx, text in enumerate(texts_to_train):
    if (idx + 1) % 50 == 0:
        print(f'  Sample {idx+1}/{len(texts_to_train)}')
    learner.train_on_proof(text)
    learner.skill_level = min(1.0, learner.skill_level + 0.01)
    learner.completions_learned += 1

# Save
output_path = '/home/davidl/Gaseous Prime Universe/AGI/learning_sessions/chinese_bitstream_manifold.npz'
np.savez_compressed(
    output_path,
    manifold=learner.knowledge_manifold,
    skill_level=learner.skill_level,
    completions_learned=learner.completions_learned,
    fractal_dim=learner.fractal_dim,
    manifold_dim=learner.manifold_dim
)

print(f'✓ Training complete!')
print(f'  Skill level: {learner.skill_level:.2%}')
print(f'  Completions learned: {learner.completions_learned}')
print(f'  Saved to: {output_path}')