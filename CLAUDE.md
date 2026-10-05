# hotaru-THREADS

Threadsアカウント **なまけろ子(@namakeroko_hikiyose)** の運用。
**引き寄せの法則 × 夫婦仲。** コアラ(@koarasan_hikiyose)というアカウントの完全再現。

---

## ★ 日付と時間は、必ず日本時間(JST)

**このコンテナのOSはUTC。Claudeに渡される「今日の日付」もUTC基準。**
**日本時間とは最大9時間ずれる(JSTの0時〜9時のあいだ、1日前の日付になる)。**

```
日付を書く前に、必ずこれで確認する
    TZ=Asia/Tokyo date '+%Y-%m-%d %H:%M (%a)'
```

**投稿ファイル名・実測の記録・コミットメッセージの日付は、すべてJSTで書く。**
`.claude/settings.json` に `TZ=Asia/Tokyo` を入れてあるので、
**新しいセッションではBashコマンドが最初からJSTになる。**

---

## 運用者

| | |
|---|---|
| 呼び方 | **ぽーちゃん** |
| 本名 | 川嶋ほたる(「川島」ではない) |

### 絶対の方針(運用者の言葉)

> 「オリジナリティはいれないでほしい。型も文字数も投稿頻度も投稿時間も、
> すべてコアラと同じように運営したい。変えるのはテーマ、ターゲット、
> アカウントの設定だけ。」
> 「あくまでメインは引き寄せの法則」

---

## ディレクトリ

| | |
|---|---|
| `knowledge/` | ルール。**ここが最上位** |
| `analysis/` | 実測データ・観察 |
| `contents/` | 成果物(投稿・note) |
| `tools/` | 機械検査 |
| `reference/` | コアラの原文 |

**毎日の作業の手順は `HANDOFF_codex.md` に全部書いてある。**

---

## 投稿を出す前に必ず通す

```
python3 tools/inspect.py contents/_posts35_source.py YYYY-MM-DD
python3 tools/check_similarity.py contents/_posts35_source.py
```

**検査が通らないものは出さない。**

---

## git

**ブランチは `claude/pensive-keller-eqi6gn` 固定。**
**プルリクエストは、頼まれない限り作らない。**
