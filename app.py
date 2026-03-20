"""
皮影戏AI - Web界面
"""

import streamlit as st
import sys
import os

sys.path.append(".")
from agent import ShadowPlayAgent
from config import OUTPUT_DIR


def init_page():
    st.set_page_config(page_title="皮影戏AI漫剧工具", page_icon="🎭", layout="wide")
    st.title("🎭 皮影戏AI漫剧工具")
    st.markdown("输入故事文字，生成皮影戏视频")


def main():
    init_page()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    story = st.text_area(
        "📖 请输入故事内容",
        placeholder="例如：从前有个叫阿强的年轻人，他每天在村口的大树下练习武艺...",
        height=150,
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button(
            "🎬 开始生成", type="primary", use_container_width=True
        )

    if generate_btn:
        if story:
            with st.spinner("正在生成..."):
                agent = ShadowPlayAgent()
                result = agent.run(story)

                st.success("生成完成！")

                st.subheader("📸 生成的图片")
                for img in result.get("images", []):
                    st.image(img["path"], caption=f"分镜 {img['scene']}")

                st.subheader("🎬 生成的视频")
                for video in result.get("videos", []):
                    st.video(video["path"])

        else:
            st.warning("请输入故事内容")

    with st.sidebar:
        st.header("使用说明")
        st.markdown("""
        1. 输入故事文字
        2. 点击「开始生成」
        3. 等待视频生成完成
        4. 下载结果
        """)

        st.header("当前状态")
        st.success("✅ 模块就绪")


if __name__ == "__main__":
    main()
