import os
import streamlit as st
from core.pipeline import LuminaPipeline

# تنظیمات پایه صفحه
st.set_page_config(page_title="Lumina Studio 2.0", layout="wide")

st.title("Lumina Studio 2.0 🎬")
st.markdown("پلتفرم AI-powered برای تولید ویدئوی آموزشی، انگیزشی و داستانی")

# منوی کناری برای تنظیمات
with st.sidebar:
    st.header("تنظیمات (Settings)")
    api_key_input = st.text_input("Gemini API Key (Optional if set in ENV)", type="password")
    
    category = st.selectbox("Category", [
        "mathematics", "science", "physics", "chemistry", "biology", 
        "history", "geography", "literature", "language", "motivation", 
        "personal_development", "storytelling", "educational", "children", "general"
    ])
    
    language = st.selectbox("Language", ["fa", "ckb", "ar", "en"])
    audience = st.selectbox("Audience", ["children", "teenagers", "adults", "general"])
    style = st.selectbox("Style", [
        "educational", "mathematical", "whiteboard", "infographic", 
        "cinematic", "cartoon", "storytelling", "motivational", "minimal", "hybrid"
    ])
    
    duration = st.slider("Duration (seconds)", min_value=15, max_value=120, value=60, step=15)
    quality = st.selectbox("Quality", ["ql (480p)", "qm (720p)", "qh (1080p)"], index=1)
    quality_code = quality.split(" ")[0]  # استخراج ql, qm یا qh

prompt = st.text_area(
    "سناریو یا موضوع خود را طبیعی وارد کنید:", 
    height=150, 
    placeholder="مثلاً: قانون دوم نیوتن را برای یک دانش‌آموز ۱۴ ساله به زبان ساده توضیح بده."
)

if st.button("تولید ویدئو (Generate Video)", type="primary"):
    if not prompt:
        st.warning("لطفاً یک موضوع یا سناریو وارد کنید.")
    else:
        try:
            with st.spinner("در حال پردازش مراحل: Content Planner -> Code Generator -> Validator -> Renderer..."):
                final_api_key = api_key_input if api_key_input else os.getenv("GEMINI_API_KEY")
                
                if not final_api_key:
                    st.error("خطا: GEMINI_API_KEY تنظیم نشده است.")
                    st.stop()

                # فراخوانی Pipeline یکپارچه
                pipeline = LuminaPipeline(api_key=final_api_key)
                
                result = pipeline.run(
                    prompt=prompt,
                    category=category,
                    language=language,
                    audience=audience,
                    style=style,
                    duration_seconds=duration,
                    quality=quality_code,
                    output_dir="generated"
                )
                
                st.success("ویدئو با موفقیت ساخته شد!")
                
                # نمایش ویدئو و دکمه دانلود
                video_file = result["video_file"]
                if os.path.exists(video_file):
                    with open(video_file, "rb") as v_file:
                        video_bytes = v_file.read()
                        
                    st.video(video_bytes)
                    
                    st.download_button(
                        label="دانلود MP4",
                        data=video_bytes,
                        file_name="lumina_generated_video.mp4",
                        mime="video/mp4"
                    )
                else:
                    st.error("فایل ویدئو پیدا نشد.")
                    
        except Exception as e:
            st.error(f"خطا در تولید ویدئو:\n{str(e)}")
