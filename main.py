from titan_genesis_core import TitanGenesisCore
import asyncio

if __name__ == "__main__":
    print("🧬 Spawning Titan Node")
    titan = TitanGenesisCore(role="Prime")
    asyncio.run(titan.start_mesh_node())
