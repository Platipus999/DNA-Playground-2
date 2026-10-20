
import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="DNA Playground",
    page_icon="🧬",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    .metric-card {
        padding: 20px;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        background: rgba(128, 128, 128, 0.04);
    }
    .base {
        display: inline-block;
        padding: 5px 7px;
        margin: 2px;
        border-radius: 5px;
        font-family: monospace;
        font-weight: bold;
        animation: appear 0.3s ease-in;
    }
    .A { background: #d1fae5; color: #047857; }
    .T { background: #fee2e2; color: #b91c1c; }
    .G { background: #fef3c7; color: #92400e; }
    .C { background: #dbeafe; color: #1d4ed8; }

    @keyframes appear {
        from { opacity: 0; transform: translateY(5px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.title("DNA Playground")
st.write(
    "Paste a DNA sequence, analyze its composition, "
    "and visualize its basic properties."
)

# ---------- Input ----------
with st.form("sequence_form"):
    sequence_input = st.text_area(
        "Your DNA sequence",
        value="ATGCGTACGTTAGCCTAGGCTAACGT",
        height=120,
        help="Spaces and line breaks are ignored.",
    )
    submitted = st.form_submit_button(
        "Analyze sequence",
        type="primary",
    )

# ---------- Analysis ----------
if submitted:
    sequence = "".join(sequence_input.split()).upper()

    if not sequence:
        st.error("Please enter a DNA sequence.")

    elif set(sequence) - set("ATGC"):
        st.error(
            "Invalid characters found. "
            "For this first version, use only A, T, G and C."
        )

    else:
        counts = Counter(sequence)
        length = len(sequence)
        gc_percent = (
            (counts["G"] + counts["C"]) / length * 100
        )

        st.success("Sequence analyzed successfully.")
        st.balloons()

        # Main metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Sequence length", f"{length} bp")
        col2.metric("GC content", f"{gc_percent:.1f}%")
        col3.metric(
            "AT content",
            f"{100 - gc_percent:.1f}%"
        )

        st.divider()

        # Nucleotide counts
        st.subheader("Nucleotide composition")

        chart_data = {
            "Nucleotide": ["A", "T", "G", "C"],
            "Count": [counts[b] for b in "ATGC"],
        }

        st.bar_chart(
            chart_data,
            x="Nucleotide",
            y="Count",
            color="#4F7DF3",
        )

        # Animated progress indicator
        st.subheader("GC content")
        st.progress(
            int(round(gc_percent)),
            text=f"{gc_percent:.1f}% of bases are G or C",
        )

        # Colored sequence visualization
        st.subheader("Your sequence")

        colored_sequence = "".join(
            f'<span class="base {base}">{base}</span>'
            for base in sequence
        )

        st.markdown(
            f'<div style="line-height:2.5; '
            f'overflow-wrap:anywhere;">'
            f'{colored_sequence}</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "GC content is a basic sequence statistic, "
            "not a complete prediction of DNA stability."
        )

else:
    st.info("Enter a sequence and click Analyze to get started.")

st.divider()
st.caption("Built with Python and Streamlit.")
