import zipfile
import xml.etree.ElementTree as ET
import os, sys

pptx_path = '/Users/junichi.takayama/Desktop/案件管理/DBJ_社史Webサイト提案/02_Materials/0826_オロ様ご確認【株式会社日本政策投資銀行御中】周年サイト提案書.pptx'

if not os.path.exists(pptx_path):
    print("File not found!")
    sys.exit(1)

with zipfile.ZipFile(pptx_path, 'r') as z:
    slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    # sort numerically
    slide_files.sort(key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', '')))
    
    print(f"Total slides: {len(slide_files)}\n")
    
    for idx, s_file in enumerate(slide_files, 1):
        slide_xml = z.read(s_file)
        tree = ET.fromstring(slide_xml)
        texts = [node.text for node in tree.iter() if node.tag.endswith('}t') and node.text]
        full_text = ' '.join([t.strip() for t in texts if t.strip()])
        
        # Check for yellow shapes or specific mentions
        # In PPTX XML, yellow fill is often solidFill -> srgbClr val="FFFF00" or similar, or schemeClr
        has_yellow = 'FFFF00' in slide_xml.decode('utf-8', errors='ignore').upper() or 'FFD700' in slide_xml.decode('utf-8', errors='ignore').upper() or 'E6B800' in slide_xml.decode('utf-8', errors='ignore').upper() or 'マル' in full_text or '黄色' in full_text or 'オロ' in full_text or '記載' in full_text
        
        print(f"Slide {idx:02d} ({s_file}):")
        if full_text:
            print(f"  [Text]: {full_text[:300]}")
        else:
            print(f"  [Text]: (No text / image only)")
        
        # Highlight potential target slides
        flags = []
        if 'オロ' in full_text:
            flags.append("オロ言及")
        if '記載' in full_text:
            flags.append("記載言及")
        if '未定' in full_text or '確認' in full_text or '貴社' in full_text:
            flags.append("確認/未定/貴社")
        if has_yellow:
            flags.append("黄色/該当キーワードあり")
            
        if flags:
            print(f"  >>> FLAGS: {', '.join(flags)}")
        print("-" * 60)
