from pathlib import Path
import re

block = '''        <!-- ==========================================
             LISTING 2 — START
             ========================================== -->
        <div class="listing-card">
          <div class="listing-gallery" id="gallery-2">
            <img class="listing-img gallery-slide active" src="images/listings/380-bristol-rd/1.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/2.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/3.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/4.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/5.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/6.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/7.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/8.png" alt="380 Bristol Rd W listing photo">
            <img class="listing-img gallery-slide" src="images/listings/380-bristol-rd/9.png" alt="380 Bristol Rd W listing photo">
            <button class="gallery-btn prev" onclick="changeSlide(event,'gallery-2',-1)">&#8249;</button>
            <button class="gallery-btn next" onclick="changeSlide(event,'gallery-2',1)">&#8250;</button>
            <div class="gallery-dots" id="dots-gallery-2">
              <span class="gallery-dot active" onclick="goToSlide('gallery-2',0)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',1)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',2)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',3)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',4)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',5)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',6)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',7)"></span>
              <span class="gallery-dot" onclick="goToSlide('gallery-2',8)"></span>
            </div>
          </div>
          <div class="listing-body">
            <span class="listing-badge available">Available</span>
            <div class="listing-address">380 Bristol Rd W</div>
            <div class="listing-unit">Mississauga, ON · L5R 2J7</div>
            <div class="listing-details">
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
                2 Bed
              </div>
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16M4 6h16M4 18h7"/></svg>
                1 Bath
              </div>
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
                650 sqft
              </div>
            </div>
            <div class="listing-rent">$2,000 <span>/ month</span></div>
            <div class="listing-avail">Available: Immediately</div>
            <button class="listing-cta" onclick="bookACall()">Book a Viewing</button>
          </div>
        </div>
        <!-- LISTING 2 — END -->'''

pattern = re.compile(r'<!--.*?LISTING 2 — START.*?-->.*?<!--\s*LISTING 2 — END\s*-->', re.DOTALL)

for path_str in ["index.html", "assets/index.html"]:
    path = Path(path_str)
    if not path.exists():
        print(f"Skipping missing file: {path}")
        continue
    text = path.read_text(encoding='utf-8')
    if not pattern.search(text):
        raise RuntimeError(f"LISTING 2 block not found in {path}")
    text = pattern.sub(block, text, count=1)
    path.write_text(text, encoding='utf-8')
    print(f"Updated {path}")

img_dir = Path('images/listings/380-bristol-rd')
img_dir.mkdir(parents=True, exist_ok=True)

def create_simple_png(filepath):
    """Create a minimal valid PNG file"""
    import struct
    import zlib
    width, height = 800, 600
    
    def png_chunk(chunk_type, data):
        chunk_len = struct.pack('>I', len(data))
        crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
        return chunk_len + chunk_type + data + crc
    
    png = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    png += png_chunk(b'IHDR', ihdr)
    
    raw = b''
    for y in range(height):
        raw += b'\x00'
        raw += b'\xf0\xf0\xf0' * width
    
    png += png_chunk(b'IDAT', zlib.compress(raw))
    png += png_chunk(b'IEND', b'')
    
    Path(filepath).write_bytes(png)

for i in range(1, 10):
    filepath = img_dir / f'{i}.png'
    create_simple_png(filepath)
    print(f'Created {filepath}')

print('Done!')
