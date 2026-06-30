import struct
import zlib
from pathlib import Path

def create_simple_png(filepath):
    """Create a minimal valid PNG file"""
    width, height = 800, 600
    
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + crc
    
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png += png_chunk(b'IHDR', ihdr)
    
    # IDAT chunk - create simple gray image data
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter type none
        raw += b'\xf0\xf0\xf0' * width  # light gray RGB
    
    png += png_chunk(b'IDAT', zlib.compress(raw))
    
    # IEND chunk
    png += png_chunk(b'IEND', b'')
    
    Path(filepath).write_bytes(png)

# Create images
img_dir = Path('images/listings/4015-the-exchange')
img_dir.mkdir(parents=True, exist_ok=True)

for i in range(1, 8):
    filepath = img_dir / f'{i}.png'
    create_simple_png(filepath)
    print(f'Created {filepath}')

print('Done!')
