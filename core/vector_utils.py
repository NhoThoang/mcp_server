import hashlib

def embed_text(text: str):
    return [float((int(hashlib.sha256(text.encode()).hexdigest(), 16) % 1000) / 1000.0)] * 128
