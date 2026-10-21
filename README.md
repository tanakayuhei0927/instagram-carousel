# instagram-carousel

レトロ16bit RPG風「ダイエット攻略」Instagramカルーセル（1080×1350px）。

## 生成方法

```bash
pip install Pillow
python3 make_slide_01.py   # -> slide_01.png（表紙）
python3 make_slide_02.py   # -> slide_02.png（共感：陥りやすいループ）
python3 make_slide_03.py   # -> slide_03.png（攻略の基本：3つのヒント）
python3 make_slide_04.py   # -> slide_04.png（攻略①：野菜・きのこアイテム）
python3 make_slide_05.py   # -> slide_05.png（攻略②：たんぱく質アイテム）
python3 make_slide_06.py   # -> slide_06.png（攻略③：主食アイテム）
```

実行後、全テキストについて「キャンバス／枠からのはみ出し」と「欠けた字形（豆腐）」を自動チェックし、結果を表示します（矢印・アイコンなどの装飾と文字の重なりも確認）。

配色・フォント・文字描画とチェック・RPGウィンドウ・ピクセル部品・ドット絵アイコン・リス（表情とポーズ）は `rpg_common.py` に共通化しています。各 `make_slide_XX.py` は背景とレイアウトだけを持ちます。

## フォント

`fonts/NotoSansJP-VF.ttf`（Noto Sans JP 可変ウェイト版, SIL Open Font License 1.1 — `fonts/OFL.txt`）
