import streamlit as st
from utils.audio_utils import transcribe_audio
from utils.gpt_utils import generate_markdown, generate_json
from utils.file_utils import save_json, save_markdown

st.set_page_config(page_title="AI求人要件整理アシスタント", layout="centered")
st.title("🎯 AI求人要件整理アシスタント")

# --- 入力選択 ---
input_option = st.radio("入力方法を選択", ["音声ファイルをアップロード", "テキストを入力"])
transcribed_text = ""

# --- 音声またはテキスト処理 ---
if input_option == "音声ファイルをアップロード":
    audio_file = st.file_uploader("🎙️ 音声ファイルをアップロード", type=["mp3", "m4a", "wav"])
    if audio_file:
        transcribed_text = transcribe_audio(audio_file)
else:
    transcribed_text = st.text_area("📝 クライアントヒアリングメモを貼り付け", height=200)

# --- タブ構成 ---
tab1, tab2 = st.tabs(["🧾 Markdown出力", "📊 JSON出力"])

with tab1:
    if st.button("生成（Markdown）", key="markdown_btn"):
        output_text = generate_markdown(transcribed_text)
        st.markdown(output_text)
        save_markdown(output_text)

with tab2:
    if st.button("生成（JSON）", key="json_btn"):
        json_text = generate_json(transcribed_text)
        st.code(json_text, language="json")
        save_json(json_text)


# import streamlit as st
# from openai import OpenAI
# import tempfile
# import json
# import os
# from dotenv import load_dotenv

# # .envファイルから環境変数を読み込み
# load_dotenv()

# # --- OpenAI API クライアント設定 ---
# api_key = os.environ.get("OPENAI_API_KEY")
# if not api_key:
#     st.error("❌ OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
#     st.stop()

# client = OpenAI(api_key=api_key)

# # --- ページ設定 ---
# st.set_page_config(page_title="AI求人要件整理アシスタント", layout="centered")
# st.title("🎯 AI求人要件整理アシスタント (MVP)")
# st.caption("クライアントヒアリング内容から求人票ドラフトを自動生成")

# # --- 入力方法選択 ---
# st.subheader("入力方法を選択")
# input_option = st.radio("選択してください", ["音声ファイルをアップロード", "テキストを入力"])

# transcribed_text = ""

# # --- 音声入力処理 ---
# if input_option == "音声ファイルをアップロード":
#     audio_file = st.file_uploader("🎙️ 音声ファイルをアップロード (.mp3, .m4a, .wav)", type=["mp3", "m4a", "wav"])
#     if audio_file is not None:
#         st.info("Whisperで文字起こし中...")
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
#             tmp.write(audio_file.read())
#             tmp_path = tmp.name
#         with open(tmp_path, "rb") as af:
#             transcript = client.audio.transcriptions.create(
#                 model="gpt-4o-mini-transcribe",
#                 file=af
#             )
#         transcribed_text = transcript.text
#         st.success("文字起こし完了！")
# else:
#     transcribed_text = st.text_area("📝 クライアントヒアリングメモを貼り付けてください", height=200)


# # --- タブ構成 ---
# tab1, tab2 = st.tabs(["🧾 Markdown出力（求人票）", "📊 JSON出力（構造化データ）"])

# # =========================================================
# # 🧾 タブ1：Markdown形式の求人票
# # =========================================================
# with tab1:
#     st.subheader("求人票（Markdown形式）")

#     if st.button("🔍 求人票を生成する"):
#         if not transcribed_text.strip():
#             st.warning("内容を入力または録音してください。")
#         else:
#             with st.spinner("AIがMarkdown形式の求人票を生成中..."):
#                 prompt = f"""
# あなたは優秀なRPOリクルーターです。
# 以下のヒアリング内容をもとに、求人票をMarkdown形式で生成してください。

# 出力フォーマット:
# # 求人票：{{職種名}}
# ## 会社概要
# ## ポジション概要
# ## 仕事内容
# ## 必須スキル
# ## 歓迎スキル
# ## 求める人物像
# ## 想定年収

# --- ヒアリング内容 ---
# {transcribed_text}
# """
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[{"role": "user", "content": prompt}],
#                     temperature=0.4,
#                 )
#                 output_text = response.choices[0].message.content

#             st.markdown("### ✅ 生成結果（Markdown）")
#             st.markdown(output_text)

#             # --- 保存・ダウンロード ---
#             with st.expander("💾 保存・ダウンロード"):
#                 if st.button("💾 Markdownを保存する"):
#                     save_path = "job_description.md"
#                     with open(save_path, "w") as f:
#                         f.write(output_text)
#                     st.success(f"保存しました: {save_path}")

#                 st.download_button(
#                     "📥 ダウンロード (Markdown)",
#                     output_text,
#                     file_name="job_description.md",
#                 )

#             # --- 修正リクエスト ---
#             st.markdown("### ✏️ 修正リクエスト")
#             refine_instruction = st.text_area("修正したい点（例：年収を追記してほしい）")

#             if st.button("🔄 再生成（修正版）"):
#                 with st.spinner("再生成中..."):
#                     refine_prompt = f"""
# 以下の求人票を、次の修正指示に基づいて改善してください。

# --- 修正指示 ---
# {refine_instruction}

# --- 元の求人票 ---
# {output_text}
# """
#                     response = client.chat.completions.create(
#                         model="gpt-4o-mini",
#                         messages=[{"role": "user", "content": refine_prompt}],
#                     )
#                     refined_text = response.choices[0].message.content
#                     st.markdown("### 🔁 修正版（AI出力）")
#                     st.markdown(refined_text)

# # =========================================================
# # 📊 タブ2：JSON形式の構造化求人データ
# # =========================================================
# with tab2:
#     st.subheader("構造化求人データ（JSON形式）")

#     if st.button("🔍 JSONを生成する"):
#         if not transcribed_text.strip():
#             st.warning("内容を入力または録音してください。")
#         else:
#             with st.spinner("AIが構造化データを生成中..."):
#                 json_prompt = f"""
# 以下のヒアリング内容をもとに、求人情報をJSON形式で構造化してください。
# キーは以下の通りです。

# {{ 
# "職種名": "",
# "会社概要": "",
# "ポジション概要": "",
# "仕事内容": "",
# "必須スキル": [],
# "歓迎スキル": [],
# "求める人物像": "",
# "想定年収": ""
# }}

# --- ヒアリング内容 ---
# {transcribed_text}
# """
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[{"role": "user", "content": json_prompt}],
#                     temperature=0.3,
#                 )
#                 json_text = response.choices[0].message.content

#             st.markdown("### ✅ 生成結果（JSON）")
#             st.code(json_text, language="json")

#             # --- JSON保存・ダウンロード ---
#             with st.expander("💾 保存・ダウンロード"):
#                 if st.button("💾 JSONを保存する"):
#                     save_path = "job_data.json"
#                     with open(save_path, "w") as f:
#                         f.write(json_text)
#                     st.success(f"保存しました: {save_path}")

#                 st.download_button(
#                     "📥 ダウンロード (JSON)",
#                     json_text,
#                     file_name="job_data.json",
#                 )


#         # --- JSON or Markdown 保存処理 ---
#         if st.button("💾 保存する"):
#             save_path = "job_data.json"
#             data = {
#                 "source_text": transcribed_text,
#                 "job_description": output_text
#             }
#             with open(save_path, "w") as f:
#                 json.dump(data, f, ensure_ascii=False, indent=2)
#             st.success(f"保存しました: {save_path}")

#         # --- ダウンロード機能 ---
#         st.download_button(
#             "📥 Markdownをダウンロード",
#             output_text,
#             file_name="job_description.md",
#         )