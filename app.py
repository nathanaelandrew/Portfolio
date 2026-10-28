import streamlit as st
import pandas as pd
import numpy as np
import os
import base64
import inspect

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Nathanael Mendoza | Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMAGE LOADERS (Base64) ---
def load_base64_image(candidates, default_fallback):
    for filename in candidates:
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as img_file:
                    encoded = base64.b64encode(img_file.read()).decode("utf-8")
                    ext = filename.split(".")[-1].lower()
                    mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
                    return f"data:image/{mime};base64,{encoded}"
            except Exception:
                pass
    return default_fallback

# 1. Sidebar Avatar Photo
avatar_src = load_base64_image(
    ["profile.jpg", "profile.png", "profile.jpeg", "avatar.jpg", "me.jpg"],
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80"
)

# 2. Autobiography Popup Photo (Drop 'bio.jpg' or 'autobiography.jpg' in folder)
bio_src = load_base64_image(
    ["bio.JPG", "bio.jpg", "bio.png", "autobiography.jpg", "autobiography.png", "modal.jpg"],
    avatar_src
)

# --- INITIALIZE SESSION STATE ---
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Overview & Bio"

# --- MODERN STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu, footer, header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ─── Profile Avatar (Exact Facebook Crop) ─── */
    .profile-card {
        text-align: center;
        padding: 4px 0 6px 0;
    }
    .profile-img-frame {
        width: 140px;
        height: 140px;
        margin: 0 auto 12px auto;
        border-radius: 50%;
        overflow: hidden;
        border: 2px solid #6366f1;
        box-shadow: 0 0 24px rgba(99, 102, 241, 0.35);
        background-color: #0b0f19;
    }
    .profile-img-frame img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        /* Matches Facebook profile circle crop precisely */
        transform: scale(1.42);
        transform-origin: 42% 67%;
        display: block;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.25);
        border-radius: 9999px;
        color: #4ade80;
        font-size: 0.74rem;
        font-weight: 600;
        margin-top: 6px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 8px #22c55e;
    }
    .github-link-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
        padding: 5px 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        color: #e2e8f0;
        text-decoration: none;
        font-size: 0.78rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .github-link-badge:hover {
        background: rgba(99, 102, 241, 0.2);
        border-color: #6366f1;
        color: #ffffff;
    }

    /* ─── Compact Navigation Buttons ─── */
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(button) {
        margin-bottom: -6px !important;
        margin-top: 0 !important;
    }
    [data-testid="stSidebar"] button {
        border-radius: 10px !important;
        font-size: 0.90rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 14px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: #f8fafc !important;
        transform: translateX(4px) !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.28) 0%, rgba(99, 102, 241, 0.1) 100%) !important;
        border: 1px solid #6366f1 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.25) !important;
        transform: translateX(2px);
    }

    /* ─── Metric Cards ─── */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        padding: 18px 20px !important;
        border-radius: 14px !important;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.45) !important;
    }
    div[data-testid="stMetricLabel"] p {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
    }
    div[data-testid="stMetricValue"] div {
        font-size: 1.65rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
        margin-top: 4px !important;
    }

    .page-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 2px;
    }
    .page-title svg {
        color: #6366f1;
        flex-shrink: 0;
    }
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f8fafc;
        border-left: 3px solid #6366f1;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    /* ─── Projects Cards ─── */
    .project-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        transition: all 0.25s ease;
    }
    .project-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 20px;
        margin-right: 6px;
        margin-bottom: 6px;
        background: rgba(99, 102, 241, 0.12);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.25);
    }
    .badge-role {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.12);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .project-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #93c5fd;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 8px;
        transition: color 0.2s ease;
    }
    .project-link-btn:hover {
        color: #ffffff;
        text-decoration: underline;
    }

    /* ─── EDITORIAL POPUP SPREAD (NO-CLIP SCROLL) ─── */
    div[data-testid="stDialog"] div[role="dialog"] {
        width: 88vw !important;
        max-width: 1140px !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        background: #000000 !important;
        padding: 0 !important;
        max-height: 88vh !important;
        box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.9) !important;
    }
    div[data-testid="stDialog"] div[role="dialog"] > div {
        padding: 0 !important;
    }
    div[data-testid="stDialog"] button[aria-label="Close"] {
        color: #ffffff !important;
        background: rgba(0, 0, 0, 0.5) !important;
        border-radius: 50% !important;
        z-index: 9999 !important;
        top: 16px !important;
        right: 16px !important;
        backdrop-filter: blur(8px) !important;
    }
    .editorial-popup-container {
        display: flex;
        flex-direction: row;
        width: 100%;
        height: 590px;
        background-color: #e7e4df;
        overflow: hidden;
    }
    .editorial-left-col {
        flex: 1.25;
        padding: 44px 46px;
        background-color: #e7e4df;
        color: #1a1a1a;
        display: flex;
        flex-direction: column;
        overflow-y: auto;
        height: 100%;
    }
    .editorial-left-col::-webkit-scrollbar {
        width: 5px;
    }
    .editorial-left-col::-webkit-scrollbar-track {
        background: transparent;
    }
    .editorial-left-col::-webkit-scrollbar-thumb {
        background: rgba(0, 0, 0, 0.18);
        border-radius: 10px;
    }
    .editorial-left-col::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 0, 0, 0.35);
    }
    .editorial-headline {
        font-family: 'Playfair Display', Didot, Georgia, serif;
        font-size: 2.85rem;
        font-weight: 600;
        letter-spacing: -0.025em;
        line-height: 1.05;
        color: #1a1a1a;
        margin-bottom: 20px;
    }
    .editorial-body-p {
        font-size: 0.95rem;
        line-height: 1.68;
        color: #383733;
        margin-bottom: 16px;
    }
    .editorial-right-col {
        flex: 1.05;
        height: 100%;
        position: relative;
        overflow: hidden;
        background-color: #18181b;
    }
    .editorial-right-col img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center 25%;
        filter: grayscale(100%) contrast(1.15) brightness(0.96);
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# --- EDITORIAL AUTOBIOGRAPHY DIALOG ---
@st.dialog(" ", width="large")
def show_autobiography_dialog():
    st.markdown(f"""
        <div class="editorial-popup-container">
            <div class="editorial-left-col">
                <div class="editorial-headline">Autobiography</div>
                <p class="editorial-body-p">
                    My name is <strong>Nathanael Andrew C. Mendoza</strong>, a Computer Science student at Cebu Institute of Technology–University. Originally from <strong>Bantayan Island, Cebu</strong>, I am someone who values faith, family, education, and personal growth.
                </p>
                <p class="editorial-body-p">
                    I completed my elementary education at Bantayan Christian School and attended <strong>Bantayan Science High School</strong>, where I consistently earned <em>With High Honors</em> from Grades 7 to 12. During my school years, I participated in various activities, including basketball, table tennis, school publication, radio broadcasting, and academic competitions. These experiences helped me develop discipline, creativity, teamwork, and communication skills.
                </p>
                <p class="editorial-body-p">
                    Currently, I am pursuing Computer Science, where I continue to develop my programming and problem-solving abilities. I aspire to become a skilled software developer who can create meaningful technological solutions and contribute positively to society.
                </p>
                <p class="editorial-body-p" style="margin-bottom: 28px;">
                    Outside academics, I enjoy playing the guitar, serving through music in church, running, and playing pickleball. My Christian faith remains an important part of my life, guiding my decisions and reminding me to trust God's plans. <strong>Romans 8:28</strong> serves as my life verse, encouraging me to remain faithful and hopeful through every season.
                </p>
            </div>
            <div class="editorial-right-col">
                <img src="{bio_src}" alt="Nathanael Andrew Mendoza">
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
        <div class="profile-card">
            <div class="profile-img-frame">
                <img src="{avatar_src}" alt="Nathanael Andrew Mendoza">
            </div>
            <h3 style="margin: 0; color: #ffffff; font-size: 1.15rem; font-weight: 700;">Nathanael Andrew Mendoza</h3>
            <p style="color: #94a3b8; font-size: 0.82rem; margin: 4px 0 0 0;">BS Computer Science • 3rd Year</p>
            <p style="color: #64748b; font-size: 0.78rem; margin: 2px 0 6px 0;">📍 Cebu City, Philippines</p>
            <div>
                <a href="https://github.com/nathanaelandrew" target="_blank" class="github-link-badge">
                    <svg height="14" width="14" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                    github.com/nathanaelandrew
                </a>
            </div>
            <div class="status-pill">
                <div class="status-dot"></div> Open to Work & Projects
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 14px 0 16px 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: #64748b; margin-bottom: 8px;'>Navigation</p>", unsafe_allow_html=True)

    nav_items = [
        ("Overview & Bio", "Overview & Bio", ":material/person:"),
        ("Skills & Metrics", "Skills & Metrics", ":material/analytics:"),
        ("Projects Portfolio", "Projects Portfolio", ":material/code:"),
        ("Contact & Feedback", "Contact & Feedback", ":material/mail:")
    ]

    supports_button_icons = "icon" in inspect.signature(st.button).parameters

    for label, target, icon_name in nav_items:
        is_active = (st.session_state.nav_page == target)
        btn_kwargs = {
            "key": f"nav_btn_{target}",
            "type": "primary" if is_active else "secondary",
            "use_container_width": True
        }
        if supports_button_icons:
            btn_kwargs["icon"] = icon_name

        if st.button(label, **btn_kwargs):
            if st.session_state.nav_page != target:
                st.session_state.nav_page = target
                st.rerun()

    st.markdown("<br><hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin-top: 24px;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #475569; font-size: 0.75rem; text-align: center; margin: 0;'>"
        "CIT-U • CSIT 365 Applied AI"
        "</p>",
        unsafe_allow_html=True
    )

# --- MAIN CONTENT ---

# 1. OVERVIEW & BIO
if st.session_state.nav_page == "Overview & Bio":
    st.markdown("""
        <div class="page-title">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>Nathanael Andrew C. Mendoza</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.15rem; color: #94a3b8; margin-bottom: 24px;'>Undergraduate Computer Science Student & Full-Stack Developer</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.65, 1.0], gap="large")
    
    with col1:
        st.markdown('<div class="section-header">About Me</div>', unsafe_allow_html=True)
        st.markdown("""
        Hello! I'm a third-year **Computer Science** undergraduate at **Cebu Institute of Technology – University (CIT-U)**. 
        
        Based in Cebu City, I bridge clean software architecture with high-contrast, editorial user interfaces inspired by film and zine design aesthetics. Whether I'm engineering full-stack healthcare platforms, mobile budget apps, or sports community tools, I prioritize **runtime performance**, **robust backend logic**, and **thoughtful UX**.
        """)
        
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Read Full Autobiography ↗", key="open_autobio_btn"):
            show_autobiography_dialog()
            
    with col2:
        st.markdown('<div class="section-header">Quick Stats</div>', unsafe_allow_html=True)
        st.metric(label="Academic Standing", value="3rd Year BSCS", delta="CIT-U")
        st.metric(label="Active DUPR Rating", value="2.442", delta="Pickleball")
        st.metric(label="Current Tech Focus", value="Django / Blazor", delta="Full-Stack")

    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 32px 0 20px 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Key Milestones</div>', unsafe_allow_html=True)
    
    tab_milestones, tab_hobbies = st.tabs(["Academic & Dev Milestones", "Creative & Personal"])
    
    with tab_milestones:
        st.markdown("""
        * **Oct 2026:** Completed ML Data Science Midterm Project analyzing Kaggle's Sleep Health Dataset using Random Forest & K-Means clustering.
        * **Oct 2026:** Presented a B2B/B2C agricultural produce sourcing solution for Cebu HoReCa establishments in Technopreneurship.
        * **Sep 2026:** Developed and deployed **MaterniLink** (Django) and **AceTime** (Blazor).
        * **May 2026:** Delivered a live architecture presentation for **SpendSass** (Kotlin / MVP) and launched **WildDocs** (PHP/MySQL).
        """)
        
    with tab_hobbies:
        st.markdown("""
        * **June 2026:** Explored street photography, urban transit systems, and Disneyland during a trip to Hong Kong.
        * **Feb 2026:** Verified official DUPR pickleball rating and joined the local amateur sports circuit.
        * **Ongoing:** Color grading Apple Log mobile footage in DaVinci Resolve with film grain simulation and custom LUTs.
        """)

# 2. SKILLS & METRICS
elif st.session_state.nav_page == "Skills & Metrics":
    st.markdown("""
        <div class="page-title">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <span>Technical Proficiency & Analytics</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; margin-bottom: 24px;'>A data-backed breakdown of programming languages, frameworks, and competency levels.</p>", unsafe_allow_html=True)
    
    skills_data = {
        "Technology / Tool": ["Python / Django", "C# / Blazor / .NET", "Kotlin (Android MVP)", "PHP / MySQL", "Java / C++", "Git & Conventional Commits", "DaVinci Resolve / UI Design"],
        "Category": ["Backend / Web", "Full-Stack / Desktop", "Mobile", "Web / Database", "Systems / Core", "Version Control", "Multimedia & Design"],
        "Proficiency (%)": [90, 85, 85, 80, 85, 90, 88],
        "Years Experience": [2.0, 2.0, 1.5, 2.0, 3.0, 3.0, 2.0]
    }
    df_skills = pd.DataFrame(skills_data)
    
    col_table, col_chart = st.columns([1.1, 1], gap="large")
    
    with col_table:
        st.markdown('<div class="section-header">Proficiency Matrix</div>', unsafe_allow_html=True)
        min_prof = st.slider("Filter by minimum proficiency (%):", 50, 95, 80)
        filtered_df = df_skills[df_skills["Proficiency (%)"] >= min_prof]
        
        st.dataframe(
            filtered_df,
            column_config={
                "Proficiency (%)": st.column_config.ProgressColumn(
                    "Proficiency",
                    help="Self-assessed confidence level",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )
        
    with col_chart:
        st.markdown('<div class="section-header">Proficiency Chart</div>', unsafe_allow_html=True)
        st.bar_chart(
            data=filtered_df.set_index("Technology / Tool")["Proficiency (%)"],
            color="#6366f1",
            use_container_width=True
        )

# 3. PROJECTS PORTFOLIO
elif st.session_state.nav_page == "Projects Portfolio":
    st.markdown("""
        <div class="page-title">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
            <span>Featured Projects</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; margin-bottom: 24px;'>Explore full-stack web platforms, mobile architectures, and collegiate software systems.</p>", unsafe_allow_html=True)
    
    projects = [
        {
            "title": "BrainRush",
            "category": "Interactive & Game Logic",
            "role": "Lead Developer",
            "tools": ["Python / Pygame", "Game Architecture", "Data Structures", "Audio Integration"],
            "desc": "A fast-paced cognitive quiz and memory challenge application featuring timed rounds, dynamic scoring mechanics, and adaptive question banks designed to test reflexes, memory, and analytical reasoning under pressure.",
            "link": "https://github.com/nathanaelandrew/BrainRush"
        },
        {
            "title": "LIGTAS-Brgy",
            "category": "Community & Incident Management",
            "role": "Full-Stack Developer (2nd Year 2nd Sem Project)",
            "tools": ["PHP", "MySQL", "JavaScript", "Bootstrap", "Dispatch Logic"],
            "desc": "A community-focused disaster preparedness and emergency response portal developed for local barangays to streamline emergency incident dispatch, resident safety verification, disaster advisory dissemination, and relief tracking.",
            "link": "https://github.com/nathanaelandrew"
        },
        {
            "title": "MaterniLink",
            "category": "Python / Django",
            "role": "Full-Stack Developer",
            "tools": ["Python", "Django", "PostgreSQL", "HTML5/CSS3"],
            "desc": "A digital pregnancy companion for obstetricians and mothers to manage health records, prenatal appointments, maternal vitals logs, and clinical notes.",
            "link": "https://github.com/nathanaelandrew/MaterniLink"
        },
        {
            "title": "AceTime",
            "category": "C# / Blazor",
            "role": "Lead Architect",
            "tools": ["C#", "Blazor Web App", ".NET 8", "Entity Framework"],
            "desc": "An athletic community hub built to organize pickleball and racket sports clubs, schedule open play sessions, track DUPR ratings, and manage tournament brackets.",
            "link": "https://github.com/nathanaelandrew/AceTime"
        },
        {
            "title": "SpendSass",
            "category": "Kotlin / Android",
            "role": "Android Developer",
            "tools": ["Kotlin", "Android Studio", "MVP Architecture", "SharedPreferences"],
            "desc": "A native Android budget-tracking mobile application featuring clean Model-View-Presenter design, local persistence, and an interactive motivational mascot UI.",
            "link": "https://github.com/nathanaelandrew"
        },
        {
            "title": "WildDocs",
            "category": "PHP / MySQL",
            "role": "Backend Engineer",
            "tools": ["PHP", "MySQL", "XAMPP", "Bootstrap 5"],
            "desc": "An automated document request portal featuring role-based authentication, student ticket tracking, and an administrative approval queue.",
            "link": "https://github.com/nathanaelandrew"
        }
    ]
    
    for p in projects:
        badges_html = "".join([f'<span class="badge">{tool}</span>' for tool in p["tools"]])
        st.markdown(f"""
        <div class="project-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <div>
                    <span style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">{p['title']}</span>
                    <span style="color: #64748b; margin-left: 8px; font-size: 0.9rem;">• {p['category']}</span>
                </div>
                <span class="badge-role">{p['role']}</span>
            </div>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 12px;">
                {p['desc']}
            </p>
            <div style="margin-bottom: 10px;">{badges_html}</div>
            <div>
                <a href="{p['link']}" target="_blank" class="project-link-btn">
                    View on GitHub ↗
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. CONTACT & FEEDBACK
elif st.session_state.nav_page == "Contact & Feedback":
    st.markdown("""
        <div class="page-title">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            <span>Get in Touch</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; margin-bottom: 24px;'>Have a project inquiry, collaboration proposal, or just want to discuss tech & coffee?</p>", unsafe_allow_html=True)
    
    with st.container():
        with st.form("contact_form", clear_on_submit=True):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                sender_name = st.text_input("Your Name", placeholder="e.g. Alex Rivera")
            with col_f2:
                sender_email = st.text_input("Your Email", placeholder="alex@domain.com")
                
            subject_topic = st.selectbox(
                "Inquiry Type", 
                ["Full-Stack Collaboration", "Freelance Software Project", "Academic Research / AI", "General Greeting"]
            )
            
            message_body = st.text_area("Message", placeholder="Share details about your project or inquiry...", height=140)
            
            subscribe_newsletter = st.checkbox("Subscribe to quarterly updates on my projects, camera tests, and dev journals")
            
            submitted = st.form_submit_button("Send Message", use_container_width=True)
            
            if submitted:
                if sender_name.strip() and message_body.strip():
                    st.success(f"Thank you, **{sender_name}**! Your message regarding *{subject_topic}* was recorded. I'll follow up shortly!")
                    st.balloons()
                else:
                    st.error("Please provide both your name and message before submitting.")

# --- FOOTER ---
st.markdown("<br><hr style='border: 0; border-top: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>"
    "© 2026 Nathanael Andrew C. Mendoza • <b>CSIT 365 Applied AI</b> • Cebu Institute of Technology – University"
    "</p>",
    unsafe_allow_html=True
)
