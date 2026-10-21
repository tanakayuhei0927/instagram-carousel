# instagram-carousel

レトロ16bit RPG風「ダイエット攻略」Instagramカルーセル（1080×1350px）。

## 生成方法

```bash
pip install Pillow
python3 make_slide_01.py   # -> slide_01.png（表紙）
python3 make_slide_02.py   # -> slide_02.png（共感：陥りやすいループ）
```

実行後、全テキストについて「キャンバス／枠からのはみ出し」と「欠けた字形（豆腐）」を自動チェックし、結果を表示します（2枚目は矢印などの装飾と文字の重なりも確認）。

`make_slide_02.py` は配色・フォント・ピクセル描画・リスを `make_slide_01.py` から読み込んで共有しています。

## フォント

`fonts/NotoSansJP-VF.ttf`（Noto Sans JP 可変ウェイト版, SIL Open Font License 1.1 — `fonts/OFL.txt`）
