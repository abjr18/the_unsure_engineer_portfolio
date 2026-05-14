"""
Portfolio app — local: `streamlit run streamlit_app.py`
Secrets (optional): copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
or set secrets in Streamlit Community Cloud. Access via `st.secrets` only in that file.
"""

import html
from pathlib import Path

import streamlit as st

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
DEFAULT_GITHUB_URL = ""

# CDN URLs for Tools
TOOLS_ICONS: list[tuple[str, str]] = [
    (
        "UiPath",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/uipath/uipath-original.svg",
    ),
    (
        "LangGraph",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/cog.svg",
    ),  # Generic cog icon
    (
        "Python",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    ),
    ("SQL", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sql/sql-plain.svg"),
    (
        "AWS",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original-wordmark.svg",
    ),
    (
        "Databricks",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/databricks/databricks-original.svg",
    ),
    ("dbt", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dbt/dbt-plain.svg"),
    (
        "LangSmith",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/wand-magic-sparkles.svg",
    ),  # Generic magic wand
    (
        "Vector DB",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/database.svg",
    ),  # Generic database
    (
        "RAG",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/book-open.svg",
    ),  # Generic book
    (
        "GRAG",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/book-open.svg",
    ),  # Assuming GRAG is similar to RAG, using same icon
    (
        "Docker",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
    ),
    (
        "Airflow",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apacheairflow/apacheairflow-original.svg",
    ),
    ("GIT", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg"),
]

# CDN URLs for Skills
SKILLS_ICONS: list[tuple[str, str]] = [
    (
        "Root Cause Analysis",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/magnifying-glass-chart.svg",
    ),
    (
        "RPA",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/robot.svg",
    ),
    (
        "Automation",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/gears.svg",
    ),
    (
        "Agentic AI",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/brain.svg",
    ),
    (
        "Debugging",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/bug.svg",
    ),
    (
        "Problem Solving",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/lightbulb.svg",
    ),
    (
        "Communication",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/comments.svg",
    ),
    (
        "Prompt Engineering",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/svgs/solid/pen-nib.svg",
    ),
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
        justify-content: flex-start;
        background: #121212;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 14px 12px;
        min-width: 96px;
        max-width: 130px;
        box-sizing: border-box;
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


def _find_profile_photo() -> Path | None:
    """Use `assets/profile.jpg` if present; otherwise first image in `assets/` or `Asset/`."""
    candidates = [
        BASE_DIR / "assets" / "profile.jpg",
        BASE_DIR / "Asset" / "profile.jpg",
    ]
    for p in candidates:
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


def _img_chip_inner(cdn_url: str, label: str) -> str:
    """Generates HTML for an image chip using a CDN URL."""
    tip = html.escape(f"Logo for: {label}", quote=True)  # Updated tooltip text
    return f'<img src="{cdn_url}" alt="{html.escape(label)}" title="{tip}" style="width: 36px; height: 36px; object-fit: contain;">'


def _tools_chips_html() -> str:
    parts = ['<div class="chip-grid">']
    for label, cdn_url in TOOLS_ICONS:  # Changed to use cdn_url directly
        inner = _img_chip_inner(cdn_url, label)
        parts.append(
            f'<div class="chip"><div class="icon-wrap">{inner}</div>'
            f"<span>{html.escape(label)}</span></div>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def _skills_chips_html() -> str:
    parts = ['<div class="chip-grid">']
    for label, cdn_url in SKILLS_ICONS:  # Changed to use cdn_url directly
        inner = _img_chip_inner(cdn_url, label)
        parts.append(
            f'<div class="chip"><div class="icon-wrap">{inner}</div>'
            f"<span>{html.escape(label)}</span></div>"
        )
    parts.append("</div>")
    return "\n".join(parts)


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
            st.image(str(profile_photo), use_container_width=True)
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
    st.markdown("**Focus areas**")
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
    st.subheader("Skills")
    st.markdown(_skills_chips_html(), unsafe_allow_html=True)

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
    st.sidebar.markdown(
        f'<p style="color:{ACCENT}; font-weight:700; margin-bottom:0.5rem;">Sections</p>',
        unsafe_allow_html=True,
    )
    _ = st.sidebar.selectbox(
        "Choose a section",
        ["My Projects", "My Hobbies"],
        label_visibility="collapsed",
        help="Reserved for future pages (no extra content on the main page yet).",
    )

    page_portfolio()


if __name__ == "__main__":
    main()
