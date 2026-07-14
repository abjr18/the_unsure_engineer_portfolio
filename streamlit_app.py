"""
Portfolio app — local: `streamlit run streamlit_app.py`
Secrets (optional): copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
or set secrets in Streamlit Community Cloud. Access via `st.secrets` only in that file.
"""

import html
import random
import runpy
import subprocess
from pathlib import Path

import requests
import streamlit as st
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif")
ACCENT = "#FF7A18"
ACCENT_SOFT = "#FFB347"

DEFAULT_NAME = "Abhishek Padalkar"
DEFAULT_SIDEBAR_BRAND = "The Unsure Engineer"
DEFAULT_PITCH = (
    "To obtain a challenging AI Automation Engineer / RPA Developer position where I can "
    "leverage my expertise in Agentic AI, Robotic Process Automation (RPA), data engineering, "
    "problem-solving, communication, and requirement gathering to design intelligent automation "
    "solutions, streamline business processes, and support organizations in achieving their "
    "operational and strategic objectives."
)

DEFAULT_ABOUT = (
    "With over 4 years of experience designing, developing, and troubleshooting complex "
    "end-to-end automation workflows within the UiPath ecosystem. At Accelirate, specialized in "
    "business process mapping and delivering scalable, high-availability RPA solutions using "
    "Python, SQL, Power Automate, and UiPath technologies. Experienced in leading global "
    "automation deployments and collaborating with stakeholders to optimize enterprise workflows. "
    "Currently expanding expertise into Agentic AI-driven automation, focusing on building "
    "intelligent, adaptive, and self-correcting systems that go beyond traditional rule-based "
    "automation frameworks."
)

ACCENT = "#FF7A18"
ACCENT_SOFT = "#FFB347"

DEFAULT_LINKEDIN_URL = "https://www.linkedin.com/in/abhishek-padalkar-760b431b9"
DEFAULT_GITHUB_URL = "https://github.com/abjr18"

FUNNY_MESSAGES = [
    "Processing request...",
    "Thank you for your patience...",
    "My developer is broke, running on CPU not GPU...",
]


TOOLS: list[str] = [
    "UiPath",
    "LangGraph",
    "Python",
    "SQL",
    "AWS",
    "Databricks",
    "dbt",
    "LangSmith",
    "Vector DB",
    "RAG",
    "Graph RAG",
    "Docker",
]


SKILLS: list[str] = [
    "Root Cause Analysis",
    "RPA",
    "Automation",
    "Agentic AI",
    "Debugging",
    "Problem Solving",
    "Communication",
    "Prompt Engineering",
]


def _theme_css() -> str:
    return f"""
    <style>
      .stApp a {{
        color: {ACCENT} !important;
      }}
      .stApp a:hover {{
        color: {ACCENT_SOFT} !important;
      }}
      .stApp hr {{
        border-color: #2a2a2a !important;
      }}
      .stApp [data-testid="stHeader"] {{
        background: #050505;
      }}
      .stApp [data-testid="stMarkdownContainer"] th {{
        color: {ACCENT};
      }}
      .chip-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        justify-content: flex-start;
        margin: 0.25rem 0 0.5rem 0;
      }}
      .chip {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: #0b1a1a;
        border: 1px solid #0f766e;
        border-radius: 12px;
        padding: 10px 14px;
        min-width: 96px;
        max-width: 130px;
        box-sizing: border-box;
        transition: all 0.25s ease;
      }}
      .chip:hover {{
        background: #115e59;
        border-color: #2dd4bf;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
      }}
      .chip .icon-wrap {{
        height: 40px;
        width: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
      }}
      .chip img {{
        width: 36px;
        height: 36px;
        object-fit: contain;
      }}
      .logo-fallback {{
        width: 36px;
        height: 36px;
        border-radius: 8px;
        border: 1px dashed #3a3a3a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 700;
        color: {ACCENT};
        background: #1a1a1a;
        letter-spacing: 0.02em;
      }}
      .chip span {{
        font-size: 0.74rem;
        color: #cfcfcf;
        text-align: center;
        line-height: 1.25;
      }}
    </style>
    """


def _optional_secret(*keys: str, default: str | None = None) -> str | None:
    """Read nested keys from st.secrets without failing when secrets.toml is absent."""
    try:
        node: object = dict(st.secrets)
        for k in keys:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return str(node) if node is not None else default
    except FileNotFoundError:
        return default


def _get_last_updated_label() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=short"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
        )
        label = result.stdout.strip()
        if label:
            return label
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def _find_profile_photo() -> Path | None:
    """Prefer `assets/profile.jpg` or `assets/profile_picture.*`, then fall back to first image.

    Searches both `assets` and `Asset` directories for a set of preferred filenames
    (profile.jpg, profile_picture.*). If none are found, returns the first image
    file found in the folder.
    """
    preferred_names = [
        "profile.jpg",
        "profile.jpeg",
        "profile.png",
        "profile.webp",
        "profile_picture.jpg",
        "profile_picture.jpeg",
        "profile_picture.png",
        "profile_picture.webp",
    ]

    for folder_name in ("assets", "Asset"):
        for name in preferred_names:
            p = BASE_DIR / folder_name / name
            if p.is_file():
                return p

    for folder_name in ("assets", "Asset"):
        d = BASE_DIR / folder_name
        if not d.is_dir():
            continue
        images = sorted(
            (p for p in d.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS),
            key=lambda p: p.name.lower(),
        )
        if images:
            return images[0]
    return None


def _find_resume_pdf() -> Path | None:
    """Pick `assets/resume.pdf` if present, else first `.pdf` in `assets/` or `Asset/`."""
    for folder_name in ("assets", "Asset"):
        for fname in ("resume.pdf", "Abhishek_Padalkar_Resume_Apr_26.pdf"):
            p = BASE_DIR / folder_name / fname
            if p.is_file():
                return p
    for folder_name in ("assets", "Asset"):
        d = BASE_DIR / folder_name
        if not d.is_dir():
            continue
        pdfs = sorted(
            (p for p in d.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"),
            key=lambda p: p.name.lower(),
        )
        if pdfs:
            return pdfs[0]
    return None


def _logo_initials(label: str) -> str:
    words = [w for w in label.replace("/", " ").replace("&", " ").split() if w]
    if not words:
        return "?"
    if len(words) == 1:
        w = words[0]
        return (w[:2] if len(w) >= 2 else w + "?")[:2].upper()
    return (words[0][0] + words[-1][0]).upper()


def _logo_fallback_inner(label: str) -> str:
    initials = html.escape(_logo_initials(label))
    tip = html.escape(f"Logo for: {label}", quote=True)  # Updated tooltip text
    return f'<div class="logo-fallback" title="{tip}">{initials}</div>'


def _tools_chips_html() -> str:
    parts = ['<div class="chip-grid">']
    for label in TOOLS:
        parts.append(f'<div class="chip"><span>{html.escape(label)}</span></div>')
    parts.append("</div>")
    return "\n".join(parts)


def _skills_chips_html() -> str:
    parts = ['<div class="chip-grid">']
    for label in SKILLS:
        parts.append(f'<div class="chip"><span>{html.escape(label)}</span></div>')
    parts.append("</div>")
    return "\n".join(parts)

def redirect_to_create():
    st.session_state.my_works_action = "AnonBlog"
    
def page_portfolio() -> None:
    name = _optional_secret("app", "name", default=DEFAULT_NAME) or DEFAULT_NAME
    pitch = _optional_secret("app", "pitch", default=DEFAULT_PITCH) or DEFAULT_PITCH

    st.markdown(
        f"""
        <h1 style="
            font-size: 2.05rem;
            font-weight: 700;
            color: #EDEDED;
            margin: 0 0 0.75rem 0;
            line-height: 1.25;
            letter-spacing: -0.02em;
        ">{html.escape(name)}</h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <p style="
            font-size: 1.05rem;
            color: #c4c4c4;
            line-height: 1.65;
            margin: 0 0 1.5rem 0;
        ">{html.escape(pitch)}</p>
        """,
        unsafe_allow_html=True,
    )

    col_photo, col_intro = st.columns([1, 2], gap="large")

    with col_photo:
        st.subheader("Profile")
        profile_photo = _find_profile_photo()
        
        if profile_photo is not None:
            # Wrap the image in a container to isolate the style
            with st.container(key="profile_pic_container"):
                st.image(str(profile_photo), use_container_width=True)
                
                # Inject CSS targeting the image inside this container
                st.html("""
                    <style>
                        div[data-testid="stVScrollBlock"]Container:has(div[key="profile_pic_container"]) img {
                            border-radius: 50% !important;
                            aspect-ratio: 1 / 1 !important;
                            object-fit: cover !important;
                            border: 3px solid #0077B5; /* Optional: LinkedIn Blue Border */
                        }
                    </style>
                """)
        else:
            st.info(
                "Add a profile image to the **`assets`** or **`Asset`** folder "
                "(e.g. `assets/profile.jpg`)."
            )

    with col_intro:
        st.subheader("About")
        about = _optional_secret("app", "about", default=DEFAULT_ABOUT) or DEFAULT_ABOUT
        st.markdown(about)

    st.divider()

    st.subheader("Work")
    st.markdown(
        """
**Recent role:** Automation Engineer — Accelirate Softech

**Project:** RPA development and maintenance using UiPath ecosystem

**Domains:** Finance and Accounting; Sales & Lead Management

**Aug 2021 – Sep 2025**
        """
    )
    st.markdown("**Current Focus areas**")
    st.markdown(
        """
- Agentic AI
- Python
- RPA
- Automation
- Data Engineering
        """
    )

    st.divider()
    st.subheader("Tools")
    st.markdown(_tools_chips_html(), unsafe_allow_html=True)

    st.divider()
    st.subheader("Resume & profiles")
    linkedin = (
        _optional_secret("app", "linkedin_url", default=DEFAULT_LINKEDIN_URL)
        or DEFAULT_LINKEDIN_URL
    )
    github = (
        _optional_secret("app", "github_url", default=DEFAULT_GITHUB_URL)
        or DEFAULT_GITHUB_URL
    ).strip()

    c_resume, c_li, c_gh = st.columns(3, gap="medium")
    with c_resume:
        resume_pdf = _find_resume_pdf()
        if resume_pdf is not None:
            st.download_button(
                label="Download resume (PDF)",
                data=resume_pdf.read_bytes(),
                file_name=resume_pdf.name,
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.caption("Add a `.pdf` resume to the `assets` folder.")
    with c_li:
        st.link_button("LinkedIn", linkedin, use_container_width=True)
    with c_gh:
        if github:
            st.link_button("GitHub", github, use_container_width=True)
        else:
            st.markdown(
                '<p style="color:#888;font-size:0.9rem;margin:0.35rem 0 0 0;">'
                "<strong>GitHub</strong> — link coming soon.</p>",
                unsafe_allow_html=True,
            )

    st.caption(f"Last updated: {_get_last_updated_label()}")


def page_job_assistant() -> None:

    st.set_page_config(page_title="Abhishek Padalkar's - Job Agent", layout="centered")
    st.title("💼 The JOB AGENT")

    # Add this updated message below your title
    st.info(
    "**Phase 1 Completed!** 🎉 More features are on the way.\n\n"
    "👉 **Current Feature:** The bot scraps job listings, saves them as an Excel file, and hands it to you automatically so you don't have to.\n\n"
    "🚀 **Next Update:** Resume reading, resume evaluation, and AI-powered job matching based on your CV.\n\n"
    "💬 **Got Feedback?** I would love to hear your thoughts! Connect with me on [LinkedIn](https://www.linkedin.com/in/abhishek-padalkar-760b431b9) to share your suggestions."
    )
    # FASTAPI_URL = "http://localhost:8000/chat"
    FASTAPI_URL = "http://152.67.164.240:8000/chat"
    # Initialize conversation tracking
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Capture new user input
    if user_query := st.chat_input(
        "e.g., Can you look up Software Engineer jobs for me?"
    ):
        # Display user comment right away
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

            # Query the FastAPI backend
        with st.chat_message("assistant"):
            message_to_display = random.choice(FUNNY_MESSAGES)
            with st.spinner(message_to_display):
                try:
                    res = requests.post(FASTAPI_URL, json={"message": user_query})
                    # res = requests.post(FASTAPI_URL, user_query)
                    if res.status_code == 200:
                        api_response = res.json()
                        ai_text = api_response["text"]
                        if "downloadable_link" in api_response:
                            file_link = api_response["downloadable_link"]
                            st.markdown(ai_text)
                            st.markdown(file_link)
                        else:
                            st.markdown(ai_text)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": api_response}
                        )

                    else:
                        st.error(f"Backend Error: {res.text}")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to FastAPI server. Is it running on port 8000?"
                    )

def choose_random_link():
    links = ["https://www.wattpad.com/story/410813616-the-asylum-of-embers","https://www.inkitt.com/stories/1743526?preview=true","https://www.royalroad.com/fiction/168553/the-asylum-of-embers"]
    luckyLink = random.choice(links)
    return luckyLink

def main() -> None:
    st.set_page_config(
        page_title=f"{DEFAULT_NAME} — Portfolio",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_theme_css(), unsafe_allow_html=True)

    brand = (
        _optional_secret("app", "sidebar_brand", default=DEFAULT_SIDEBAR_BRAND)
        or DEFAULT_SIDEBAR_BRAND
    )

    st.sidebar.markdown(
        f"""
        <p style="
            font-size: 1.35rem;
            font-weight: 700;
            color: #EDEDED;
            margin: 0 0 1rem 0;
            line-height: 1.2;
        ">{html.escape(brand)}</p>
        """,
        unsafe_allow_html=True,
    )
    sidebar_image_path = BASE_DIR / "assets" / "the_unsure_engineer.png"
    if sidebar_image_path.is_file():
        st.sidebar.image(str(sidebar_image_path))
    st.sidebar.markdown(
        f'<p style="color:{ACCENT}; font-weight:700; margin-bottom:0.5rem;">My WoRkS</p>',
        unsafe_allow_html=True,
    )
    my_works_action = st.sidebar.selectbox(
        "My WoRkS",
        ["Home", "AnonBlog", "Projects"],
        index=0,
        key="my_works_action",
        label_visibility="collapsed",
        help="Choose the workflow you want to open from the portfolio app.",
    )

    # More about me (simple list, first item is a placeholder link to be updated later)
    st.sidebar.markdown(
        f'<p style="color:{ACCENT}; font-weight:700; margin-bottom:0.25rem; margin-top:1rem;">More about me</p>',
        unsafe_allow_html=True,
    )
    story_url = choose_random_link()

    # Pass the variable into the string using an f-string
    st.sidebar.markdown(
        f"- [Fictional Stories]({story_url})\n"
        "- Badminton\n"
        "- Swim\n"
        "- Travel\n"
        "- Have fun whenever possible",
        unsafe_allow_html=True,
    )

    if my_works_action == "AnonBlog":
        runpy.run_path(str(BASE_DIR / "AnonyBlog" / "create_post.py"), run_name="__main__")
    elif my_works_action == "Projects":
        page_portfolio()
    else:
        page_portfolio()


if __name__ == "__main__":
    main()
