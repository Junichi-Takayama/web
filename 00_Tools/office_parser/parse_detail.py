import pptx

pptx_path = '/Users/junichi.takayama/Desktop/案件管理/DBJ_社史Webサイト提案/02_Materials/0826_オロ様ご確認【株式会社日本政策投資銀行御中】周年サイト提案書.pptx'
prs = pptx.Presentation(pptx_path)

target_slides = [15, 29, 32, 34, 39, 43, 45, 46, 47, 49, 50, 51, 52]

for idx in range(len(prs.slides)):
    slide_num = idx + 1
    slide = prs.slides[idx]
    
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                t = ''.join(run.text for run in p.runs).strip()
                if t:
                    texts.append(t)
        elif shape.has_table:
            for row in shape.table.rows:
                r_text = ' | '.join(cell.text.strip().replace('\n', ' ') for cell in row.cells)
                if r_text:
                    texts.append(r_text)
                    
    full_text = '\n'.join(texts)
    
    # オロ、XXXX、記載、確認などが含まれるか、指定されたターゲットスライドであれば詳細表示
    if slide_num in target_slides or any(k in full_text for k in ['オロ', 'XXXX', 'xxxx', '黄色']):
        print(f"==========================================")
        print(f"=== Slide {slide_num} ===")
        print(f"==========================================")
        print(full_text)
        print("\n")
