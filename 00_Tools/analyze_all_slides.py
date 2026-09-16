import zipfile
import xml.etree.ElementTree as ET
import os

pptx_path = '/Users/junichi.takayama/Desktop/案件管理/DBJ_社史Webサイト提案/02_Materials/0826_オロ様ご確認【株式会社日本政策投資銀行御中】周年サイト提案書.pptx'

with zipfile.ZipFile(pptx_path, 'r') as z:
    slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
    slide_files.sort(key=lambda x: int(x.replace('ppt/slides/slide', '').replace('.xml', '')))
    
    print(f"=== PPTX Analysis: {len(slide_files)} Slides ===\n")
    
    for idx, s_file in enumerate(slide_files, 1):
        slide_xml = z.read(s_file).decode('utf-8', errors='ignore')
        tree = ET.fromstring(slide_xml)
        texts = [node.text.strip() for node in tree.iter() if node.tag.endswith('}t') and node.text and node.text.strip()]
        
        full_text = ' '.join(texts)
        
        # Check if contains オロ or 記載 or 担当 or イエロー / 黄色 or TODO or あああ
        important = False
        reasons = []
        
        if 'オロ' in full_text:
            important = True
            reasons.append("オロ")
        if '記載' in full_text:
            important = True
            reasons.append("記載")
        if 'あああ' in full_text or '○○' in full_text or 'XX' in full_text:
            important = True
            reasons.append("未記入プレースホルダー(あああ/○○)")
        if '実績' in full_text or '体制' in full_text or 'プロフィール' in full_text:
            reasons.append("実績/体制/プロフィール")
            
        print(f"Slide {idx:02d}: {full_text[:120]}")
        if important:
            print(f"  *** IMPORTANT *** ({', '.join(reasons)})")
            print(f"  Full text: {full_text}\n")
