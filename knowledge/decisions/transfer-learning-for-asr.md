## Decision: Transfer Learning for Low-Resource ASR

### Context
Speech recognition needed to work for low-resource languages with limited labeled data.

### Options Considered
- Training ASR models from scratch
- Fine-tuning pre-trained transformer models

### Decision
Chose transfer learning using Wav2Vec2.

### Reasoning
- Pre-trained models already captured general speech representations
- Fine-tuning required significantly less data
- Better generalization on scarce datasets

### Trade-offs
- Upper-bound performance limited by base model
- Required careful regularization to avoid overfitting

### Outcome
Delivered measurable WER improvements with limited training data.