"""
Mīzān al-Ḥadīth — Classical Commentary Cache Downloader
Downloads structured commentary cache chunks for Kutub al-Sittah.
"""

import os
import sys
import time
import requests
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "data" / "commentary_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    {
        "slug": "bukhari",
        "name": "Sahih al-Bukhari (Fatḥ al-Bārī)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sahih_Al-Bukhari/sahih_al-bukhari_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    },
    {
        "slug": "muslim",
        "name": "Sahih Muslim (Sharḥ al-Nawawī)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sahih_Muslim/sahih_muslim_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    },
    {
        "slug": "tirmidhi",
        "name": "Jami` al-Tirmidhi (Tuḥfat al-Aḥwadhī)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sunan_Al-Tirmidhi/sunan_al-tirmidhi_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    },
    {
        "slug": "abudawud",
        "name": "Sunan Abi Dawud (ʿAwn al-Maʿbūd)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sunan_Abu-Dawud/sunan_abu-dawud_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    },
    {
        "slug": "nasai",
        "name": "Sunan an-Nasa'i (Ḥāshiyat al-Sindī)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sunan_Al-Nasai/sunan_al-nasai_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    },
    {
        "slug": "ibnmajah",
        "name": "Sunan Ibn Majah (Ḥāshiyat al-Sindī)",
        "url": "https://raw.githubusercontent.com/mhashim6/Open-Hadith-Data/master/Sunan_Ibn-Maja/sunan_ibn-maja_ahadith_mushakkala_mufassala.utf8.csv",
        "max_bytes": 5 * 1024 * 1024
    }
]

def download_cache():
    print("=" * 80)
    print("DOWNLOADING COMMENTARY SOURCE CACHE FOR KUTUB AL-SITTAH")
    print("=" * 80)
    for src in SOURCES:
        out_path = CACHE_DIR / f"{src['slug']}_sharh.csv"
        if out_path.exists() and out_path.stat().st_size >= 1024 * 1024:
            print(f"[CACHE HIT] {src['name']} already exists ({out_path.stat().st_size / (1024*1024):.2f} MB)")
            continue
        print(f"[FETCHING] {src['name']}...")
        t0 = time.time()
        try:
            resp = requests.get(src["url"], stream=True, timeout=30)
            resp.raise_for_status()
            downloaded = 0
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=512 * 1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if downloaded >= src["max_bytes"]:
                            break
            t1 = time.time()
            print(f"  -> Saved {downloaded / (1024*1024):.2f} MB in {t1 - t0:.2f}s to {out_path.name}")
        except Exception as e:
            print(f"  -> Failed to download {src['name']}: {e}")
    print("=" * 80)

if __name__ == "__main__":
    download_cache()
