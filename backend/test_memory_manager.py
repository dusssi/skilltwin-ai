from app.memory.models import MemoryRecord
from app.memory.memory_manager import MemoryManager

memory = MemoryRecord(
    user_id="dushyant",
    goal="AI Internship"
)

manager = MemoryManager()

manager.save_memory(memory)

loaded = manager.load_memory("dushyant")

print(loaded)