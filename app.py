import streamlit as st
import pandas as pd
from pathlib import Path
from src.search import search_similar, index_dataframe

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Bug Duplicate Detector",
    page_icon="🐞",
    layout="wide"
)

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parent
FEEDBACK_FILE = ROOT / "data" / "reviewer_feedback.csv"

# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = []

# ---------------------------------------------------------
# Feedback functions
# ---------------------------------------------------------

def load_feedback():
    if FEEDBACK_FILE.exists():
        return pd.read_csv(FEEDBACK_FILE)

    return pd.DataFrame(
        columns=["bug_id", "decision"]
    )


def save_feedback(bug_id, decision):

    feedback_df = load_feedback()

    # Remove previous decision for this bug
    feedback_df = feedback_df[
        feedback_df["bug_id"] != bug_id
    ]

    # Add latest decision
    new_row = pd.DataFrame(
        [{
            "bug_id": bug_id,
            "decision": decision
        }]
    )

    feedback_df = pd.concat(
        [feedback_df, new_row],
        ignore_index=True
    )

    FEEDBACK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    feedback_df.to_csv(
        FEEDBACK_FILE,
        index=False
    )


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🐞 AI Semantic Bug Duplicate Detector")

st.caption(
    "Semantic search + vector database for QA defect duplicate detection."
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Search settings")

    top_k = st.slider(
        "Results",
        3,
        10,
        5
    )

    threshold = st.slider(
        "Potential duplicate threshold",
        0.50,
        0.95,
        0.75,
        0.01
    )

    st.divider()

    st.header("Defect repository")

    uploaded = st.file_uploader(
        "Upload Jira-style CSV",
        type=["csv"]
    )

    if uploaded is not None:

        if st.button("Index Uploaded Defects"):

            try:

                df = pd.read_csv(uploaded)

                count = index_dataframe(df)

                st.success(
                    f"Indexed {count} defects."
                )

            except Exception as e:

                st.error(
                    f"Indexing failed: {e}"
                )

# ---------------------------------------------------------
# New defect
# ---------------------------------------------------------

title = st.text_input(
    "New defect title",
    placeholder="UPI transfer fails for high value transactions"
)

description = st.text_area(
    "New defect description",
    height=150,
    placeholder="Describe the observed behavior, expected behavior, module, and conditions."
)

# ---------------------------------------------------------
# Search button
# ---------------------------------------------------------

if st.button(
    "Find Similar Defects",
    type="primary"
):

    if not (title.strip() or description.strip()):

        st.warning(
            "Enter a title or description."
        )

    else:

        try:

            st.session_state.results = search_similar(
                title,
                description,
                top_k
            )

        except Exception as e:

            st.error(
                f"Search failed: {e}"
            )

# ---------------------------------------------------------
# Display search results
# ---------------------------------------------------------

if st.session_state.results:

    st.subheader(
        "Potentially related historical defects"
    )

    feedback_df = load_feedback()

    for x in st.session_state.results:

        similarity = x["similarity"]

        if similarity >= threshold:

            label = "🔴 Potential duplicate"

        elif similarity >= threshold - 0.10:

            label = "🟡 Possibly related"

        else:

            label = "🟢 Low similarity"

        with st.container(border=True):

            c1, c2 = st.columns([4, 1])

            # ---------------------------------------------
            # Defect details
            # ---------------------------------------------

            with c1:

                st.subheader(
                    f'{x["bug_id"]} — {x["title"]}'
                )

                st.write(
                    x["description"]
                )

                st.caption(
                    f'Module: {x["module"]} | '
                    f'Severity: {x["severity"]} | '
                    f'Status: {x["status"]}'
                )

            # ---------------------------------------------
            # Similarity
            # ---------------------------------------------

            with c2:

                st.metric(
                    "Similarity",
                    f"{similarity:.1%}"
                )

                st.write(label)

                # Check previous decision
                previous = feedback_df[
                    feedback_df["bug_id"] == x["bug_id"]
                ]

                if not previous.empty:

                    current_decision = previous.iloc[0]["decision"]

                else:

                    current_decision = "No decision"

                decision = st.radio(
                    "Reviewer decision",
                    [
                        "No decision",
                        "Confirm duplicate",
                        "Not duplicate",
                        "Related"
                    ],
                    index=[
                        "No decision",
                        "Confirm duplicate",
                        "Not duplicate",
                        "Related"
                    ].index(current_decision),
                    key=f"review_{x['bug_id']}",
                    label_visibility="collapsed"
                )

                # Save feedback
                if decision != current_decision:

                    save_feedback(
                        x["bug_id"],
                        decision
                    )

                    st.success(
                        "Feedback recorded"
                    )

# ---------------------------------------------------------
# Reviewer feedback history
# ---------------------------------------------------------

feedback_df = load_feedback()

if not feedback_df.empty:

    st.divider()

    st.subheader(
        "📝 Reviewer feedback captured"
    )

    st.dataframe(
        feedback_df,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# How it works
# ---------------------------------------------------------

with st.expander("How it works"):

    st.write(
        """
        1. Defect title and description are converted into embeddings.

        2. ChromaDB performs semantic similarity search against
           historical defects.

        3. The system returns the most similar historical defects.

        4. Similarity threshold identifies potential duplicates.

        5. A QA reviewer makes the final decision:
           duplicate, not duplicate, related, or no decision.

        6. Reviewer decisions are stored in reviewer_feedback.csv.
        """
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.caption(
    "Synthetic Jira-style demo data only; no proprietary company data is used."
)