import streamlit as st
from openai import OpenAI
import tempfile
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# --- OpenAI API クライアント設定 ---
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
    st.stop()

client = OpenAI(api_key=api_key)

# --- ページ設定 ---
st.set_page_config(page_title="AI求人要件整理アシスタント", layout="centered")
st.title("🎯 AI求人要件整理アシスタント (MVP)")
st.caption("クライアントヒアリング内容から求人票ドラフトを自動生成")

# --- 入力方法選択 ---
st.subheader("入力方法を選択")
input_option = st.radio("選択してください", ["音声ファイルをアップロード", "テキストを入力"])

transcribed_text = ""

# --- 音声入力処理 ---
if input_option == "音声ファイルをアップロード":
    audio_file = st.file_uploader("🎙️ 音声ファイルをアップロード (.mp3, .m4a, .wav)", type=["mp3", "m4a", "wav"])
    if audio_file is not None:
        st.info("Whisperで文字起こし中...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        with open(tmp_path, "rb") as af:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",  # Whisper相当モデル
                file=af
            )
        transcribed_text = transcript.text
        st.success("文字起こし完了！")
        st.text_area("文字起こし結果", transcribed_text, height=200)

# --- テキスト入力処理 ---
elif input_option == "テキストを入力":
    transcribed_text = st.text_area("📝 クライアントヒアリングメモを貼り付けてください", height=200)

# --- 解析ボタン ---
if st.button("🔍 求人票を生成する"):
    if transcribed_text.strip() == "":
        st.warning("内容を入力または録音してください。")
    else:
        with st.spinner("AIが求人票を整理しています..."):
            prompt = f"""
あなたは優秀なRPOリクルーターです。
以下のヒアリング内容をもとに、求人票をMarkdown形式で生成してください。

出力フォーマット:
# 求人票：{{職種名}}
## 会社概要
## ポジション概要
## 仕事内容
## 必須スキル
## 歓迎スキル
## 求める人物像
## 想定年収

--- ヒアリング内容 ---
{transcribed_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            output_text = response.choices[0].message.content

        st.markdown("### ✅ 生成結果（AI求人票）")
        st.markdown(output_text)

        # --- ダウンロード機能 ---
        st.download_button(
            "📥 Markdownをダウンロード",
            output_text,
            file_name="job_description.md",
        )