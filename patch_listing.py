from pathlib import Path
import re

block = '''        <!-- ==========================================
             LISTING 1 — START
             ========================================== -->
        <div class="listing-card">
          <div class="listing-gallery" id="gallery-1">
            <img class="listing-img gallery-slide active" src="images/listings/4015-the-exchange/1.png" alt="4015 The Exchange listing photo">
            <button class="gallery-btn prev" onclick="changeSlide(event,'gallery-1',-1)">&#8249;</button>
            <button class="gallery-btn next" onclick="changeSlide(event,'gallery-1',1)">&#8250;</button>
            <div class="gallery-dots" id="dots-gallery-1">
              <span class="gallery-dot active" onclick="goToSlide('gallery-1',0)"></span>
            </div>
          </div>
          <div class="listing-body">
            <span class="listing-badge available">Available</span>
            <div class="listing-address">4015 The Exchange</div>
            <div class="listing-unit">Mississauga, ON · L5B 0N9</div>
            <div class="listing-details">
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
                1 Bed
              </div>
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16M4 6h16M4 18h7"/></svg>
                1 Bath
              </div>
              <div class="listing-detail">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/></svg>
                Balcony
              </div>
            </div>
            <div class="listing-rent">$2,200 <span>/ month</span></div>
            <div class="listing-avail">Available: Immediately</div>
            <button class="listing-cta" onclick="bookACall()">Book a Viewing</button>
          </div>
        </div>
        <!-- LISTING 1 — END -->'''

pattern = re.compile(r'<!--.*?LISTING 1 — START.*?-->.*?<!--\s*LISTING 1 — END\s*-->', re.DOTALL)

for path_str in ["index.html", "assets/index.html"]:
    path = Path(path_str)
    if not path.exists():
        print(f"Skipping missing file: {path}")
        continue
    text = path.read_text(encoding='utf-8')
    if not pattern.search(text):
        raise RuntimeError(f"LISTING 1 block not found in {path}")
    text = pattern.sub(block, text, count=1)
    path.write_text(text, encoding='utf-8')
    print(f"Updated {path}")

img_dir = Path('images/listings/4015-the-exchange')
img_dir.mkdir(parents=True, exist_ok=True)
img_file = img_dir / '1.png'
if not img_file.exists():
    img_file.write_bytes(
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc```\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    print(f"Created placeholder image: {img_file}")
else:
    print(f"Image already exists: {img_file}")
