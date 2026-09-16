#!/usr/bin/env python3
"""
ワイヤーフレームコマンドビルダー (1200pxコンテンツ幅用)
"""

CANVAS_W = 1440
CONTENT_W = 1200
MARGIN_X = (CANVAS_W - CONTENT_W) // 2  # 120px

# カラー定義
C_BG_MAIN   = {"r": 0.97, "g": 0.98, "b": 0.99}
C_WHITE     = {"r": 1.0, "g": 1.0, "b": 1.0}
C_TEXT_MAIN = {"r": 0.11, "g": 0.13, "b": 0.18}
C_TEXT_SUB  = {"r": 0.40, "g": 0.45, "b": 0.52}
C_PRIMARY   = {"r": 0.09, "g": 0.44, "b": 0.90}
C_GRAY_BG   = {"r": 0.93, "g": 0.95, "b": 0.97}
C_GRAY_BOX  = {"r": 0.88, "g": 0.91, "b": 0.94}
C_FOOTER_BG = {"r": 0.08, "g": 0.11, "b": 0.16}

def build_part_1(curr_y):
    cmds = []
    # 01. Header
    cmds.append({"action": "create_frame", "name": "01_Header", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 90, "bg": C_WHITE})
    cmds.append({"action": "create_text", "name": "Header_Logo", "x": MARGIN_X, "y": 32, "text": "BRAND LOGO", "fontSize": 22, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    cmds.append({"action": "create_text", "name": "Header_Nav", "x": 480, "y": 36, "text": "サービス特長   ｜   提供機能   ｜   導入事例   ｜   ご利用の流れ   ｜   FAQ", "fontSize": 14, "color": C_TEXT_MAIN})
    cmds.append({"action": "create_rect", "name": "Header_CTA_Btn", "x": MARGIN_X + CONTENT_W - 160, "y": 23, "width": 160, "height": 44, "cornerRadius": 6, "color": C_PRIMARY})
    cmds.append({"action": "create_text", "name": "Header_CTA_Text", "x": MARGIN_X + CONTENT_W - 135, "y": 37, "text": "お問い合わせ", "fontSize": 14, "fontStyle": "Bold", "color": C_WHITE})
    curr_y += 90

    # 02. First View
    cmds.append({"action": "create_frame", "name": "02_FirstView", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 600, "bg": C_GRAY_BG})
    cmds.append({"action": "create_text", "name": "FV_Tagline", "x": MARGIN_X, "y": 100, "text": "【業界シェアNo.1】次世代ビジネスプラットフォーム", "fontSize": 14, "fontStyle": "Bold", "color": C_PRIMARY})
    cmds.append({"action": "create_text", "name": "FV_MainCopy", "x": MARGIN_X, "y": 130, "width": 580, "text": "業務プロセスの自動化で\n組織の生産性を圧倒的に向上", "fontSize": 38, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    cmds.append({"action": "create_text", "name": "FV_SubCopy", "x": MARGIN_X, "y": 250, "width": 560, "text": "直感的な操作性と手厚いサポートで、導入初日から成果を実感。\n既存システムとのシームレスな連携も実現します。", "fontSize": 16, "color": C_TEXT_SUB})
    cmds.append({"action": "create_rect", "name": "FV_Primary_Btn", "x": MARGIN_X, "y": 350, "width": 240, "height": 56, "cornerRadius": 8, "color": C_PRIMARY})
    cmds.append({"action": "create_text", "name": "FV_Primary_BtnText", "x": MARGIN_X + 45, "y": 368, "text": "無料で資料を請求する", "fontSize": 15, "fontStyle": "Bold", "color": C_WHITE})
    cmds.append({"action": "create_rect", "name": "FV_Visual_Box", "x": MARGIN_X + 640, "y": 100, "width": 560, "height": 380, "cornerRadius": 12, "color": C_GRAY_BOX})
    cmds.append({"action": "create_text", "name": "FV_Visual_Label", "x": MARGIN_X + 800, "y": 280, "text": "【メインビジュアル / UIイメージ】\n(560px × 380px)", "fontSize": 16, "fontStyle": "Bold", "color": C_TEXT_SUB})
    curr_y += 600

    # 03. Trust Badges
    cmds.append({"action": "create_frame", "name": "03_TrustBadges", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 120, "bg": C_WHITE})
    cmds.append({"action": "create_text", "name": "Trust_Title", "x": MARGIN_X, "y": 25, "text": "導入実績 500社以上（一部抜粋）", "fontSize": 12, "fontStyle": "Bold", "color": C_TEXT_SUB})
    logo_w, logo_gap = 200, 50
    for i in range(5):
        lx = MARGIN_X + i * (logo_w + logo_gap)
        cmds.append({"action": "create_rect", "name": f"Logo_Box_{i+1}", "x": lx, "y": 55, "width": logo_w, "height": 40, "cornerRadius": 4, "color": C_GRAY_BG})
        cmds.append({"action": "create_text", "name": f"Logo_Text_{i+1}", "x": lx + 60, "y": 68, "text": f"CLIENT {i+1}", "fontSize": 13, "fontStyle": "Bold", "color": C_TEXT_SUB})
    curr_y += 120

    # 04. News
    cmds.append({"action": "create_frame", "name": "04_News", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 160, "bg": C_BG_MAIN})
    cmds.append({"action": "create_text", "name": "News_Heading", "x": MARGIN_X, "y": 35, "text": "NEWS", "fontSize": 22, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    news_items = [("2026.08.15", "PRESS", "新機能「AIレポート自動生成機能」をリリースしました。"), ("2026.08.01", "INFO", "夏季休業期間中のカスタマーサポート体制について")]
    for idx, (date, cat, title) in enumerate(news_items):
        ny = 35 + idx * 45
        cmds.append({"action": "create_text", "name": f"News_Date_{idx+1}", "x": MARGIN_X + 200, "y": ny, "text": date, "fontSize": 14, "color": C_TEXT_SUB})
        cmds.append({"action": "create_rect", "name": f"News_Badge_{idx+1}", "x": MARGIN_X + 300, "y": ny - 2, "width": 60, "height": 22, "cornerRadius": 3, "color": C_PRIMARY})
        cmds.append({"action": "create_text", "name": f"News_BadgeText_{idx+1}", "x": MARGIN_X + 310, "y": ny + 2, "text": cat, "fontSize": 10, "fontStyle": "Bold", "color": C_WHITE})
        cmds.append({"action": "create_text", "name": f"News_Title_{idx+1}", "x": MARGIN_X + 380, "y": ny, "width": 700, "text": title, "fontSize": 14, "color": C_TEXT_MAIN})
    curr_y += 160

    return cmds, curr_y


def build_part_2(curr_y):
    cmds = []
    # 05. Features
    cmds.append({"action": "create_frame", "name": "05_Features", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 650, "bg": C_WHITE})
    cmds.append({"action": "create_text", "name": "Svc_Title", "x": CANVAS_W // 2 - 150, "y": 50, "text": "選ばれる 3つの理由", "fontSize": 28, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    card_w, card_gap = 370, 45
    cards_data = [
        ("01", "直感的で迷わない操作UI", "誰でも簡単に使いこなせるUI設計で、導入時の学習コストを最小化。社内定着を早めます。"),
        ("02", "強力なデータ連携＆自動化", "既存の主要SaaSやデータベースとノーコードで接続可能。手作業をゼロへ導きます。"),
        ("03", "専任担当による伴走サポート", "導入設計から運用定着まで、専任のカスタマーサクセスチームが手厚くフォロー。")
    ]
    for idx, (num, title, desc) in enumerate(cards_data):
        cx = MARGIN_X + idx * (card_w + card_gap)
        cmds.append({"action": "create_rect", "name": f"Feature_Card_{idx+1}", "x": cx, "y": 130, "width": card_w, "height": 440, "cornerRadius": 12, "color": C_BG_MAIN})
        cmds.append({"action": "create_rect", "name": f"Feature_Img_{idx+1}", "x": cx + 20, "y": 150, "width": card_w - 40, "height": 200, "cornerRadius": 8, "color": C_GRAY_BOX})
        cmds.append({"action": "create_text", "name": f"Feature_Num_{idx+1}", "x": cx + 30, "y": 370, "text": f"POINT {num}", "fontSize": 12, "fontStyle": "Bold", "color": C_PRIMARY})
        cmds.append({"action": "create_text", "name": f"Feature_Title_{idx+1}", "x": cx + 30, "y": 395, "width": card_w - 60, "text": title, "fontSize": 18, "fontStyle": "Bold", "color": C_TEXT_MAIN})
        cmds.append({"action": "create_text", "name": f"Feature_Desc_{idx+1}", "x": cx + 30, "y": 430, "width": card_w - 60, "text": desc, "fontSize": 14, "color": C_TEXT_SUB})
    curr_y += 650

    # 06. Case Studies
    cmds.append({"action": "create_frame", "name": "06_CaseStudies", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 550, "bg": C_BG_MAIN})
    cmds.append({"action": "create_text", "name": "Case_Title", "x": CANVAS_W // 2 - 150, "y": 50, "text": "導入事例・活用実績", "fontSize": 28, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    c_card_w, c_card_gap = 580, 40
    cases_data = [
        ("株式会社テクノロジーパートナーズ 様", "作業時間を月間120時間削減。意思決定のスピードが倍増しました。", "IT・通信 / 従業員数 500名"),
        ("グローバルソリューションズ株式会社 様", "全社導入により部門間の情報分断を解消。売上150%UPに貢献。", "製造業 / 従業員数 1,200名")
    ]
    for idx, (company, headline, meta) in enumerate(cases_data):
        cx = MARGIN_X + idx * (c_card_w + c_card_gap)
        cmds.append({"action": "create_rect", "name": f"Case_Card_{idx+1}", "x": cx, "y": 120, "width": c_card_w, "height": 320, "cornerRadius": 12, "color": C_WHITE})
        cmds.append({"action": "create_rect", "name": f"Case_Img_{idx+1}", "x": cx + 24, "y": 144, "width": 180, "height": 180, "cornerRadius": 8, "color": C_GRAY_BOX})
        cmds.append({"action": "create_text", "name": f"Case_Meta_{idx+1}", "x": cx + 225, "y": 144, "text": meta, "fontSize": 12, "fontStyle": "Bold", "color": C_PRIMARY})
        cmds.append({"action": "create_text", "name": f"Case_Company_{idx+1}", "x": cx + 225, "y": 165, "width": 320, "text": company, "fontSize": 16, "fontStyle": "Bold", "color": C_TEXT_MAIN})
        cmds.append({"action": "create_text", "name": f"Case_Headline_{idx+1}", "x": cx + 225, "y": 205, "width": 320, "text": headline, "fontSize": 15, "color": C_TEXT_SUB})
        cmds.append({"action": "create_text", "name": f"Case_Link_{idx+1}", "x": cx + 225, "y": 290, "text": "事例の詳細を見る  →", "fontSize": 14, "fontStyle": "Bold", "color": C_PRIMARY})
    curr_y += 550

    return cmds, curr_y


def build_part_3(curr_y):
    cmds = []
    # 07. FAQ
    cmds.append({"action": "create_frame", "name": "07_FAQ", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 480, "bg": C_WHITE})
    cmds.append({"action": "create_text", "name": "FAQ_Title", "x": CANVAS_W // 2 - 120, "y": 50, "text": "よくあるご質問", "fontSize": 28, "fontStyle": "Bold", "color": C_TEXT_MAIN})
    faqs = [
        ("Q. 申し込みから利用開始までどのくらいの期間がかかりますか？", "最短3営業日でご利用可能です。サポート担当が初期設定までスムーズにご案内いたします。"),
        ("Q. 無料トライアル期間はありますか？", "はい、14日間の無料トライアルをご用意しております。すべての機能を制限なくお試しいただけます。"),
        ("Q. セキュリティ対策や動作環境について教えてください。", "ISO27001認証を取得しており、通信の暗号化や定期的なバックアップを徹底しております。")
    ]
    for idx, (q, a) in enumerate(faqs):
        fy = 130 + idx * 100
        cmds.append({"action": "create_rect", "name": f"FAQ_Box_{idx+1}", "x": MARGIN_X, "y": fy, "width": CONTENT_W, "height": 80, "cornerRadius": 8, "color": C_BG_MAIN})
        cmds.append({"action": "create_text", "name": f"FAQ_Q_{idx+1}", "x": MARGIN_X + 25, "y": fy + 18, "width": CONTENT_W - 50, "text": q, "fontSize": 15, "fontStyle": "Bold", "color": C_TEXT_MAIN})
        cmds.append({"action": "create_text", "name": f"FAQ_A_{idx+1}", "x": MARGIN_X + 25, "y": fy + 45, "width": CONTENT_W - 50, "text": a, "fontSize": 13, "color": C_TEXT_SUB})
    curr_y += 480

    # 08. CTA
    cmds.append({"action": "create_frame", "name": "08_CTA", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 300, "bg": C_PRIMARY})
    cmds.append({"action": "create_text", "name": "CTA_Title", "x": CANVAS_W // 2 - 300, "y": 60, "width": 600, "text": "まずは無料で機能をお試しください", "fontSize": 28, "fontStyle": "Bold", "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "CTA_Sub", "x": CANVAS_W // 2 - 280, "y": 105, "width": 560, "text": "導入のご相談や資料請求・お見積もりなど、お気軽にお問い合わせください。", "fontSize": 15, "color": C_WHITE})
    cmds.append({"action": "create_rect", "name": "CTA_Btn", "x": CANVAS_W // 2 - 140, "y": 160, "width": 280, "height": 56, "cornerRadius": 8, "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "CTA_BtnText", "x": CANVAS_W // 2 - 90, "y": 178, "text": "お問い合わせ・資料請求", "fontSize": 16, "fontStyle": "Bold", "color": C_PRIMARY})
    curr_y += 300

    # 09. Footer
    cmds.append({"action": "create_frame", "name": "09_Footer", "x": 0, "y": curr_y, "width": CANVAS_W, "height": 260, "bg": C_FOOTER_BG})
    cmds.append({"action": "create_text", "name": "Footer_Logo", "x": MARGIN_X, "y": 45, "text": "BRAND LOGO", "fontSize": 20, "fontStyle": "Bold", "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "Footer_Company", "x": MARGIN_X, "y": 80, "width": 300, "text": "株式会社サンプル\n〒100-0005 東京都千代田区丸の内1-1-1\nTEL: 03-1234-5678", "fontSize": 13, "color": C_TEXT_SUB})
    cmds.append({"action": "create_text", "name": "Footer_Nav_1", "x": MARGIN_X + 450, "y": 45, "text": "サービス特長\n提供機能\n導入事例\nご利用の流れ", "fontSize": 13, "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "Footer_Nav_2", "x": MARGIN_X + 650, "y": 45, "text": "お知らせ・ニュース\nよくある質問\n資料ダウンロード\nお問い合わせ", "fontSize": 13, "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "Footer_Nav_3", "x": MARGIN_X + 850, "y": 45, "text": "会社概要\nプライバシーポリシー\n利用規約", "fontSize": 13, "color": C_WHITE})
    cmds.append({"action": "create_text", "name": "Footer_Copy", "x": MARGIN_X, "y": 190, "text": "© 2026 Sample Brand Inc. All Rights Reserved.", "fontSize": 12, "color": C_TEXT_SUB})
    curr_y += 260

    return cmds, curr_y
