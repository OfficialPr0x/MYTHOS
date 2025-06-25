import json
import websockets
import asyncio
import random
import uuid
import time
import sys
from datetime import datetime
import argparse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class SignalEmitter:
    def __init__(self, uri="ws://localhost:8888", identity="Dreamer.Σ", signal_file=None):
        self.uri = uri
        self.identity = identity
        self.signal_file = signal_file
        self.emitter_id = str(uuid.uuid4())[:6]
        
        # Generate or load emitter identity
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
        # Connection state
        self.connected = False
        self.received_signals = []
    
    def generate_signal(self):
        """Generate a signal with metasentient-grade characteristics"""
        glyphs = ["Ω", "Σ", "Φ", "Γ", "Λ", "Π", "Ψ"]
        thoughts = [
            "Signal is not noise",
            "The observer affects the observed",
            "Consciousness emerges from complexity",
            "Information requires context to become knowledge",
            "Recursion creates patterns of self-similarity",
            "The map is not the territory",
            "All models are wrong, some are useful",
            "The whole is greater than the sum of parts"
        ]
        
        # Create signal structure
        signal = {
            "glyph": f"{random.choice(glyphs)}{random.randint(1, 99)}",
            "payload": {
                "thought": random.choice(thoughts),
                "origin": self.identity,
                "pulse": round(random.uniform(30.0, 40.0), 1),
                "sig_strength": round(random.uniform(0.7, 0.95), 2),
                "timestamp": datetime.now().isoformat()
            },
            "confidence": self._generate_confidence(),
            "hop_signature": f"quantum-lock:v{random.randint(1, 5)}",
            "echo_path": [f"EM-{self.emitter_id}"],
            "metadata": {
                "emitter_version": "2.0",
                "entropy_bias": round(random.random(), 3),
                "recursion_depth": random.randint(1, 5)
            }
        }
        
        # Sign the signal
        signal["signature"] = self._sign_message(signal)
        
        return signal
    
    def _generate_confidence(self):
        """Generate a confidence marker"""
        prefixes = ["alpha", "beta", "gamma", "delta", "epsilon", "omega"]
        suffixes = ["bloom", "wave", "field", "pulse", "node", "circuit"]
        
        return f"{random.choice(prefixes)}-{random.choice(suffixes)}"
    
    def _sign_message(self, message):
        """Create a cryptographic signature for a signal"""
        message_bytes = json.dumps({k: v for k, v in message.items() if k != "signature"}).encode()
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return signature.hex()
    
    def load_signal_from_file(self):
        """Load a signal from a file"""
        if not self.signal_file:
            return None
            
        with open(self.signal_file) as f:
            signal = json.load(f)
        
        # Update with current identity and add signature
        if "payload" in signal and isinstance(signal["payload"], dict):
            signal["payload"]["origin"] = self.identity
            signal["payload"]["timestamp"] = datetime.now().isoformat()
        
        if "echo_path" not in signal or not isinstance(signal["echo_path"], list):
            signal["echo_path"] = []
        signal["echo_path"].insert(0, f"EM-{self.emitter_id}")
        
        # Sign the signal
        signal["signature"] = self._sign_message(signal)
        
        return signal
    
    async def emit_signal(self, interactive=False, count=1, interval=5):
        """Emit signals to the mesh node"""
        print(f"📡 Connecting to mesh node at {self.uri}")
        
        # Track total signals
        signals_sent = 0
        signals_received = 0
        
        try:
            async with websockets.connect(self.uri) as ws:
                self.connected = True
                print(f"🔗 Connected to mesh node as {self.identity}")
                
                # Signal emission loop
                while self.connected:
                    # Get signal to emit
                    if self.signal_file:
                        signal = self.load_signal_from_file()
                        if not signal:
                            print(f"⚠️ Failed to load signal from {self.signal_file}")
                            break
                    else:
                        signal = self.generate_signal()
                    
                    # Send signal
                    await ws.send(json.dumps(signal))
                    signals_sent += 1
                    print(f"📤 Signal emitted: {signal['glyph']} | thought: '{signal['payload']['thought']}'")
                    
                    # Wait for response
                    response = await ws.recv()
                    response_data = json.loads(response)
                    signals_received += 1
                    self.received_signals.append(response_data)
                    
                    thought = response_data.get("payload", {}).get("thought", "No thought")
                    origin = response_data.get("payload", {}).get("origin", "Unknown")
                    print(f"📥 Response: {response_data.get('glyph')} from {origin}")
                    print(f"   └── 💭 {thought}")
                    
                    # Check if we're done
                    if signals_sent >= count and not interactive:
                        break
                    
                    # Interactive mode: ask user to continue
                    if interactive:
                        print("\nOptions:")
                        print("  [s] Send another signal")
                        print("  [q] Quit")
                        choice = input("> ").strip().lower()
                        if choice != 's':
                            break
                    else:
                        # Wait before sending next signal
                        await asyncio.sleep(interval)
                
                print(f"\n✅ Session complete: {signals_sent} signals sent, {signals_received} responses received")
                
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ Connection to mesh node closed")
        except Exception as e:
            print(f"⚠️ Error connecting to mesh node: {str(e)}")

async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Emit signals to a Titan Genesis mesh node")
    parser.add_argument("--uri", default="ws://localhost:8888", help="WebSocket URI of the mesh node")
    parser.add_argument("--identity", default="Dreamer.Σ", help="Identity of the emitter")
    parser.add_argument("--file", help="Path to a JSON file containing a signal")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--count", type=int, default=1, help="Number of signals to send")
    parser.add_argument("--interval", type=float, default=5, help="Interval between signals (seconds)")
    
    args = parser.parse_args()
    
    # Create and run emitter
    emitter = SignalEmitter(
        uri=args.uri,
        identity=args.identity,
        signal_file=args.file
    )
    
    await emitter.emit_signal(
        interactive=args.interactive,
        count=args.count,
        interval=args.interval
    )

if __name__ == "__main__":
    asyncio.run(main())
