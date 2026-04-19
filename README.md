# Medical Evidence Evaluator (Prototype)

理学療法士を目指す学生向けに、**医療・健康情報の信頼性を可視化する Web アプリ試作**です。

## できること

- Google検索結果（またはデモデータ）を取得
- 以下3軸でスコアリング
  - 情報源の権威性（ドメイン等）
  - 複数ソースの一致度（検索結果間の語彙一致）
  - 医学的エビデンスレベル（メタ分析、RCT などのキーワード）
- 総合スコアとソース別スコアをUIで表示
- **各スコアの根拠（reasons）** を表示

> 注意: この実装は授業課題向けのプロトタイプです。臨床判断には必ず一次文献の精読と指導者確認を行ってください。

## 起動方法

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

ブラウザで `http://127.0.0.1:8000` を開いて利用します。

## Google Custom Search API を使う場合

以下の環境変数を設定すると、デモデータではなく実検索を利用します。

```bash
export GOOGLE_API_KEY="..."
export GOOGLE_CSE_ID="..."
```

未設定の場合は、UI確認用のデモデータを評価します。

## テスト

```bash
pytest -q
```

## 実装構成

- `app/main.py`: FastAPI API/UIエントリ、Google検索取得
- `app/evaluator.py`: スコアリングロジック
- `templates/index.html`: UI
- `static/app.js`, `static/style.css`: フロント実装

## 今後の改善案

1. PubMed / Crossref API 連携で文献種別を正確に同定
2. GRADE/Oxford CEBM などの評価規準を厳密実装
3. ソースの公開日・更新日を評価軸に追加
4. 「なぜこのスコアか」の説明可能性（根拠表示）を強化
5. 学生向けの引用補助（APA/Vancouver出力）

## 次アクション

- 改善計画は `docs/NEXT_STEPS.md` を参照してください。
