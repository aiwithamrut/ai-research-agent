import time
import streamlit as st
from pdf_generator import create_pdf
from agents.researcher import research_agent

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Research Assistant")

st.markdown("""
Ask anything and the AI will:

- Search the web
- Analyze information
- Generate a research summary
""")

query = st.text_input(
    "Enter research topic:",
    placeholder="Example: Latest AI trends in 2026"
)

if st.button("🔍 Research"):

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
                        f"{elapsed_time}s"
                    )

                st.subheader("📊 Key Statistics")
                st.markdown(result["statistics"])

                st.subheader("✅ Validation Report")
                st.markdown(result["validation"])

                st.subheader("📄 Research Report")
                st.markdown(result["report"])

                pdf_path = create_pdf(
                 result["report"]
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
                    label="📥 Download Report",
                    data=result["report"],
                    file_name="research_report.md",
                    mime="text/markdown"
                )

                st.subheader("🔗 Sources")

                for source in result["sources"]:
                    st.markdown(f"- {source}")

            except Exception as e:

                st.error(f"Error: {e}")