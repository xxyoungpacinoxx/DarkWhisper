import uuid

def generate_node_address() -> str:
    # Generate a 512-character node address by concatenating 16 UUIDs
    return ''.join([uuid.uuid4().hex for _ in range(16)])
