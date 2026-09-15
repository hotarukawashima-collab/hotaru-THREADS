# hotaru-THREADS

Obsidianに書いたメモから、Threads(SNS)の投稿文をClaudeが自動で作ってくれる仕組みです。
「メモを書く → このツールを実行 → 投稿文が3パターン、Obsidianの中に生成される」という流れになります。

## 1. これは何をするもの?

1. あなたがObsidianの「投稿ネタ」フォルダに、思いついたことをメモとして書きます。
   (夫婦仲修復・離婚問題の相談でよくあるテーマなど、ラフなメモでOK)
2. このツール(`generate_posts.py`というプログラム)を実行します。
3. Claudeがメモを読んで、Threadsに投稿できる文章を3パターン作り、
   「生成済み投稿」フォルダの中にObsidianのノートとして保存してくれます。
4. あなたはObsidianを開いて、生成された文章を見て、気に入ったものをコピーして投稿するだけです。

一度読み込んだメモは自動的に「処理済み」の印がついて、次回実行時に重複して処理されません。

## 2. 事前に必要なもの

- パソコン(このプロジェクトは **Windows** 前提で書いています)
- [Python](https://www.python.org/downloads/) (バージョン3.10以上)
  - すでに入っているか不安な場合は、**PowerShell** を開いて
    `python --version` と入力してみてください。バージョンが表示されればOKです。
  - **インストール時の注意:** インストーラの最初の画面で
    「**Add python.exe to PATH**」のチェックを必ず入れてください。
    ここを入れ忘れると、あとで `python は認識されていません` というエラーが出ます。

> **PowerShellの開き方:** スタートボタンを右クリック →「ターミナル」または「Windows PowerShell」。
> もしくは、対象フォルダをエクスプローラーで開いて、
> アドレスバーに `powershell` と入力してEnterでも開けます(そのフォルダで開くので便利です)。
- Claude(Anthropic)のAPIキー
  - https://console.anthropic.com/ にアクセスし、アカウントを作成 → 「API Keys」から発行できます。
  - このキーは他人に見せないでください(自分のClaude利用料金に直結する、いわば「合鍵」です)。
- Obsidianのアプリ(すでにお使いのものでOKです)

## 3. セットアップ手順(最初の1回だけ)

### 3-1. このプロジェクトをパソコンに用意する

このリポジトリのファイル一式(`generate_posts.py`、`requirements.txt`、`.env.example`)を、
パソコンの好きな場所(例: デスクトップに「hotaru-THREADS」というフォルダを作る)に置いてください。

### 3-2. 必要な部品をインストールする

PowerShellを開き、上記のフォルダに移動してから、次のコマンドを実行します。

```powershell
cd $HOME\Desktop\hotaru-THREADS
pip install -r requirements.txt
```

(デスクトップ以外に置いた場合は、`cd` のあとをその場所に変えてください)

### 3-3. 設定ファイルを作る

`.env.example` というファイルをコピーして、`.env` という名前のファイルを作ります。

```powershell
copy .env.example .env
```

作った `.env` をテキストエディタ(メモ帳など)で開き、以下を書き換えます。

- `ANTHROPIC_API_KEY` → 3.で発行したClaudeのAPIキーを貼り付ける
- `OBSIDIAN_VAULT_PATH` → 自分のObsidian Vault(ノートを保存しているフォルダ)の場所
- `INPUT_FOLDER` → メモを書くフォルダ名(初期値は「投稿ネタ」。Obsidian内に同名フォルダを作っておく)
- `OUTPUT_FOLDER` → 生成された投稿文を保存するフォルダ名(初期値は「生成済み投稿」。自動で作られます)

## 4. 使い方

1. Obsidianの「投稿ネタ」フォルダに、投稿したい内容のメモ(Markdownノート)を書く。
2. PowerShellで、プロジェクトのフォルダに移動し、次を実行する。

```powershell
python generate_posts.py
```

3. 「生成中: ○○.md」のように表示され、完了すると
   「完了: N件のメモから投稿文を生成しました。」と出ます。
4. Obsidianを開くと、「生成済み投稿」フォルダに、メモと同じ名前のノートが増えています。
   中に3パターンの投稿文が入っているので、気に入ったものを選んでThreadsに投稿してください。

## 5. もっと自動化したい場合

「メモを書いたら実行するのも忘れそう」という場合は、パソコンのスケジュール機能を使って、
毎日決まった時間に自動実行することもできます。

Windowsなら「**タスクスケジューラ**」(スタートメニューで「タスク」と検索すると出てきます)で、
毎日決まった時間に `python generate_posts.py` を実行する設定ができます。

設定方法が分からない場合は、そのままお知らせください。手順をご案内します。

## 6. うまくいかないとき

- `エラー: .envファイルにANTHROPIC_API_KEYを設定してください。`
  → `.env` ファイルにAPIキーが正しく貼り付けられているか確認してください。
- `エラー: OBSIDIAN_VAULT_PATHが正しくありません`
  → Vaultフォルダの場所(パス)が間違っています。Obsidianの「Vaultを開く」画面などで正確な場所を確認してください。
- `エラー: 入力フォルダが見つかりません`
  → Vaultの中に、`.env` の `INPUT_FOLDER` と同じ名前のフォルダを作ってください。
- `python は、内部コマンドまたは外部コマンド〜として認識されていません`
  → Pythonのインストール時に「Add python.exe to PATH」のチェックが入っていません。
    Pythonをもう一度インストールし直して、最初の画面でチェックを入れてください。
- `pip は認識されていません`
  → 上と同じ原因です。応急処置として `py -m pip install -r requirements.txt` でも動きます。

## 7. アカウント分析 → ナレッジ作り

参考アカウントのスクショを分析して、新アカウント(引き寄せ×夫婦仲)の設計図を作る手順は
`analysis/README.md` にまとめてあります。

```
①スクショを入れる  → analysis/accounts/◯◯/screenshots/
②書き起こし        → posts.jsonl(15枚ずつ、Claude Codeに読ませる)
③分析              → analysis.md
④設計              → knowledge/(新アカウントの設計図)
⑤運用              → knowledge/ を generate_posts.py に反映
```

`knowledge/05_NGリスト.md` だけは、分析結果より優先される安全ルールです。必ず目を通してください。
