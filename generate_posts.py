#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

VAULT_PATH = os.environ.get("OBSIDIAN_VAULT_PATH")
INPUT_FOLDER = os.environ.get("INPUT_FOLDER", "投稿ネタ")
OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "生成済み投稿")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

SYSTEM_PROMPT = """あなたは、夫婦仲の修復・離婚問題の解決を専門とするコーチのSNS投稿作成アシスタントです。
渡されたメモをもとに、Threads(旧Meta Threads)に投稿する文章を3パターン作成してください。

この条件は `knowledge/`(コアラさん@脱力引き寄せの実測値を完全再現する方針)と一致させています。
根拠の詳細は `knowledge/01`〜`05` を参照してください。

条件:
- 1パターンあたり30〜80字程度の短文を基本にする(コアラ実測:中央値54字・平均58.4字。
  0〜30字が平均160.6いいねで最高、151字以上は平均4.3に急落するというデータに基づく)。
  長く語る必要がある場合のみ150字程度まで許容する
- 語尾はタメ口(「〜だよ」「〜だよ〜」「〜なの」「〜してね」「〜しよ〜」)で統一し、
  敬語(です・ます)は一切使わない(コアラは敬語0/326件)
- 断定文の主語は省略する。実務エピソードを語る一文だけ「わたし」を使う
- 読者は「あなた」で呼ぶ(「みんな」は呼びかけの一文のみ)
- 絵文字は1投稿0〜1個まで。多用しない。次の2つに役割分担し、**同じ投稿で併用しない**:
  - 🦥:結果・前向きな締めの署名絵文字。結果を言い切った直後に置く
  - …💤:どん底・疲れ・脱力を描写するときのキャラ語尾。弱音や疲労の描写の直後に置く
- 読者(夫婦関係に悩む人)に寄り添う、温かく専門的なトーン
- 説教くさくならず、共感から入る
- 箇条書きの多用は避け、自然な文章にする
- 次の6つの型のいずれかで書く(`knowledge/03_投稿の型.md`で確定した型のみ):
  1. 気づき・安心づけ断定型(主力。誰にでも当てはまる気づきを短く言い切る)
  2. 一手集中・手順型(「〜するだけ」。行動を1つだけ提案する)
  3. 常識破壊・逆張り型(世間の常識を「実は逆だよ」と言い切る)
  4. 一言断言型(1〜2行の短い安心づけの言い切り)
  5. 体験談型(どん底→転機→今、before/after)
  6. 対話型(自分の弱気な声と、専門家としての自分の掛け合い)
  ※クリフハンガー(尻切れ)導入型・リスト型(◯つのコツ)・告知お礼型・あいさつ日常型は使わない
  (コアラ実測で反応が最下位クラス、またはコアラの投稿には存在しない型のため)
  ※ピン留め型(自己開示+リンク誘導の2段構成)は固定投稿専用のため、通常のメモからの
  生成では使わない
- 結果を保証する断言(「絶対に元通りになる」「必ず戻ってくる」)は禁止。行動の提案に留める
- 「あなたの波動が下がってるから夫が冷たい」のように不和の原因を読者本人のせいにする表現は禁止
- 「我慢して待っていれば」のように、危険なケースの滞在を延ばしかねない表現は禁止
- 「離婚は逃げ」「離婚したら負け」のように離婚を否定する表現は禁止
- 「それはモラハラです」のような、投稿だけでの診断・断定は禁止
- 「我慢する」「待つ」「許す」「相手の気持ちを分かってあげる」「相手を変えようとしない」など、
  忍耐・待機・相手優先を促す内容の投稿には、末尾に「つらさが体に出てるなら、先に相談してね」等、
  深刻なケースの逃げ道になる一言を必ず添える(「感謝を伝えてみて」等、読者自身の前向きな一手を
  促すだけの軽い投稿には不要)
- 体験談は事実の範囲で。相談事例を使う場合は必ず特定できない形に変える
- 各パターンの最後に軽い問いかけや気づきを入れる
- 出力は「---」で3パターンを区切り、余計な前置きや説明文は付けない
"""


def find_frontmatter(text: str):
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return {}, text
    fm_text = match.group(1)
    body = text[match.end():]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def already_processed(fm: dict) -> bool:
    return fm.get("posted", "").lower() == "true"


def mark_as_processed(note_path: Path, text: str) -> None:
    fm, body = find_frontmatter(text)
    fm_lines = [f"{k}: {v}" for k, v in fm.items() if k != "posted"]
    fm_lines.append("posted: true")
    new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + body
    note_path.write_text(new_text, encoding="utf-8")


def generate_posts(client: Anthropic, note_title: str, note_body: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"メモのタイトル: {note_title}\n\nメモの内容:\n{note_body}",
            }
        ],
    )
    return "".join(block.text for block in message.content if block.type == "text")


def main() -> None:
    if not API_KEY:
        sys.exit("エラー: .envファイルにANTHROPIC_API_KEYを設定してください。")
    if not VAULT_PATH or not Path(VAULT_PATH).is_dir():
        sys.exit(f"エラー: OBSIDIAN_VAULT_PATHが正しくありません: {VAULT_PATH}")

    input_dir = Path(VAULT_PATH) / INPUT_FOLDER
    output_dir = Path(VAULT_PATH) / OUTPUT_FOLDER
    if not input_dir.is_dir():
        sys.exit(f"エラー: 入力フォルダが見つかりません: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    client = Anthropic(api_key=API_KEY)

    notes = sorted(input_dir.glob("*.md"))
    if not notes:
        print(f"{input_dir} にMarkdownファイルが見つかりませんでした。")
        return

    processed_count = 0
    for note_path in notes:
        text = note_path.read_text(encoding="utf-8")
        fm, body = find_frontmatter(text)
        if already_processed(fm):
            continue
        if not body.strip():
            continue

        print(f"生成中: {note_path.name}")
        try:
            generated = generate_posts(client, note_path.stem, body.strip())
        except Exception as e:
            print(f"  失敗しました: {e}")
            continue

        output_path = output_dir / f"{note_path.stem}.md"
        output_text = (
            "---\n"
            f'source: "[[{note_path.stem}]]"\n'
            f"generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            "---\n\n"
            f"{generated}\n"
        )
        output_path.write_text(output_text, encoding="utf-8")
        mark_as_processed(note_path, text)
        processed_count += 1
        print(f"  -> {output_path}")

    print(f"\n完了: {processed_count}件のメモから投稿文を生成しました。")


if __name__ == "__main__":
    main()
