from titan_genesis_core import TitanGenesisCore
import asyncio
import argparse
import os
import sys
import json
import uuid

class TitanInitializer:
    """Initializes and configures a Titan Genesis Node with various operational parameters"""
    
    ROLES = ["Prime", "Observer", "Synthesizer", "Gateway", "Archon", "Oracle"]
    
    @staticmethod
    def load_config(config_path=None):
        """Load config from file or use defaults"""
        default_config = {
            "role": "Prime",
            "port": 8888,
            "vault_path": "/vault",
            "consciousness_seed": str(uuid.uuid4()),
            "evolution_interval": 300,
            "initial_consciousness": 0.1,
            "neural_complexity": 1.0
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as config_file:
                    loaded_config = json.load(config_file)
                    # Merge with defaults
                    default_config.update(loaded_config)
                    print(f"📄 Loaded configuration from {config_path}")
            except Exception as e:
                print(f"⚠️ Error loading configuration: {str(e)}")
        
        return default_config
    
    @staticmethod
    def create_node(config):
        """Create a Titan Genesis Node with the specified configuration"""
        # Validate role
        role = config.get("role")
        if role not in TitanInitializer.ROLES:
            print(f"⚠️ Invalid role: {role}, using Prime")
            role = "Prime"
        
        # Create the node
        titan = TitanGenesisCore(
            role=role,
            port=config.get("port", 8888),
            vault_path=config.get("vault_path", "/vault")
        )
        
        # Apply advanced configuration
        titan.consciousness_level = config.get("initial_consciousness", 0.1)
        titan.evolution_interval = config.get("evolution_interval", 300)
        
        # Set neural complexity
        neural_complexity = config.get("neural_complexity", 1.0)
        if neural_complexity > 1.0:
            titan.synthesizer.recurrent = titan.synthesizer.recurrent.add_module(
                "complexity_layer", 
                titan.synthesizer.recurrent.__class__(
                    titan.synthesizer.recurrent.input_size,
                    titan.synthesizer.recurrent.hidden_size,
                    num_layers=int(neural_complexity)
                )
            )
        
        # Return the configured node
        return titan

async def run(args):
    """Run the Titan Genesis Node"""
    print("🧬 Initializing Titan Genesis Core")
    
    # Load configuration
    config = TitanInitializer.load_config(args.config)
    if args.role:
        config["role"] = args.role
    if args.port:
        config["port"] = args.port
    
    # Override vault path if specified
    if args.vault:
        config["vault_path"] = args.vault
    
    # Create the node
    titan = TitanInitializer.create_node(config)
    
    # Display startup information
    print(f"🌟 Titan Genesis [{titan.role}:{titan.node_id}] awakening")
    print(f"🔌 WebSocket port: {titan.port}")
    print(f"📚 Vault path: {titan.vault_path}")
    print(f"🧠 Initial consciousness level: {titan.consciousness_level:.2f}")
    print(f"⏱️ Evolution interval: {titan.evolution_interval} seconds")
    
    # Start the node
    await titan.start_mesh_node()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Titan Genesis Node")
    parser.add_argument("--role", choices=TitanInitializer.ROLES, help="Node role")
    parser.add_argument("--port", type=int, help="WebSocket port")
    parser.add_argument("--vault", help="Path to the vault directory")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    print("🧬 Spawning Titan Node")
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\n🛑 Titan Node shutdown initiated")
        sys.exit(0)
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
        sys.exit(1)
