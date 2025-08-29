# stegx/image_lsb.py
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Tuple


def _read_image(path: Path) -> Tuple[np.ndarray, Image.Image]:
    img = Image.open(path).convert("RGB")
    arr = np.array(img, dtype=np.uint8)
    return arr, img

def _write_image(arr: np.ndarray, out_path: Path, ref_img: Image.Image) -> None:
    Image.fromarray(arr.astype(np.uint8), mode="RGB").save(out_path, format="PNG", optimize=True)

def embed_bytes(in_png: str, out_png: str, payload: bytes) -> None:
    """
    Embed payload (bytes) into in_png and write out_png.
    Prepends 4-byte length header (big-endian) to payload before embedding.
    """
    arr, img = _read_image(Path(in_png))
    flat = arr.flatten()  # 1D view of all channel byte values

    header = len(payload).to_bytes(4, "big")
    full = header + payload

    bits = np.unpackbits(np.frombuffer(full, dtype=np.uint8)).astype(np.uint8)  # array of 0/1
    capacity = flat.size
    if bits.size > capacity:
        raise ValueError(f"Payload too large ({bits.size} bits) for image capacity ({capacity} bits)")

    # Insert bits into LSBs
   
    flat[: bits.size] = ((flat[: bits.size] & 0xFE) | (bits & 1)).astype(np.uint8)

    out_arr = flat.reshape(arr.shape)
    _write_image(out_arr, Path(out_png), img)

def extract_bytes(in_png: str) -> bytes:
    """
    Extract bytes embedded by embed_bytes.
    Returns the raw payload bytes (not including the 4-byte length header).
    """
    arr, _ = _read_image(Path(in_png))
    flat = arr.flatten()

    # First 32 bits -> length
    header_bits = flat[:32] & 1
    header_bytes = np.packbits(header_bits)
    payload_len = int.from_bytes(header_bytes.tobytes()[:4], "big")

    total_bits = 32 + payload_len * 8
    if total_bits > flat.size:
        raise ValueError("Image does not contain the declared payload length (corrupt or wrong image)")

    payload_bits = flat[32: total_bits] & 1
    payload_bytes = np.packbits(payload_bits).tobytes()
    return payload_bytes  # raw payload (as bytes)

# Convenience wrappers for compatibility with older names:
def hide_message(in_png: str, out_png: str, data_bytes: bytes) -> None:
    embed_bytes(in_png, out_png, data_bytes)

def reveal_message(in_png: str) -> bytes:
    return extract_bytes(in_png)

def embed_png(input_img, output_img, data):
    """Backward compatibility wrapper for old name"""
    return hide_message(input_img, output_img, data)

def extract_png(stego_path: str) -> bytes:
    """Wrapper for backward compatibility with old tests."""
    return reveal_message(stego_path)
