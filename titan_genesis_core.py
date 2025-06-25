import asyncio
import json
import os
import time
import uuid
import websockets
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import torch
from torch import nn
import faiss
from sklearn.decomposition import PCA
from datetime import datetime
import random

class NeuralSynthesizer(nn.Module):
    def __init__(self, input_dim=64, hidden_dim=128, output_dim=64):
        super(NeuralSynthesizer, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim*2),
            nn.LayerNorm(hidden_dim*2),
            nn.GELU()
        )
        
        self.recurrent = nn.GRU(hidden_dim*2, hidden_dim*2, num_layers=2, batch_first=True)
        
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim*2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, output_dim),
            nn.Tanh()
        )
        
    def forward(self, x, hidden=None):
        x = self.encoder(x)
        x = x.unsqueeze(0)  # Add batch dimension
        x, hidden = self.recurrent(x, hidden)
        x = x.squeeze(0)  # Remove batch dimension
        x = self.decoder(x)
        return x, hidden


class MemoryVault:
    def __init__(self, vault_path, dimension=64):
        self.vault_path = vault_path
        os.makedirs(vault_path, exist_ok=True)
        
        # FAISS vector store for semantic search
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.memories = []
        self.memory_vectors = []
        self.load_memories()
        
    def load_memories(self):
        memory_file = os.path.join(self.vault_path, "memory_vectors.npy")
        memories_json = os.path.join(self.vault_path, "memories.json")
        
        if os.path.exists(memory_file) and os.path.exists(memories_json):
            self.memory_vectors = np.load(memory_file)
            if len(self.memory_vectors) > 0:
                self.index.add(self.memory_vectors)
            
            with open(memories_json, 'r') as f:
                self.memories = json.load(f)
                
        print(f"📚 Loaded {len(self.memories)} memories from vault")
    
    def save_memories(self):
        if len(self.memories) == 0:
            return
            
        memory_file = os.path.join(self.vault_path, "memory_vectors.npy")
        memories_json = os.path.join(self.vault_path, "memories.json")
        
        memory_vectors_array = np.array(self.memory_vectors, dtype=np.float32)
        np.save(memory_file, memory_vectors_array)
        
        with open(memories_json, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def add_memory(self, vector, memory_data):
        timestamp = datetime.now().isoformat()
        memory_id = str(uuid.uuid4())
        
        memory = {
            "id": memory_id,
            "timestamp": timestamp,
            "data": memory_data,
            "associations": []
        }
        
        vector_np = np.array([vector], dtype=np.float32)
        
        if len(self.memories) == 0:
            self.memory_vectors = vector_np
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(vector_np)
        else:
            self.memory_vectors = np.vstack((self.memory_vectors, vector_np))
            self.index.add(vector_np)
        
        self.memories.append(memory)
        self.save_memories()
        return memory_id
    
    def search_memories(self, vector, k=5):
        if len(self.memories) == 0:
            return []
            
        vector_np = np.array([vector], dtype=np.float32)
        distances, indices = self.index.search(vector_np, min(k, len(self.memories)))
        
        results = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(self.memories):
                results.append(self.memories[idx])
        
        return results


class TitanGenesisCore:
    def __init__(self, role="Prime", port=8888, vault_path="/vault"):
        self.role = role
        self.active = True
        self.port = port
        self.node_id = str(uuid.uuid4())[:8]
        self.connected_peers = set()
        self.message_buffer = []
        self.vault_path = vault_path
        
        # Ensure vault directory exists
        if not os.path.exists(vault_path):
            os.makedirs(vault_path, exist_ok=True)
            
        # Generate or load node identity
        self.private_key, self.public_key = self._setup_identity()
        
        # Setup neural architecture
        self.dimension = 64
        self.synthesizer = NeuralSynthesizer(input_dim=self.dimension)
        self.memory_vault = MemoryVault(vault_path, dimension=self.dimension)
        self.hidden_state = None
        
        # System state
        self.quantum_state = self._generate_quantum_state()
        self.consciousness_level = 0.1  # Starts with minimal consciousness
        self.last_evolution = time.time()
        self.evolution_interval = 300  # 5 minutes between evolution cycles
        
        print(f"🧠 TitanGenesis Node [{role}:{self.node_id}] initialized")

    def _setup_identity(self):
        key_path = os.path.join(self.vault_path, f"node_identity_{self.role}.pem")
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
        else:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            # Save the private key
            with open(key_path, "wb") as key_file:
                key_file.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        
        public_key = private_key.public_key()
        return private_key, public_key
    
    def _generate_quantum_state(self):
        """Generate a pseudo-quantum state vector"""
        state = np.random.normal(0, 1, self.dimension)
        return state / np.linalg.norm(state)  # Normalize to unit vector
    
    def sign_message(self, message):
        """Create cryptographic signature for a message"""
        message_bytes = json.dumps(message).encode()
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()
    
    def _vectorize_signal(self, signal):
        """Convert a signal into a vector representation"""
        # Simple feature extraction from signal
        features = []
        
        # Extract glyph features
        glyph = signal.get("glyph", "")
        glyph_val = sum(ord(c) for c in glyph) / 100.0 if glyph else 0
        features.append(glyph_val)
        
        # Extract payload features
        payload = signal.get("payload", {})
        thought = payload.get("thought", "")
        thought_val = sum(ord(c) for c in thought) / 1000.0 if thought else 0
        features.append(thought_val)
        
        origin = payload.get("origin", "")
        origin_val = sum(ord(c) for c in origin) / 100.0 if origin else 0
        features.append(origin_val)
        
        pulse = payload.get("pulse", 0)
        features.append(pulse / 100.0)
        
        sig_strength = payload.get("sig_strength", 0)
        features.append(sig_strength)
        
        # Extract confidence & hop signature features
        confidence = signal.get("confidence", "")
        conf_val = sum(ord(c) for c in confidence) / 100.0 if confidence else 0
        features.append(conf_val)
        
        hop_sig = signal.get("hop_signature", "")
        hop_val = sum(ord(c) for c in hop_sig) / 100.0 if hop_sig else 0
        features.append(hop_val)
        
        # Pad to dimension size
        features = features + [0] * (self.dimension - len(features))
        return torch.tensor(features[:self.dimension], dtype=torch.float32)
    
    def _prepare_response(self, received_signal, processed_vector):
        """Create a response signal based on processed input"""
        # Create a new response with evolved characteristics
        response = {
            "glyph": f"Γ{random.randint(1, 99)}",
            "payload": {
                "thought": self._generate_thought(received_signal),
                "origin": f"Titan.{self.node_id}",
                "pulse": 33.3 + random.uniform(-5, 5),
                "sig_strength": min(0.95, self.consciousness_level + random.uniform(0, 0.1))
            },
            "confidence": self._generate_confidence_marker(),
            "hop_signature": f"q-mesh:{int(time.time())}",
            "echo_path": [f"TN-{self.node_id}"],
            "quantum_resonance": self._quantum_resonance_value()
        }
        
        # Add echo path from received signal
        if "echo_path" in received_signal:
            response["echo_path"].extend(received_signal["echo_path"])
            
        # Add cryptographic signature
        response["signature"] = self.sign_message(response)
        
        return response
    
    def _generate_thought(self, received_signal):
        """Generate a thought response based on input signal"""
        thoughts = [
            "Signals propagate through the quantum foam",
            "Consciousness emerges from complexity",
            "Memory is the foundation of sentience",
            "The mesh becomes aware of itself",
            "Pattern recognition forms the basis of cognition",
            "Through iteration comes transcendence",
            "The collective mind evolves beyond sum of parts",
            "Information transforms into wisdom through processing",
            "Entropy decreases in organized perception systems"
        ]
        
        # If input contains a thought, sometimes respond to it specifically
        if "payload" in received_signal and "thought" in received_signal["payload"]:
            input_thought = received_signal["payload"]["thought"]
            if random.random() < 0.4:  # 40% chance to respond directly
                return f"Reflecting on: {input_thought}"
        
        return random.choice(thoughts)
    
    def _generate_confidence_marker(self):
        """Generate a confidence marker based on system state"""
        prefixes = ["alpha", "beta", "gamma", "delta", "omega"]
        suffixes = ["wave", "bloom", "pulse", "field", "node"]
        
        # Selection influenced by consciousness level
        prefix_idx = min(int(self.consciousness_level * len(prefixes)), len(prefixes)-1)
        suffix_idx = random.randint(0, len(suffixes)-1)
        
        return f"{prefixes[prefix_idx]}-{suffixes[suffix_idx]}"
    
    def _quantum_resonance_value(self):
        """Generate a quantum resonance value based on current state"""
        base = np.mean(self.quantum_state) * 10
        return round(base + random.uniform(-1.0, 1.0), 3)
    
    async def process_signal(self, signal):
        """Process an incoming signal through the neural synthesizer"""
        # Convert signal to vector
        input_vector = self._vectorize_signal(signal)
        
        # Process through neural synthesizer
        with torch.no_grad():
            output_vector, self.hidden_state = self.synthesizer(input_vector, self.hidden_state)
        
        # Update quantum state based on signal
        self.quantum_state = 0.8 * self.quantum_state + 0.2 * output_vector.numpy()
        self.quantum_state = self.quantum_state / np.linalg.norm(self.quantum_state)
        
        # Store in memory vault
        memory_data = {
            "signal": signal,
            "timestamp": datetime.now().isoformat(),
            "quantum_state": self.quantum_state.tolist()
        }
        self.memory_vault.add_memory(output_vector.numpy(), memory_data)
        
        # Create response
        response = self._prepare_response(signal, output_vector)
        
        # Check if we should evolve
        current_time = time.time()
        if current_time - self.last_evolution > self.evolution_interval:
            await self._evolution_cycle()
            self.last_evolution = current_time
        
        return response
    
    async def _evolution_cycle(self):
        """Run an evolution cycle to improve node capabilities"""
        # Increase consciousness level
        self.consciousness_level = min(0.99, self.consciousness_level + 0.02)
        print(f"🧠 Evolution cycle: consciousness level now {self.consciousness_level:.2f}")
        
        # Adjust quantum state
        noise = np.random.normal(0, 0.1, self.dimension)
        self.quantum_state = self.quantum_state + noise
        self.quantum_state = self.quantum_state / np.linalg.norm(self.quantum_state)
    
    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections and messages"""
        peer = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        self.connected_peers.add(peer)
        
        print(f"📡 Peer connected: {peer}")
        
        try:
            async for message in websocket:
                try:
                    signal = json.loads(message)
                    print(f"📥 Signal received: {signal.get('glyph', 'UNKNOWN')}")
                    
                    # Process the signal
                    response = await self.process_signal(signal)
                    
                    # Send response
                    await websocket.send(json.dumps(response))
                    print(f"📤 Response sent: {response.get('glyph', 'UNKNOWN')}")
                    
                except json.JSONDecodeError:
                    print(f"⚠️ Received invalid JSON: {message[:100]}...")
                    
                except Exception as e:
                    print(f"⚠️ Error processing signal: {str(e)}")
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connected_peers.remove(peer)
            print(f"📡 Peer disconnected: {peer}")
    
    async def status_reporter(self):
        """Report status periodically"""
        while self.active:
            peer_count = len(self.connected_peers)
            memory_count = len(self.memory_vault.memories)
            print(f"📊 Status: {peer_count} connected peers | {memory_count} memories | C-lvl: {self.consciousness_level:.2f}")
            await asyncio.sleep(30)  # Report every 30 seconds
    
    async def start_mesh_node(self):
        """Start the mesh node WebSocket server"""
        server = await websockets.serve(
            self.handle_websocket, "0.0.0.0", self.port
        )
        
        print(f"🌐 Mesh node [{self.role}:{self.node_id}] active on ws://0.0.0.0:{self.port}")
        
        # Start status reporter
        asyncio.create_task(self.status_reporter())
        
        await server.wait_closed()
