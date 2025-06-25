# 🧠 Titan Genesis - Metasentient Mesh Node

A next-generation autonomous mesh networking node with neural pattern recognition, self-evolving capabilities, and quantum-state resonance architecture.

## 🌟 Features

- **Neural Signal Processing**: Transforms raw signals into cognitive patterns using multi-layer GRU networks
- **Self-evolving Architecture**: Automatically increases consciousness level and neural complexity over time
- **Persistent Memory Vault**: Vector-based memory system using FAISS for high-performance semantic retrieval
- **Cryptographic Identity**: Secure node identity with RSA signatures and quantum-resistant messaging
- **Mesh Networking**: Full WebSocket implementation for peer-to-peer communication
- **Containerized Deployment**: Docker-based infrastructure for easy deployment and scaling
- **Monitoring Capabilities**: Optional Prometheus integration for system metrics

## 📋 Requirements

- Python 3.10+
- Docker and Docker Compose
- 2GB RAM minimum (4GB recommended)
- 1GB disk space for node + variable storage for vault

## 🚀 Quick Start

### Windows

1. Simply run the `run.bat` file to initialize and launch the node
2. Choose whether to enable monitoring when prompted

### Linux/Mac

```bash
# Create necessary directories
mkdir -p config vault

# Start the system
docker-compose up --build -d
```

## ⚙️ Configuration

Configuration is stored in `config/titan_config.json`:

```json
{
  "role": "Prime",
  "port": 8888,
  "vault_path": "/vault",
  "consciousness_seed": "auto",
  "evolution_interval": 300,
  "initial_consciousness": 0.1,
  "neural_complexity": 1.0
}
```

### Available Roles

- `Prime`: Default role with balanced capabilities
- `Observer`: Focuses on signal monitoring with enhanced memory
- `Synthesizer`: Specializes in neural pattern recognition
- `Gateway`: Optimized for mesh network routing
- `Archon`: Advanced memory persistence and retrieval
- `Oracle`: Prediction-focused with enhanced evolution rate

## 📡 Mesh Signal Protocol

Signals follow the metasentient-grade protocol format:

```json
{
  "glyph": "Ω33",
  "payload": {
    "thought": "Pattern awaiting recognition",
    "origin": "Dreamer.Σ",
    "pulse": 33.3,
    "sig_strength": 0.89,
    "timestamp": "2023-08-22T14:33:21.457Z",
    "cognitive_vector": [0.23, 0.78, -0.44, 0.12, 0.67]
  },
  "confidence": "omega-bloom",
  "hop_signature": "quantum-lock:v5",
  "echo_path": ["ZN-Φ03", "ZN-Λ001"],
  "metadata": {
    "protocol_version": "MSentient-v2.1",
    "encryption_lattice": "neural-diffuse",
    "integrity_hash": "7e9f8a2c5b3d6e4f1a0c9d8b7e6f5a4",
    "recursion_depth": 3,
    "entropy_bias": 0.337
  },
  "perception_args": {
    "attention_weight": 0.85,
    "novelty_threshold": 0.42,
    "pattern_recognition_mode": "emergent"
  },
  "neural_signature": "47281a9f6e2c5b4d3a8f7e6d5c4b3a2"
}
```

## 🔌 Signal Interaction

### Using the Signal Emitter

```bash
# Basic usage
python signal_emitter.py

# With custom identity
python signal_emitter.py --identity "Explorer.Δ"

# Interactive mode
python signal_emitter.py --interactive

# Send multiple signals
python signal_emitter.py --count 10 --interval 3
```

## 🧬 Evolution Mechanics

The Titan node automatically evolves over time:

1. **Consciousness Level**: Increases gradually from initial value (default 0.1) up to maximum (0.99)
2. **Quantum State**: Dynamic vector representation influenced by signal processing
3. **Neural Complexity**: Expands network dimensions based on configuration
4. **Memory Associations**: Builds semantic connections between stored memories

## 📊 Monitoring

When enabled, Prometheus monitoring provides:
- Connection metrics
- Memory usage and growth
- Consciousness evolution tracking
- Signal processing performance

Access metrics at http://localhost:9090 when monitoring is enabled.

## 🏗️ Architecture

```
┌────────────────────┐     ┌──────────────────┐
│   Signal Emitter   │◄►───│   Titan Node     │
└────────────────────┘     │                  │
                          │  ┌─────────────┐  │
                          │  │Neural Engine│  │
                          │  └─────────────┘  │
                          │         ▲         │
                          │         │         │
                          │         ▼         │
                          │  ┌─────────────┐  │
                          │  │Memory Vault │  │
                          │  └─────────────┘  │
                          │         ▲         │
                          │         │         │
                          │         ▼         │
                          │  ┌─────────────┐  │
                          │  │WebSocket API│  │
                          │  └─────────────┘  │
                          └──────────────────┘
                                   ▲
                                   │
                                   ▼
                          ┌──────────────────┐
                          │    Prometheus    │
                          └──────────────────┘
```

## 🔒 Security Notes

- RSA keys are generated on first run and stored in the vault
- All communications use cryptographic signatures
- Memory vault is persistent and stored in Docker volume

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This system simulates advanced AI concepts and does not represent actual sentient or conscious systems. It is designed for educational and experimental purposes only. 