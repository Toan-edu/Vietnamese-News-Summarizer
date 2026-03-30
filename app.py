import streamlit as st
from utils import summarize_text
import time

st.set_page_config(
    page_title="Viet News Summarizer",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Vietnamese News Article Summarizer")
st.markdown("Tóm tắt bài báo tiếng Việt tự động bằng mô hình **ViT5**")

# Sidebar
st.sidebar.header("Cài đặt tóm tắt")
max_len = st.sidebar.slider("Độ dài tối đa (số từ)", 50, 300, 150)
min_len = st.sidebar.slider("Độ dài tối thiểu (số từ)", 30, 100, 50)

# Main content
tab1, tab2 = st.tabs(["📝 Dán văn bản", "📁 Upload file .txt"])

with tab1:
    article = st.text_area(
        "Dán nội dung bài báo vào đây:", 
        height=400,
        placeholder="Paste toàn bộ bài báo tiếng Việt ở đây..."
    )
    
    if st.button("🚀 Tóm tắt ngay", type="primary"):
        if len(article.strip()) < 100:
            st.error("Bài báo quá ngắn! Vui lòng dán ít nhất 100 ký tự.")
        else:
            with st.spinner("Đang tóm tắt bằng ViT5... (lần đầu tải model có thể mất 10-30 giây)"):
                start = time.time()
                summary = summarize_text(article, max_length=max_len, min_length=min_len)
                duration = time.time() - start
            
            st.success(f"✅ Hoàn thành trong {duration:.1f} giây")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader("📄 Bài gốc")
                st.caption(f"{len(article):,} ký tự")
                st.text_area("", article[:1500] + ("..." if len(article) > 1500 else ""), height=300, disabled=True)
            
            with col2:
                st.subheader("📝 Bản tóm tắt")
                st.caption(f"{len(summary):,} ký tự")
                st.text_area("", summary, height=300)
                
                st.download_button(
                    label="📥 Tải bản tóm tắt",
                    data=summary,
                    file_name="tom_tat_bai_bao.txt",
                    mime="text/plain"
                )

with tab2:
    uploaded = st.file_uploader("Chọn file bài báo (.txt)", type="txt")
    if uploaded:
        article = uploaded.read().decode("utf-8")
        st.info(f"Đã tải file: {uploaded.name} — {len(article):,} ký tự")
        
        if st.button("🚀 Tóm tắt từ file", type="primary"):
            with st.spinner("Đang tóm tắt..."):
                summary = summarize_text(article, max_length=max_len, min_length=min_len)
            st.text_area("Kết quả tóm tắt:", summary, height=250)

st.caption("Project NLP cho CV thực tập | Model: VietAI/vit5-base-vietnews-summarization")
