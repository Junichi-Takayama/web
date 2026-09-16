#!/usr/bin/env python3
"""
HTML/CSS → Figma 一括自動描画エンジン (HTMLToFigmaEngine)
相対座標系・ネスト構造の厳格計算版
- 既存キャンバスの要素削除なし (clear_canvas非実行)
- 親フレーム基準の相対座標 (x, y) によるはみ出し・崩れの完全防止
"""

import re
import json
import urllib.request
from bs4 import BeautifulSoup, Tag

def parse_color(color_str):
    if not color_str:
        return None
    color_str = color_str.strip().lower()
    if color_str in ['transparent', 'none']:
        return None
    
    if color_str.startswith('#'):
        hex_code = color_str.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join([c*2 for c in hex_code])
        if len(hex_code) == 6:
            r = int(hex_code[0:2], 16) / 255.0
            g = int(hex_code[2:4], 16) / 255.0
            b = int(hex_code[4:6], 16) / 255.0
            return {"r": round(r, 3), "g": round(g, 3), "b": round(b, 3)}
    
    m = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color_str)
    if m:
        r = int(m.group(1)) / 255.0
        g = int(m.group(2)) / 255.0
        b = int(m.group(3)) / 255.0
        return {"r": round(r, 3), "g": round(g, 3), "b": round(b, 3)}
    
    color_map = {
        'white': {"r": 1.0, "g": 1.0, "b": 1.0},
        'black': {"r": 0.0, "g": 0.0, "b": 0.0},
        'slate-900': {"r": 0.06, "g": 0.09, "b": 0.16},
        'slate-800': {"r": 0.12, "g": 0.16, "b": 0.23},
        'blue-600': {"r": 0.15, "g": 0.39, "b": 0.92},
        'gray-100': {"r": 0.95, "g": 0.96, "b": 0.98}
    }
    return color_map.get(color_str, None)

def parse_px(val_str, default=0):
    if not val_str:
        return default
    m = re.search(r'(-?\d+(\.\d+)?)', str(val_str))
    if m:
        return float(m.group(1))
    return default

class HTMLToFigmaEngine:
    def __init__(self, bridge_url="http://localhost:3030/push"):
        self.bridge_url = bridge_url
        self.commands = []
        self.key_counter = 0

    def gen_key(self, prefix="node"):
        self.key_counter += 1
        return f"{prefix}_{self.key_counter}"

    def parse_inline_style(self, style_attr):
        styles = {}
        if not style_attr:
            return styles
        for item in style_attr.split(';'):
            if ':' in item:
                k, v = item.split(':', 1)
                styles[k.strip().lower()] = v.strip()
        return styles

    def convert_html_to_commands(self, html_content, artboard_name="PC_Top_Wireframe_1440px", artboard_width=1440, x_offset=0, y_offset=0):
        soup = BeautifulSoup(html_content, 'html.parser')
        self.commands = []

        root_key = "artboard"
        self.commands.append({
            "action": "create_frame",
            "key": root_key,
            "name": artboard_name,
            "x": x_offset,
            "y": y_offset,
            "width": artboard_width,
            "height": 2000,
            "bg": {"r": 0.98, "g": 0.98, "b": 0.99},
            "clipsContent": False
        })

        body = soup.find('body') or soup
        current_y = 0

        sections = [c for c in body.children if isinstance(c, Tag) and c.name in ['header', 'section', 'footer', 'nav', 'main', 'div']]

        for sec in sections:
            sec_height = self._process_section(sec, root_key, current_y, artboard_width)
            current_y += sec_height

        self.commands[0]["height"] = max(current_y, 800)
        return self.commands

    def _process_section(self, element, parent_key, y_offset, artboard_width):
        styles = self.parse_inline_style(element.get('style', ''))
        
        classes = element.get('class', [])
        sec_name = element.get('id') or (classes[0] if isinstance(classes, list) and classes else element.name)
        sec_key = self.gen_key("sec")
        
        bg_color = parse_color(styles.get('background-color') or styles.get('background')) or {"r": 1.0, "g": 1.0, "b": 1.0}
        sec_height = parse_px(styles.get('height'), 300)
        border_color = parse_color(styles.get('border-color'))
        border_width = parse_px(styles.get('border-width'), 1)

        cmd = {
            "action": "create_frame",
            "key": sec_key,
            "parentKey": parent_key,
            "name": f"Section_{sec_name}",
            "x": 0,
            "y": y_offset, # 親(アートボード)の直下なのでy_offset
            "width": artboard_width,
            "height": sec_height,
            "bg": bg_color,
            "clipsContent": False
        }
        if border_color:
            cmd["borderColor"] = border_color
            cmd["borderWidth"] = border_width

        self.commands.append(cmd)

        pad_top = parse_px(styles.get('padding-top'), 40)
        pad_bottom = parse_px(styles.get('padding-bottom'), 40)
        pad_left = parse_px(styles.get('padding-left'), 120) or 120
        pad_right = parse_px(styles.get('padding-right'), 120) or 120
        container_width = artboard_width - pad_left - pad_right

        # 親フレーム(sec_key)内部の相対座標起点 (pad_left, pad_top)
        max_child_bottom = self._process_container(element, sec_key, pad_left, pad_top, container_width)
        final_height = max(sec_height, max_child_bottom + pad_bottom)
        cmd["height"] = final_height
        return final_height


    def _process_container(self, parent_element, parent_key, start_x, start_y, parent_width):
        styles = self.parse_inline_style(parent_element.get('style', ''))
        display = styles.get('display', '').lower()
        is_flex = 'flex' in display
        flex_dir = styles.get('flex-direction', 'row').lower()
        is_row = is_flex and flex_dir != 'column'
        gap = parse_px(styles.get('gap'), 20 if is_flex else 0)

        # 親要素の枠内相対座標起点
        curr_x = start_x
        curr_y = start_y
        max_row_height = 0

        children = [c for c in parent_element.children if isinstance(c, Tag) or (str(c).strip() and not str(c).startswith('<!--'))]

        for child in children:
            if not isinstance(child, Tag):
                text_content = str(child).strip()
                if text_content:
                    self.commands.append({
                        "action": "create_text",
                        "parentKey": parent_key,
                        "name": "Text",
                        "text": text_content,
                        "x": curr_x,
                        "y": curr_y,
                        "width": parent_width,
                        "fontSize": 14,
                        "color": {"r": 0.2, "g": 0.2, "b": 0.2},
                        "textAutoResize": "HEIGHT"
                    })
                    curr_y += 28
                continue

            c_styles = self.parse_inline_style(child.get('style', ''))
            tag = child.name.lower()
            classes = child.get('class', [])
            if isinstance(classes, str): classes = [classes]

            c_width = parse_px(c_styles.get('width'))
            c_height = parse_px(c_styles.get('height'))

            # テキストタグ
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a', 'label', 'li', 'strong']:
                text_str = child.get_text().strip()
                if not text_str: continue

                font_size = parse_px(c_styles.get('font-size'))
                if not font_size:
                    if tag == 'h1': font_size = 36
                    elif tag == 'h2': font_size = 28
                    elif tag == 'h3': font_size = 22
                    elif tag == 'h4': font_size = 18
                    else: font_size = 14

                font_weight = c_styles.get('font-weight', '')
                font_style = "Bold" if ('bold' in font_weight or tag in ['h1', 'h2', 'h3', 'h4', 'strong']) else "Regular"
                color = parse_color(c_styles.get('color')) or {"r": 0.15, "g": 0.15, "b": 0.15}
                align = c_styles.get('text-align', 'left').upper()
                if align not in ['LEFT', 'CENTER', 'RIGHT']: align = 'LEFT'

                width = c_width or (parent_width if not is_row else 200)

                self.commands.append({
                    "action": "create_text",
                    "parentKey": parent_key,
                    "name": f"{tag.upper()}_{text_str[:12]}",
                    "text": text_str,
                    "x": curr_x,
                    "y": curr_y,
                    "width": width,
                    "fontSize": font_size,
                    "fontStyle": font_style,
                    "color": color,
                    "textAlignHorizontal": align,
                    "textAutoResize": "HEIGHT"
                })

                elem_h = font_size * 1.5 + 8
                if is_row:
                    curr_x += width + gap
                    max_row_height = max(max_row_height, elem_h)
                else:
                    curr_y += elem_h + gap

            # 画像プレースホルダー
            elif tag in ['img', 'svg'] or 'img-placeholder' in classes or 'placeholder' in classes:
                w = c_width or 300
                h = c_height or 200
                bg = parse_color(c_styles.get('background-color')) or {"r": 0.88, "g": 0.9, "b": 0.93}
                radius = parse_px(c_styles.get('border-radius'), 8)

                rect_key = self.gen_key("img")
                self.commands.append({
                    "action": "create_rect",
                    "key": rect_key,
                    "parentKey": parent_key,
                    "name": "Image_Placeholder",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "color": bg,
                    "cornerRadius": radius
                })
                alt_text = child.get('alt') or "【 UI / 画像イメージ 】"
                self.commands.append({
                    "action": "create_text",
                    "parentKey": rect_key,
                    "name": "Img_Label",
                    "text": alt_text,
                    "x": max(10, w / 2 - 80),
                    "y": max(10, h / 2 - 10),
                    "fontSize": 12,
                    "color": {"r": 0.5, "g": 0.5, "b": 0.5}
                })

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, h)
                else:
                    curr_y += h + gap

            # ボタン
            elif tag == 'button' or 'btn' in classes or 'button' in classes:
                btn_text = child.get_text().strip() or "Button"
                w = c_width or 180
                h = c_height or 48
                bg = parse_color(c_styles.get('background-color')) or {"r": 0.15, "g": 0.39, "b": 0.92}
                radius = parse_px(c_styles.get('border-radius'), 6)

                btn_key = self.gen_key("btn")
                self.commands.append({
                    "action": "create_rect",
                    "key": btn_key,
                    "parentKey": parent_key,
                    "name": f"Btn_{btn_text[:10]}",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "color": bg,
                    "cornerRadius": radius
                })
                text_color = parse_color(c_styles.get('color')) or {"r": 1.0, "g": 1.0, "b": 1.0}
                self.commands.append({
                    "action": "create_text",
                    "parentKey": btn_key,
                    "name": "Btn_Label",
                    "text": btn_text,
                    "x": 16,
                    "y": (h - 16) / 2,
                    "fontSize": 14,
                    "fontStyle": "Bold",
                    "color": text_color,
                    "textAutoResize": "WIDTH_AND_HEIGHT"
                })

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, h)
                else:
                    curr_y += h + gap

            # サブコンテナ (div, nav など)
            else:
                w = c_width or (parent_width if not is_row else (parent_width / max(len(children), 1) - gap))
                h = c_height or 80
                bg = parse_color(c_styles.get('background-color'))
                radius = parse_px(c_styles.get('border-radius'), 0)
                border_color = parse_color(c_styles.get('border-color'))
                border_width = parse_px(c_styles.get('border-width'), 1)

                frame_key = self.gen_key("frame")
                cmd = {
                    "action": "create_frame",
                    "key": frame_key,
                    "parentKey": parent_key,
                    "name": f"Frame_{classes[0] if classes else tag}",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "bg": bg,
                    "cornerRadius": radius,
                    "clipsContent": False
                }
                if border_color:
                    cmd["borderColor"] = border_color
                    cmd["borderWidth"] = border_width

                self.commands.append(cmd)

                pad_t = parse_px(c_styles.get('padding-top') or c_styles.get('padding'), 16)
                pad_l = parse_px(c_styles.get('padding-left') or c_styles.get('padding'), 16)
                pad_r = parse_px(c_styles.get('padding-right') or c_styles.get('padding'), 16)
                pad_b = parse_px(c_styles.get('padding-bottom') or c_styles.get('padding'), 16)

                # 重要: 子コンテナの内部要素は、その子コンテナ(frame_key)の相対座標 (pad_l, pad_t) からスタート
                sub_bottom = self._process_container(child, frame_key, pad_l, pad_t, w - pad_l - pad_r)
                actual_h = max(h, sub_bottom + pad_b)
                cmd["height"] = actual_h

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, actual_h)
                else:
                    curr_y += actual_h + gap

        return (curr_y + max_row_height) if is_row else curr_y

    def send_to_figma(self):
        if not self.commands:
            print("[Engine] 送信するコマンドがありません。")
            return False

        data = json.dumps({"commands": self.commands}, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(self.bridge_url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as res:
                resp = json.loads(res.read().decode('utf-8'))
                print(f"[Engine Success] Figma Bridge に {resp.get('queued')} 件の描画コマンドを送信しました！")
                return True
        except Exception as e:
            print(f"[Engine Error] Figma Bridge Server に接続できませんでした: {e}")
            return False

        display = styles.get('display', '').lower()
        is_flex = 'flex' in display
        flex_dir = styles.get('flex-direction', 'row').lower()
        is_row = is_flex and flex_dir != 'column'
        gap = parse_px(styles.get('gap'), 20 if is_flex else 0)

        curr_x = start_x
        curr_y = start_y
        max_row_height = 0

        children = [c for c in parent_element.children if isinstance(c, Tag) or (str(c).strip() and not str(c).startswith('<!--'))]

        for child in children:
            if not isinstance(child, Tag):
                text_content = str(child).strip()
                if text_content:
                    self.commands.append({
                        "action": "create_text",
                        "parentKey": parent_key,
                        "name": "Text",
                        "text": text_content,
                        "x": curr_x,
                        "y": curr_y,
                        "width": parent_width,
                        "fontSize": 14,
                        "color": {"r": 0.2, "g": 0.2, "b": 0.2},
                        "textAutoResize": "HEIGHT"
                    })
                    curr_y += 30
                continue

            c_styles = self.parse_inline_style(child.get('style', ''))
            tag = child.name.lower()
            classes = child.get('class', [])
            if isinstance(classes, str): classes = [classes]

            c_width = parse_px(c_styles.get('width'))
            c_height = parse_px(c_styles.get('height'))

            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'a', 'label', 'li', 'strong']:
                text_str = child.get_text().strip()
                if not text_str: continue

                font_size = parse_px(c_styles.get('font-size'))
                if not font_size:
                    if tag == 'h1': font_size = 36
                    elif tag == 'h2': font_size = 28
                    elif tag == 'h3': font_size = 22
                    elif tag == 'h4': font_size = 18
                    else: font_size = 14

                font_weight = c_styles.get('font-weight', '')
                font_style = "Bold" if ('bold' in font_weight or tag in ['h1', 'h2', 'h3', 'h4', 'strong']) else "Regular"
                color = parse_color(c_styles.get('color')) or {"r": 0.15, "g": 0.15, "b": 0.15}
                align = c_styles.get('text-align', 'left').upper()
                if align not in ['LEFT', 'CENTER', 'RIGHT']: align = 'LEFT'

                width = c_width or (parent_width if not is_row else 200)

                self.commands.append({
                    "action": "create_text",
                    "parentKey": parent_key,
                    "name": f"{tag.upper()}_{text_str[:12]}",
                    "text": text_str,
                    "x": curr_x,
                    "y": curr_y,
                    "width": width,
                    "fontSize": font_size,
                    "fontStyle": font_style,
                    "color": color,
                    "textAlignHorizontal": align,
                    "textAutoResize": "HEIGHT"
                })

                elem_h = font_size * 1.5 + 10
                if is_row:
                    curr_x += width + gap
                    max_row_height = max(max_row_height, elem_h)
                else:
                    curr_y += elem_h + gap

            elif tag in ['img', 'svg'] or 'img-placeholder' in classes or 'placeholder' in classes:
                w = c_width or 300
                h = c_height or 200
                bg = parse_color(c_styles.get('background-color')) or {"r": 0.88, "g": 0.9, "b": 0.93}
                radius = parse_px(c_styles.get('border-radius'), 8)

                rect_key = self.gen_key("img")
                self.commands.append({
                    "action": "create_rect",
                    "key": rect_key,
                    "parentKey": parent_key,
                    "name": "Image_Placeholder",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "color": bg,
                    "cornerRadius": radius
                })
                alt_text = child.get('alt') or "【 UI / 画像イメージ 】"
                self.commands.append({
                    "action": "create_text",
                    "parentKey": rect_key,
                    "name": "Img_Label",
                    "text": alt_text,
                    "x": max(10, w / 2 - 80),
                    "y": max(10, h / 2 - 10),
                    "fontSize": 12,
                    "color": {"r": 0.5, "g": 0.5, "b": 0.5}
                })

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, h)
                else:
                    curr_y += h + gap

            elif tag == 'button' or 'btn' in classes or 'button' in classes:
                btn_text = child.get_text().strip() or "Button"
                w = c_width or 180
                h = c_height or 48
                bg = parse_color(c_styles.get('background-color')) or {"r": 0.15, "g": 0.39, "b": 0.92}
                radius = parse_px(c_styles.get('border-radius'), 6)

                btn_key = self.gen_key("btn")
                self.commands.append({
                    "action": "create_rect",
                    "key": btn_key,
                    "parentKey": parent_key,
                    "name": f"Btn_{btn_text[:10]}",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "color": bg,
                    "cornerRadius": radius
                })
                text_color = parse_color(c_styles.get('color')) or {"r": 1.0, "g": 1.0, "b": 1.0}
                self.commands.append({
                    "action": "create_text",
                    "parentKey": btn_key,
                    "name": "Btn_Label",
                    "text": btn_text,
                    "x": 16,
                    "y": (h - 16) / 2,
                    "fontSize": 14,
                    "fontStyle": "Bold",
                    "color": text_color,
                    "textAutoResize": "WIDTH_AND_HEIGHT"
                })

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, h)
                else:
                    curr_y += h + gap

            else:
                w = c_width or (parent_width if not is_row else (parent_width / max(len(children), 1) - gap))
                h = c_height or 100
                bg = parse_color(c_styles.get('background-color'))
                radius = parse_px(c_styles.get('border-radius'), 0)
                border_color = parse_color(c_styles.get('border-color'))
                border_width = parse_px(c_styles.get('border-width'), 1)

                frame_key = self.gen_key("frame")
                cmd = {
                    "action": "create_frame",
                    "key": frame_key,
                    "parentKey": parent_key,
                    "name": f"Frame_{classes[0] if classes else tag}",
                    "x": curr_x,
                    "y": curr_y,
                    "width": w,
                    "height": h,
                    "bg": bg,
                    "cornerRadius": radius,
                    "clipsContent": False
                }
                if border_color:
                    cmd["borderColor"] = border_color
                    cmd["borderWidth"] = border_width

                self.commands.append(cmd)

                pad_top = parse_px(c_styles.get('padding-top') or c_styles.get('padding'), 16)
                pad_left = parse_px(c_styles.get('padding-left') or c_styles.get('padding'), 16)
                pad_right = parse_px(c_styles.get('padding-right') or c_styles.get('padding'), 16)

                sub_bottom = self._process_container(child, frame_key, pad_left, pad_top, w - pad_left - pad_right)
                actual_h = max(h, sub_bottom + parse_px(c_styles.get('padding-bottom') or c_styles.get('padding'), 16))
                cmd["height"] = actual_h

                if is_row:
                    curr_x += w + gap
                    max_row_height = max(max_row_height, actual_h)
                else:
                    curr_y += actual_h + gap

        return (curr_y + max_row_height) if is_row else curr_y

    def send_to_figma(self):
        if not self.commands:
            print("[Engine] 送信するコマンドがありません。")
            return False

        data = json.dumps({"commands": self.commands}, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(self.bridge_url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as res:
                resp = json.loads(res.read().decode('utf-8'))
                print(f"[Engine Success] Figma Bridge に {resp.get('queued')} 件の描画コマンドを送信しました！")
                return True
        except Exception as e:
            print(f"[Engine Error] Figma Bridge Server に接続できませんでした: {e}")
            return False

        return current_y

    def send_to_figma(self):
        if not self.commands:
            print("[Engine] 送信するコマンドがありません。")
            return False

        data = json.dumps({"commands": self.commands}, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(self.bridge_url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as res:
                resp = json.loads(res.read().decode('utf-8'))
                print(f"[Engine Success] Figma Bridge に {resp.get('queued')} 件の描画コマンドを送信しました！")
                return True
        except Exception as e:
            print(f"[Engine Error] Figma Bridge Server に接続できませんでした: {e}")
            return False

