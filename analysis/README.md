# アカウント分析の進め方

コアラさん(土台)とゆきぴーさん(類似)のThreadsアカウントを分析して、
「引き寄せ × 夫婦仲」の新アカウントの設計図(ナレッジ)を作るための手順書です。

Windowsのパソコンで Claude Code(黒い画面)を開いて、上から順に進めてください。
専門知識は要りません。**Claudeに話しかけるだけ**です。

> **Claude Codeの開き方(Windows):**
> スタートボタンを右クリック →「ターミナル」または「Windows PowerShell」を開き、
> このプロジェクトのフォルダに移動してから `claude` と入力してEnter。
>
> ```powershell
> cd $HOME\Desktop\hotaru-THREADS
> claude
> ```
>
> Claude Codeをまだ入れていない場合は、先に以下を実行してください(初回だけ)。
>
> ```powershell
> npm install -g @anthropic-ai/claude-code
> ```
>
> (`npm` が無いと言われたら、先に [Node.js](https://nodejs.org/) をインストールしてください)

---

## 全体の流れ

```
①スクショを入れる
      ↓
②書き起こし   スクショ → posts.jsonl(文字データ)   ← ここだけ時間がかかる
      ↓
③分析         posts.jsonl → analysis.md(分析レポート)
      ↓
④設計         2つの分析レポート → knowledge/(新アカウントの設計図)
      ↓
⑤運用         knowledge/ を使って generate_posts.py で投稿を作る
```

**②と③を分けるのが一番のコツです。**
一度スクショを文字にしてしまえば、③以降は何度でもやり直せます。
「やっぱり違う切り口で分析して」と言っても、スクショを読み直す必要がありません。

---

## ①スクショを入れる

### 1-1. iPhoneのスクショをWindowsに移す

一番確実なのは **USBケーブルで繋ぐ方法**です。

1. iPhoneをUSBケーブルでパソコンに繋ぐ
2. iPhoneの画面に「このコンピュータを信頼しますか?」と出たら「**信頼**」をタップ
   (ここでロック解除しておかないと、パソコン側でフォルダが空に見えます)
3. パソコンで「エクスプローラー」を開く → 左側の「**PC**」の下に `Apple iPhone` が出る
4. `Apple iPhone` → `Internal Storage` → `DCIM` の中に写真が入っています
5. スクショを探して、全部コピーする

> **DCIMの中がフォルダだらけで見つからない場合:**
> エクスプローラーの検索窓(右上)に `.png` と入れて検索してください。
> iPhoneのスクショはPNG形式、写真はJPGなので、これでスクショだけ絞り込めます。

**ケーブルがない / うまくいかない場合:** iPhoneのGoogleフォトやGoogleドライブに
スクショをアップロードして、パソコンのブラウザからまとめてダウンロードするのが早いです。

### 1-2. 所定のフォルダに入れる

コピーしたスクショを、以下のフォルダに貼り付けてください。

- コアラさん → `analysis\accounts\koara\screenshots\`
- ゆきぴーさん → `analysis\accounts\yukipi\screenshots\`

### 1-3. 連番にリネームする(推奨)

**並び順が分かるように**しておくと、「何枚目まで終わったか」の管理が楽になります。

対象のフォルダをエクスプローラーで開き、アドレスバーに `powershell` と入力してEnter。
開いた画面に、以下をコピーして貼り付けてEnterを押してください。

```powershell
$files = Get-ChildItem -File | Where-Object { $_.Extension -match '\.(png|jpg|jpeg)$' } | Sort-Object Name
$i = 1
foreach ($f in $files) {
  Rename-Item $f.FullName -NewName ("koara_{0:D3}{1}" -f $i, $f.Extension.ToLower())
  $i++
}
Write-Host "$($files.Count) 枚のリネームが完了しました"
```

`koara_001.png` `koara_002.png` … という名前に一括で変わります。

> **ゆきぴーさんのフォルダで実行するときは**、上の `koara_` の部分を `yukipi_` に
> 書き換えてから貼り付けてください(2箇所ではなく1箇所だけです)。

**スクショを撮った順に並んでいるか、必ず目視で確認してください。**
iPhoneのファイル名(`IMG_1234.PNG`)は撮影順に番号が付くので、通常はこれで正しく並びます。
もし順番がおかしければ、`Sort-Object Name` の部分を `Sort-Object LastWriteTime` に変えて
やり直してください。

### 注意

スクショ画像そのものはGitHubには保存されません(容量が大きいため)。
パソコンの中にだけ置いておく形になります。書き起こした文字データの方が保存されます。

---

## ②書き起こし(15枚ずつ)

**全134枚 / 全10バッチ。1バッチ数分なので、通しで1時間前後です。**

| アカウント | 枚数 | バッチ数 |
|---|---|---|
| コアラさん | 95枚 | 7バッチ |
| ゆきぴーさん | 39枚 | 3バッチ |

ゆきぴーさんも**全部やります**。39枚なら絞るより全部読んだほうが、
「反応が良い投稿と悪い投稿の差」が見えるので分析の質が上がります。

### やり方

Claude Codeに、こう言ってください。

```
analysis/prompts/01_書き起こし.md の手順で、
analysis/accounts/koara/screenshots/ の 1〜15枚目を書き起こして、
analysis/accounts/koara/posts.jsonl に追記して
```

終わったら次のバッチ:

```
続けて 16〜30枚目をお願い
```

これを繰り返します。**1バッチ終わるごとに `analysis/進捗.md` にチェックを入れてください。**
途中で中断しても、どこから再開すればいいかが分かります。

コアラさんが終わったら、同じ要領でゆきぴーさん(`yukipi`)を3バッチ。

> **なぜ15枚ずつ?**
> 一度にたくさん読ませると、Claudeの「記憶の作業台」が溢れて、
> 後半の精度が落ちたり途中で止まったりします。小分けにすると確実です。

> **途中で画面が重くなってきたら:**
> Claude Codeで `/clear` と入力すると、会話がリセットされて軽くなります。
> 書き起こし済みの `posts.jsonl` はファイルに残っているので消えません。
> 再開するときは、また上の指示文をそのまま貼り付ければOKです。

---

## ③分析

書き起こしが終わったら、アカウントごとに:

```
analysis/prompts/02_分析.md の手順で、
analysis/accounts/koara/posts.jsonl を分析して、
analysis/accounts/koara/analysis.md に書いて
```

ゆきぴーさんも同じように実行します。

---

## ④設計(新アカウントのナレッジを作る)

2つの分析が揃ったら:

```
analysis/prompts/03_コンセプト設計.md の手順で、
2つの analysis.md をもとに knowledge/ の各ファイルを埋めて
```

ここで、`knowledge/` フォルダに新アカウントの設計図が完成します。

---

## ⑤運用

`knowledge/` の内容を `generate_posts.py` のシステムプロンプトに反映すれば、
Obsidianにメモを書くだけで、設計図どおりの投稿文が出てくるようになります。

やり方が分からなければ、Claude Codeに
「knowledge/ の内容を generate_posts.py に反映して」と言えば作業してくれます。
