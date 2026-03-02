import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from src.analyzer import analyze_query
from src.balancer import get_balanced_recommendations, init_db

st.set_page_config(page_title="SHL Recommender", page_icon="📝", layout="centered")

st.title("🎯 SHL Assessment Recommender")
st.markdown("Enter a natural language query or job description to map relevant **Individual Test Solutions**.")

query = st.text_area("Job Description or Query", height=150, placeholder="e.g. Looking for a Python Developer who is an excellent communicator...")
k = st.slider("Number of Recommendations", min_value=5, max_value=10, value=5)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query or job description.")
    else:
        with st.spinner(f"Analyzing intent and matching top {k} SHL tests..."):
            try:
                # Initialize DB natively dynamically
                init_db()
                recs = get_balanced_recommendations(query, k=k)
                
                # Show detected intent
                intent_obj = analyze_query(query)
                st.info(f"**Extracted Intent:** Needs Hard Skills: `{intent_obj.requires_hard_skills}` | Needs Soft Skills: `{intent_obj.requires_soft_skills}`")
                
                if recs:
                    st.success(f"Found {len(recs)} relevant test solutions!")
                    
                    df = pd.DataFrame(recs)
                    if not df.empty and "title" in df.columns and "url" in df.columns:
                        df = df.rename(columns={"title": "Assessment Name", "url": "URL"})
                        st.dataframe(
                            df,
                            column_config={"URL": st.column_config.LinkColumn("SHL Link")},
                            hide_index=True,
                            use_container_width=True
                        )
                    else:
                        st.dataframe(df)
                else:
                    st.warning("No relevant matching assessments found.")
                    
            except Exception as e:
                st.error(f"Error executing recommendation engine natively: {e}")
