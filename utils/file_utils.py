import json
import os
import streamlit as st

DATA_DIR = "data"

def save_json(json_text):
    """JSON形式で保存"""
    os.makedirs(DATA_DIR, exist_ok=True)
    save_path = os.path.join(DATA_DIR, "job_data.json")
    with open(save_path, "w") as f:
        f.write(json_text)
    st.success(f"✅ JSON保存完了: {save_path}")


def save_markdown(md_text):
    """Markdown形式で保存"""
    os.makedirs(DATA_DIR, exist_ok=True)
    save_path = os.path.join(DATA_DIR, "job_description.md")
    with open(save_path, "w") as f:
        f.write(md_text)
    st.success(f"✅ Markdown保存完了: {save_path}")
