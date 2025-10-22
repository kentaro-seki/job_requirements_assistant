import streamlit as st
from .config import get_openai_client

def generate_markdown(text):
    """ヒアリング内容からMarkdown形式の求人票を生成"""
    client = get_openai_client()
    with st.spinner("Markdown求人票を生成中..."):
        prompt = f"""
あなたは優秀なRPOリクルーターです。
以下のヒアリング内容をもとに求人票をMarkdown形式で生成してください。

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
{text}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
    return response.choices[0].message.content


def generate_json(text):
    """ヒアリング内容をJSON構造化"""
    client = get_openai_client()
    with st.spinner("構造化中..."):
        prompt = f"""
以下のヒアリング内容をもとに、求人情報をJSON形式で出力してください。

{{ 
"職種名": "",
"会社概要": "",
"ポジション概要": "",
"仕事内容": "",
"必須スキル": [],
"歓迎スキル": [],
"求める人物像": "",
"想定年収": ""
}}

--- ヒアリング内容 ---
{text}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
    return response.choices[0].message.content
