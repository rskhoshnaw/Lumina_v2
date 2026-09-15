import os
from pathlib import Path

import streamlit as st

from core.gemini_provider import GeminiProvider
from core.content_planner import ContentPlanner
from core.code_generator import CodeGenerator
from core.validator import validate_code
from core.renderer import ManimRenderer


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

GENERATED_DIR = BASE_DIR / "generated"
MEDIA_DIR = BASE_DIR / "media"
PROJECTS_DIR = BASE_DIR / "projects"
PROMPTS_DIR = BASE_DIR / "prompts"

GENERATED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MEDIA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PROJECTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Lumina Studio 2.0",
    page_icon="✨",
    layout="wide",
)


# =========================================================
# HEADER
# =========================================================

st.title("✨ Lumina Studio 2.0")

st.caption("AI Educational & Motivational Animation Studio")


# =========================================================
# GEMINI
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY تنظیم نشده است.")
    st.stop()


try:
    provider = GeminiProvider(api_key=GEMINI_API_KEY)

except Exception as err:
    st.error(f"❌ خطا در اتصال به Gemini:\n{err}")
    st.stop()


# =========================================================
# ENGINES
# =========================================================

planner = ContentPlanner(
    provider=provider,
    prompt_file=(PROMPTS_DIR / "planner.txt"),
)

code_generator = CodeGenerator(
    provider=provider,
    prompt_file=(PROMPTS_DIR / "code_generator.txt"),
)

renderer = ManimRenderer(
    base_dir=BASE_DIR,
    media_dir=MEDIA_DIR,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header("🎛️ تنظیمات ویدئو")

    category = st.selectbox(
        "📚 نوع محتوا",
        [
            "mathematics",
            "science",
            "physics",
            "chemistry",
            "biology",
            "history",
            "geography",
            "literature",
            "language",
            "motivation",
            "personal_development",
            "storytelling",
            "educational",
            "children",
            "general",
        ],
        format_func=lambda x: {
            "mathematics": "📐 ریاضیات",
            "science": "🔬 علوم",
            "physics": "⚛️ فیزیک",
            "chemistry": "🧪 شیمی",
            "biology": "🧬 زیست‌شناسی",
            "history": "🏛️ تاریخ",
            "geography": "🌍 جغرافیا",
            "literature": "📖 ادبیات",
            "language": "🔤 زبان",
            "motivation": "🔥 انگیزشی",
            "personal_development": "🎯 توسعه فردی",
            "storytelling": "📚 داستانی",
            "educational": "🎓 آموزشی",
            "children": "🧒 کودکان",
            "general": "✨ عمومی",
        }.get(x, x),
    )

    language = st.selectbox(
        "🌍 زبان",
        ["fa", "ckb", "ar", "en"],
        format_func=lambda x: {
            "fa": "🇮🇷 فارسی",
            "ckb": "☀️ کوردی سورانی",
            "ar": "🇸🇦 العربية",
            "en": "🇬🇧 English",
        }[x],
    )

    audience = st.selectbox(
        "👥 مخاطب",
        [
            "children",
            "teenagers",
            "students",
            "university",
            "general",
            "teachers",
        ],
        format_func=lambda x: {
            "children": "🧒 کودکان",
            "teenagers": "👦 نوجوانان",
            "students": "🎓 دانش‌آموزان",
            "university": "🏫 دانشجویان",
            "general": "👥 عموم",
            "teachers": "👨‍🏫 معلمان",
        }[x],
    )

    style = st.selectbox(
        "🎨 سبک",
        [
            "educational",
            "mathematical",
            "whiteboard",
            "infographic",
            "cinematic",
            "cartoon",
            "storytelling",
            "motivational",
            "minimal",
            "hybrid",
        ],
        format_func=lambda x: {
            "educational": "🎓 آموزشی",
            "mathematical": "📐 ریاضی",
            "whiteboard": "📝 Whiteboard",
            "infographic": "📊 Infographic",
            "cinematic": "🎬 Cinematic",
            "cartoon": "🎨 Cartoon",
            "storytelling": "📖 Storytelling",
            "motivational": "🔥 Motivational",
            "minimal": "⚪ Minimal",
            "hybrid": "✨ ترکیبی",
        }[x],
    )

    duration = st.selectbox(
        "⏱ مدت ویدئو",
        [
            30,
            60,
            90,
            120,
            180,
            300,
        ],
        format_func=lambda x: f"{x} ثانیه",
    )

    quality = st.selectbox(
        "🎞 کیفیت",
        [
            "-ql",
            "-qm",
            "-qh",
        ],
        format_func=lambda x: {
            "-ql": "480p — سریع",
            "-qm": "720p — متوسط",
            "-qh": "1080p — باکیفیت",
        }[x],
    )


# =========================================================
# INPUT
# =========================================================

st.subheader("📝 موضوع یا سناریو")

user_prompt = st.text_area(
    "موضوع ویدئو را بنویسید:",
    height=180,
    placeholder=(
        "مثلاً:\nقانون دوم نیوتن را برای یک دانش‌آموز ۱۴ ساله به زبان ساده توضیح بده."
    ),
)


# =========================================================
# GENERATE BUTTON
# =========================================================

generate_button = st.button(
    "🚀 ساخت ویدئو",
    type="primary",
    use_container_width=True,
)


if generate_button:
    if not user_prompt.strip():
        st.warning("⚠️ ابتدا موضوع ویدئو را وارد کنید.")
        st.stop()

    # =====================================================
    # SETTINGS
    # =====================================================

    settings = {
        "category": category,
        "language": language,
        "audience": audience,
        "style": style,
        "duration_seconds": duration,
        "quality": quality,
    }

    # =====================================================
    # STEP 1
    # =====================================================

    st.subheader("🧠 مرحله ۱ — طراحی محتوای ویدئو")

    with st.spinner("Gemini در حال طراحی Blueprint است..."):
        try:
            blueprint = planner.create_blueprint(
                user_request=user_prompt,
                settings=settings,
            )

        except Exception as err:
            st.error(f"❌ خطا در طراحی Blueprint:\n{err}")
            st.stop()

    st.success("✅ Blueprint با موفقیت ایجاد شد.")

    # =====================================================
    # SHOW BLUEPRINT
    # =====================================================

    with st.expander(
        "🧠 مشاهده Blueprint",
        expanded=False,
    ):
        st.json(blueprint)

    # =====================================================
    # STEP 2
    # =====================================================

    st.subheader("🐍 مرحله ۲ — تولید کد Manim")

    with st.spinner("در حال تبدیل Blueprint به انیمیشن Manim..."):
        try:
            code = code_generator.generate(blueprint)

        except Exception as err:
            st.error(f"❌ خطا در تولید کد:\n{err}")
            st.stop()

    # =====================================================
    # VALIDATION
    # =====================================================

    valid, validation_errors = validate_code(code)

    if not valid:
        st.error("❌ کد تولیدشده معتبر نیست.")

        for error in validation_errors:
            st.warning(error)

        with st.expander("🐍 کد تولیدشده"):
            st.code(
                code,
                language="python",
            )

        st.stop()

    st.success("✅ کد Python با موفقیت اعتبارسنجی شد.")

    # =====================================================
    # SAVE CODE
    # =====================================================

    code_file = GENERATED_DIR / "auto_scene.py"

    code_file.write_text(
        code,
        encoding="utf-8",
    )

    with st.expander("🐍 مشاهده کد Manim"):
        st.code(
            code,
            language="python",
        )

    # =====================================================
    # STEP 3
    # =====================================================

    st.subheader("🎬 مرحله ۳ — رندر ویدئو")

    with st.spinner("Manim در حال رندر ویدئو است..."):
        result = renderer.render(
            python_file=code_file,
            quality_flag=quality,
        )

    # =====================================================
    # RENDER ERROR
    # =====================================================

    if result.returncode != 0:
        st.error("❌ رندر Manim ناموفق بود.")

        if result.stderr:
            st.subheader("🔴 خطای Manim")

            st.code(
                result.stderr,
                language="text",
            )

        if result.stdout:
            with st.expander("📋 خروجی کامل Manim"):
                st.code(
                    result.stdout,
                    language="text",
                )

        st.stop()

    # =====================================================
    # FIND VIDEO
    # =====================================================

    target_video = renderer.find_video(scene_file_stem=code_file.stem)

    if not target_video:
        st.error("❌ رندر انجام شد ولی فایل MP4 پیدا نشد.")

        st.code(
            result.stdout,
            language="text",
        )

        st.stop()

    # =====================================================
    # SUCCESS
    # =====================================================

    st.success("🎉 ویدئو با موفقیت ساخته شد!")

    st.video(str(target_video))

    # =====================================================
    # DOWNLOAD
    # =====================================================

    video_data = target_video.read_bytes()

    st.download_button(
        "⬇️ دانلود ویدئو MP4",
        data=video_data,
        file_name="lumina_video.mp4",
        mime="video/mp4",
        use_container_width=True,
    )

    # =====================================================
    # MODEL INFO
    # =====================================================

    if provider.last_model:
        st.caption(f"🤖 مدل استفاده‌شده: {provider.last_model}")
