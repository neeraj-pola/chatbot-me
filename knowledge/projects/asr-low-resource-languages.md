## Project: ASR for Low-Resource Languages

### Problem
Speech recognition models perform poorly on low-resource languages due to limited labeled data.

### Context & Constraints
- Limited audio data (27–45 hours per language)
- Need for multilingual adaptability
- Performance measured via WER and CER

### Solution
Fine-tuned Wav2Vec2 transformer-based ASR models on:
- Bengali (45+ hours)
- Assamese (27 hours)

Engineered a custom 512-unit neural layer for BPE transfer learning to improve contextual representations.

### Key Decisions
- Used transfer learning instead of training from scratch
- Focused on representation learning for resource-scarce data
- Evaluated using WER and CER for robustness

### Trade-offs
- Limited upper-bound performance due to data scarcity
- Required careful regularization to avoid overfitting

### Outcome
- Achieved WER 38.7 and CER 10.2 on Bengali
- Delivered 12–18% WER improvement on Assamese
- Improved contextual representation learning

### What I’d Do Differently
- Explore semi-supervised data augmentation
- Evaluate multilingual joint training strategies