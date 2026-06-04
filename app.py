import time
import streamlit as st
from pdf_generator import create_pdf
from agents.researcher import research_agent

st.set_page_config(
    page_title="ResearchGPT",
    page_icon="🚀",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
    135deg,
    #0f172a,
    #111827,
    #312e81
    );
}

[data-testid="stMetric"]{
    background: rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
    backdrop-filter: blur(10px);
}

.stTextInput input{
    border-radius:20px;
    font-size:18px;
}

.stButton button{
    background:
    linear-gradient(
    90deg,
    #7c3aed,
    #ec4899
    );
    color:white;
    border:none;
    border-radius:20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# SIDEBAR
# =========================

st.sidebar.title("📜 Research History")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.session_state.latest_result = None
    st.rerun()

for index, item in enumerate(reversed(st.session_state.history)):

    if st.sidebar.button(
        item["query"],
        key=f"history_{index}"
    ):
        st.session_state.latest_result = item
        st.rerun()

# =========================
# HERO SECTION
# =========================

st.markdown("""
<h1 style='text-align:center;
font-size:65px;
font-weight:900;
background:linear-gradient(
90deg,
#7c3aed,
#ec4899
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
'>
ResearchGPT
</h1>

<p style='text-align:center;
font-size:20px;
color:#cbd5e1;'>
AI-Powered Research Platform
</p>
""",
unsafe_allow_html=True)

# =========================
# SEARCH BOX
# =========================

query = st.text_input(
    "",
    placeholder="Ask anything... (AI Trends, Nvidia Earnings, Microsoft News)"
)

# =========================
# RESEARCH BUTTON
# =========================

if st.button("🔍 Generate Research Report"):

    if query.strip() == "":
        st.warning("Please enter a topic.")

    else:

        start_time = time.time()

        with st.spinner("Researching..."):

            try:

                result = research_agent(query)

                elapsed_time = round(
                    time.time() - start_time,
                    2
                )

                result["query"] = query
                result["elapsed_time"] = elapsed_time

                st.session_state.latest_result = result

                st.session_state.history.append(result)

                st.session_state.history = (
                    st.session_state.history[-10:]
                )

                st.rerun()

            except Exception as e:

                st.error(f"Error: {e}")

# =========================
# DISPLAY RESULTS
# =========================

if st.session_state.latest_result:

    result = st.session_state.latest_result

    st.success("Research Complete!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Sources",
            len(result["sources"])
        )

    with col2:
        st.metric(
            "Model",
            "Gemini 2.5 Flash"
        )

    with col3:
        st.metric(
            "Time",
            f"{result.get('elapsed_time',0)}s"
        )

    st.divider()

    st.markdown(result["statistics"])

    st.divider()

    st.markdown(result["validation"])

    st.divider()

    st.markdown(result["report"])
    
    

    pdf_path = create_pdf(
    query=result.get("query", "Research Topic"),
    statistics=result["statistics"],
    validation=result["validation"],
    report=result["report"],
    sources=result["sources"]
)

    with open(
        pdf_path,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="AI_Research_Report.pdf",
            mime="application/pdf"
        )

    st.download_button(
        label="📥 Download Markdown Report",
        data=result["report"],
        file_name="research_report.md",
        mime="text/markdown"
    )

    st.divider()

    st.subheader("🔗 Sources")

    for source in result["sources"]:
        st.markdown(f"- {source}")