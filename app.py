import streamlit as st
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

        with st.spinner("Researching..."):

            try:
                result = research_agent(query)

                st.success("Research Complete!")

                st.subheader("📄 Research Report")

                st.write(result)

            except Exception as e:

                st.error(f"Error: {e}")