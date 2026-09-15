# アカウント分析の進め方

コアラさん(土台)とゆきぴーさん(類似)のThreadsアカウントを分析して、
「引き寄せ × 夫婦仲」の新アカウントの設計図(ナレッジ)を作るための手順書です。

Windowsのパソコンで Claude Code(黒い画面)を開いて、上から順に進めてください。
専門知識は要りません。**Claudeに話しかけるだけ**です。

> **Claude Codeの開き方(Windows):**
> スタートボタンを右クリック →「ターミナル」または「Windows PowerShell」を開き、
> このプロジェクトのフォルダに移動してから `claude` と入力してEnter。
>
> ### 【重要】VS Codeの中のターミナルは使わないでください
>
> VS Code内蔵のターミナルで `claude` を動かすと、
> VS Code自身のログ(`update#setState`、`Extension host with pid ... exited` など)が
> 同じ画面に流れ込み、**Claude Codeの表示が壊れて操作できなくなります**。
>
> **必ずスタートボタンから開いた独立したPowerShell**を使ってください。
> VS Codeはこの作業では一切使いません(分析結果を読みたいときだけ開けば十分です)。
>
> 起動すると「このフォルダを信頼しますか」と聞かれます。
> **マウスでは選べません。↓キーで `Yes, I trust this folder` に移動してEnter**です。
> Claude Codeの選択画面はすべてこの操作になります。
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

## ⓪パソコンにこのプロジェクトを持ってくる(最初の1回だけ)

> ### 【前提】「コマンドプロンプト」と「PowerShell」は別物です
>
> どちらも黒い画面ですが、中身が違います。**このプロジェクトはPowerShellを使います。**
>
> | | コマンドプロンプト | PowerShell |
> |---|---|---|
> | 正体 | 古いほう | 新しいほう(今の標準) |
> | 行頭の表示 | `C:\Users\名前>` | **`PS`** `C:\Users\名前>` |
>
> **見分け方は行頭の `PS`。** これが付いていればPowerShellです。
>
> **開き方:** スタートボタンを右クリック →
> 「ターミナル」(Windows 11) または「Windows PowerShell」(Windows 10)
>
> もうひとつ便利な開き方:**エクスプローラーでフォルダを開き、
> 上のアドレスバーに `powershell` と入力してEnter**。
> そのフォルダの場所で開くので `cd` を打たずに済みます(スクショのリネームで使います)。
>
> **もしコマンドプロンプトを使う場合**、違うのは `$HOME` の書き方だけです。
> `$HOME` を `%USERPROFILE%` に読み替えてください
> (例:`cd %USERPROFILE%\Desktop`)。`git` や `claude` はどちらでも同じです。

### 0-1. Gitが入っているか確認

PowerShellを開いて:

```powershell
git --version
```

バージョンが出ればOK。`認識されていません` と出たら、
[Git for Windows](https://git-scm.com/download/win) をインストールしてください。
インストーラの選択肢は**全部そのまま「次へ」で構いません**。
終わったらPowerShellを一度閉じて開き直してから、もう一度確認します。

### 0-2. ダウンロードする

```powershell
cd $HOME\Desktop
git clone https://github.com/hotarukawashima-collab/hotaru-THREADS.git
cd hotaru-THREADS
git checkout claude/pensive-keller-eqi6gn
```

途中でブラウザが開いてGitHubのログインを求められたら、ログインして許可してください
(初回だけです。次からは聞かれません)。

デスクトップに `hotaru-THREADS` フォルダができて、
その中に `analysis` と `knowledge` のフォルダが入っていれば成功です。

> **最後の `git checkout` を忘れないでください。** これを実行しないと、
> `analysis` や `knowledge` のフォルダが見当たらない状態になります。

### 0-3. Claude Codeを起動する

```powershell
claude
```

これで準備完了です。以降はこの画面にお話しするだけで進みます。

> **Pythonはまだ要りません。** ①〜④(スクショの分析とナレッジ作り)は
> Claude Codeだけで完結します。Pythonが必要になるのは⑤の運用からなので、
> そのときに `README.md` の「3. セットアップ手順」をやれば大丈夫です。

### 作業を中断して、また次の日に再開するとき

```powershell
cd $HOME\Desktop\hotaru-THREADS
claude
```

この2行だけです。0-1と0-2はもうやらなくて構いません。

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

### 1-1. スクショをパソコンに用意する

**すでにパソコンのフォルダに入れてある場合は、1-2へ進んでください。**

まだiPhoneの中にある場合は、USBケーブルで繋ぐのが確実です。

1. iPhoneをUSBケーブルでパソコンに繋ぐ
2. iPhoneの画面に「このコンピュータを信頼しますか?」と出たら「**信頼**」をタップ
   (このとき**iPhoneのロックを解除しておいてください**。
   ロックしたままだとパソコン側でフォルダが空に見えます)
3. エクスプローラー → 左の「**PC**」の下の `Apple iPhone`
   → `Internal Storage` → `DCIM`
4. 中がフォルダだらけで見つからない場合は、
   **エクスプローラー右上の検索窓に `.png` と入力**してください。
   iPhoneのスクショはPNG、写真はJPGなので、これでスクショだけ絞り込めます。

**ケーブルがない場合:** iPhoneからGoogleフォトやGoogleドライブにアップロードして、
パソコンのブラウザからまとめてダウンロードするのが早いです。

### 1-2. 所定のフォルダにコピーする

エクスプローラーで95枚をドラッグするのは大変なので、PowerShellでコピーします。
プロジェクトのフォルダ(`hotaru-THREADS`)でPowerShellを開き、**1行ずつ**実行してください。

デスクトップに「コアラ」「ゆきぴー」というフォルダで分けてある場合の例:

```powershell
Copy-Item "$HOME\Desktop\コアラ\*" -Destination "analysis\accounts\koara\screenshots"
```

```powershell
Copy-Item "$HOME\Desktop\ゆきぴー\*" -Destination "analysis\accounts\yukipi\screenshots"
```

フォルダ名が違う場合は、`\Desktop\` のあとを実際の名前に書き換えてください。
**コピーなので元のフォルダはそのまま残ります。** 失敗しても元データは無事です。

枚数を確認します(これも1行ずつ)。

```powershell
(Get-ChildItem analysis\accounts\koara\screenshots\* -Include *.png,*.jpg,*.jpeg).Count
```

```powershell
(Get-ChildItem analysis\accounts\yukipi\screenshots\* -Include *.png,*.jpg,*.jpeg).Count
```

数字だけが表示されます。元のフォルダの枚数と一致していればOKです。

> **数が合わない場合**、元フォルダの中身を種類別に数えてみてください。
> `.heic` が混ざっていると、上のコピーから漏れています。
>
> ```powershell
> Get-ChildItem "$HOME\Desktop\コアラ" -File | Group-Object Extension | Select-Object Count, Name
> ```

### 1-3. 連番にリネームする

**並び順が分かるように**しておくと、「何枚目まで終わったか」の管理が楽になります。
また、連投(1/2、2/2のような投稿)を正しくつなげるために、**撮った順に並んでいること**が重要です。

> ### 【重要】PowerShellへの貼り付けは「1行ずつ」
>
> 複数行をまとめて貼ると、**改行が飲み込まれて行がくっつき**、
> 意図しない動作やエラーになります。
> **1行貼る → Enter → 結果を確認 → 次の1行**、の順で進めてください。
>
> 貼る前に、画面が `PS C:\...\hotaru-THREADS>` だけの状態(何も入力されていない)
> になっているか確認してください。前の入力が残っているとくっつきます。

#### 手順

プロジェクトのフォルダでPowerShellを開き、以下を**1行ずつ**実行します。

**①並び順を確認する**

```powershell
Get-ChildItem analysis\accounts\koara\screenshots\* -Include *.png | Sort-Object Name | Select-Object -First 5 Name, LastWriteTime
```

`IMG_9337.PNG` のように**桁数の揃った連番**で、日時も順に並んでいればOK。
名前がバラバラな場合は、次の②③の `Sort-Object Name` を
`Sort-Object LastWriteTime` に書き換えてください。

**②コアラをリネームする**

```powershell
$i=1; (Get-ChildItem analysis\accounts\koara\screenshots\* -Include *.png | Sort-Object Name) | ForEach-Object { Rename-Item $_.FullName -NewName ("koara_{0:D3}.png" -f $i); $i++ }
```

**③確認する**

```powershell
Get-ChildItem analysis\accounts\koara\screenshots\* -Include *.png | Select-Object -First 3 Name
```

`koara_001.png` `koara_002.png` `koara_003.png` と出れば成功です。

**④ゆきぴーをリネームする**

```powershell
$i=1; (Get-ChildItem analysis\accounts\yukipi\screenshots\* -Include *.png | Sort-Object Name) | ForEach-Object { Rename-Item $_.FullName -NewName ("yukipi_{0:D3}.png" -f $i); $i++ }
```

デスクトップの元フォルダを残しておけば、失敗しても何度でもやり直せます。

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
