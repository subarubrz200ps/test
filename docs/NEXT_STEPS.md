# Next Steps（改善ロードマップ）

前回プロトタイプの課題（評価根拠が弱い・再現性が低い・教育用途として説明不足）を解消するため、次は以下の順で進める。

## 1. 評価基準の“厳密化”

- **Evidence Pyramid を明示実装**
  - `meta-analysis > systematic review > RCT > cohort > case-control > case report > expert opinion`
- **判定をキーワード依存から脱却**
  - PubMed E-utilities / Crossref を使い、論文タイプ（Publication Type）を取得して判定する。
- **判定理由を必ず出力**
  - 例: `"RCTと明記"`, `"PubMed publication type=Randomized Controlled Trial"`

### Done条件
- 同じ入力に対して同じスコアが再現される。
- 各スコアに説明文（根拠）が紐づく。

---

## 2. 信頼性評価の“透明化”

- 権威性のスコアを「ドメイン一点評価」から改善
  - 著者情報、所属、査読誌か、ガイドライン発行主体（学会/政府）を加点。
- 一致度は「語彙一致」だけでなく
  - 主張（claim）単位の一致/不一致を可視化。
- 最終出力は
  - **総合点 + 3軸 + 根拠 + 注意点（限界）** を表示。

### Done条件
- UI上で「なぜその点数か」が読める。

---

## 3. 学生向けUXの強化

- レポート用途向けに
  - 文献リスト（Vancouver / APA）自動整形。
  - 重要文献の優先表示（高エビデンス順）。
- 授業課題向けテンプレート
  - 「検索式」「採用/除外理由」「結論」を自動で下書き出力。

### Done条件
- 学生がそのまま課題に転記できる最小テンプレートが生成できる。

---

## 4. 品質保証（必須）

- ユニットテスト
  - evidence classification
  - scoring weight
  - deterministic output
- E2Eテスト
  - 検索→評価→表示まで。
- しきい値検証
  - 教員レビューで妥当性確認（サンプルクエリ10本）。

### Done条件
- CIで自動実行し、主要ロジックの回帰を防止。

---

## 直近スプリント（最優先）

1. `evaluator.py` を Evidence Pyramid ベースへ更新
2. `details` に `reasons` フィールド追加
3. UIに「根拠表示」欄を追加
4. テスト追加（最低10ケース）
