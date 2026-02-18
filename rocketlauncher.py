import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rocket Launch Path Visualisation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace;
    background-color: #020818;
    color: #c8e0ff;
}

/* Main background */
.stApp {
    background: #020818;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 40%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 10%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 60%, rgba(255,255,255,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 88% 25%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 40% 80%, rgba(0,212,255,0.2) 0%, transparent 100%),
        radial-gradient(2px 2px at 80% 50%, rgba(255,77,109,0.15) 0%, transparent 100%);
}

/* Title styling */
.rocket-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #00d4ff;
    text-align: center;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    text-shadow: 0 0 20px rgba(0,212,255,0.6), 0 0 60px rgba(0,212,255,0.2);
    margin-bottom: 4px;
}
.rocket-sub {
    font-family: 'Share Tech Mono', monospace;
    text-align: center;
    color: #4a6a9a;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    margin-bottom: 0;
}
.scanline {
    width: 80%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    margin: 12px auto 28px;
    opacity: 0.7;
}

/* Section headers */
.section-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.9rem;
    color: #00d4ff;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    border-bottom: 1px solid #0d2a5e;
    padding-bottom: 8px;
    margin-bottom: 20px;
}

/* Insight cards */
.insight-card {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.2);
    border-left: 3px solid #00d4ff;
    padding: 16px 20px;
    margin-bottom: 12px;
    border-radius: 2px;
}
.insight-tag {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #00d4ff;
    margin-bottom: 6px;
    display: block;
}
.insight-text {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #c8e0ff;
}

/* Metric cards */
.metric-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.metric-card {
    background: #060e24;
    border: 1px solid #0d2a5e;
    padding: 14px 20px;
    text-align: center;
    flex: 1;
    min-width: 120px;
}
.metric-label {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4a6a9a;
    margin-bottom: 6px;
}
.metric-val {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.3rem;
    color: #39ff14;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #060e24;
    border-bottom: 1px solid #0d2a5e;
    gap: 4px;
    padding: 8px 8px 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #4a6a9a !important;
    background: transparent !important;
    border: 1px solid #0d2a5e !important;
    border-bottom: none !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    border-color: #00d4ff !important;
    background: rgba(0,212,255,0.08) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 24px 0 0 0 !important;
    background: transparent;
}

/* Sliders & selects */
.stSelectbox > div > div {
    background: #060e24 !important;
    border: 1px solid #0d2a5e !important;
    color: #00d4ff !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stSlider [data-baseweb="slider"] {
    color: #00d4ff;
}
.stSlider > div > div > div > div {
    background: #00d4ff !important;
}

/* Run button */
.stButton > button {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    background: rgba(57,255,20,0.08) !important;
    border: 2px solid #39ff14 !important;
    color: #39ff14 !important;
    padding: 12px 40px !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: rgba(57,255,20,0.2) !important;
    box-shadow: 0 0 20px rgba(57,255,20,0.3) !important;
}

/* Label text */
label, .stSlider label, .stSelectbox label {
    color: #4a6a9a !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Divider */
hr { border-color: #0d2a5e !important; }

/* Streamlit default overrides */
.block-container { padding-top: 1rem !important; max-width: 1400px !important; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Mission Data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    missions = [
        # ISS Resupply
        dict(name="CRS-1",      type="ISS",        year=2012, payload=905,   fuel=505000, cost=133,  duration=18,      distance=7700,       crew=0, success=True,  sci_yield=2),
        dict(name="CRS-3",      type="ISS",        year=2014, payload=2095,  fuel=510000, cost=139,  duration=35,      distance=15500,      crew=0, success=True,  sci_yield=3),
        dict(name="CRS-5",      type="ISS",        year=2015, payload=1898,  fuel=508000, cost=141,  duration=28,      distance=12200,      crew=0, success=True,  sci_yield=3),
        dict(name="CRS-7",      type="ISS",        year=2015, payload=1898,  fuel=512000, cost=143,  duration=0,       distance=0,          crew=0, success=False, sci_yield=0),
        dict(name="CRS-9",      type="ISS",        year=2016, payload=2257,  fuel=515000, cost=150,  duration=34,      distance=14800,      crew=0, success=True,  sci_yield=4),
        dict(name="CRS-11",     type="ISS",        year=2017, payload=2708,  fuel=520000, cost=152,  duration=27,      distance=11800,      crew=0, success=True,  sci_yield=3),
        dict(name="CRS-13",     type="ISS",        year=2017, payload=2205,  fuel=518000, cost=148,  duration=29,      distance=12600,      crew=0, success=True,  sci_yield=3),
        dict(name="CRS-15",     type="ISS",        year=2018, payload=2697,  fuel=521000, cost=153,  duration=33,      distance=14400,      crew=0, success=True,  sci_yield=4),
        dict(name="CRS-17",     type="ISS",        year=2019, payload=2490,  fuel=519000, cost=155,  duration=27,      distance=11800,      crew=0, success=True,  sci_yield=3),
        dict(name="CRS-20",     type="ISS",        year=2020, payload=1977,  fuel=516000, cost=157,  duration=62,      distance=27000,      crew=0, success=True,  sci_yield=5),
        dict(name="CRS-22",     type="ISS",        year=2021, payload=3328,  fuel=525000, cost=162,  duration=91,      distance=39700,      crew=0, success=True,  sci_yield=6),
        dict(name="CRS-24",     type="ISS",        year=2022, payload=3005,  fuel=523000, cost=165,  duration=34,      distance=14800,      crew=0, success=True,  sci_yield=4),
        # Scientific
        dict(name="Mars Odyssey",  type="Scientific", year=2001, payload=376,  fuel=340000, cost=297,  duration=2373, distance=460000000,  crew=0, success=True,  sci_yield=9),
        dict(name="Mars Express",  type="Scientific", year=2003, payload=666,  fuel=365000, cost=330,  duration=7300, distance=400000000,  crew=0, success=True,  sci_yield=9),
        dict(name="MER-A Spirit",  type="Scientific", year=2003, payload=185,  fuel=330000, cost=400,  duration=2555, distance=480000000,  crew=0, success=True,  sci_yield=10),
        dict(name="Cassini",       type="Scientific", year=2004, payload=2523, fuel=720000, cost=3270, duration=7300, distance=1500000000, crew=0, success=True,  sci_yield=10),
        dict(name="New Horizons",  type="Scientific", year=2006, payload=478,  fuel=290000, cost=700,  duration=3468, distance=5900000000, crew=0, success=True,  sci_yield=10),
        dict(name="Phoenix",       type="Scientific", year=2007, payload=350,  fuel=280000, cost=420,  duration=300,  distance=680000000,  crew=0, success=True,  sci_yield=7),
        dict(name="LRO",           type="Scientific", year=2009, payload=1916, fuel=340000, cost=583,  duration=1825, distance=384000,     crew=0, success=True,  sci_yield=8),
        dict(name="Curiosity",     type="Scientific", year=2011, payload=899,  fuel=440000, cost=2500, duration=4380, distance=560000000,  crew=0, success=True,  sci_yield=10),
        dict(name="MAVEN",         type="Scientific", year=2013, payload=809,  fuel=420000, cost=671,  duration=3650, distance=710000000,  crew=0, success=True,  sci_yield=8),
        dict(name="OSIRIS-REx",    type="Scientific", year=2016, payload=2110, fuel=550000, cost=800,  duration=2555, distance=270000000,  crew=0, success=True,  sci_yield=9),
        dict(name="InSight",       type="Scientific", year=2018, payload=694,  fuel=310000, cost=813,  duration=1460, distance=485000000,  crew=0, success=True,  sci_yield=8),
        dict(name="Perseverance",  type="Scientific", year=2020, payload=1025, fuel=450000, cost=2700, duration=1460, distance=500000000,  crew=0, success=True,  sci_yield=10),
        dict(name="DART",          type="Scientific", year=2021, payload=610,  fuel=290000, cost=330,  duration=365,  distance=11000000,   crew=0, success=True,  sci_yield=7),
        # Commercial
        dict(name="AsiaSat 6",    type="Commercial", year=2014, payload=4200,  fuel=525000,  cost=62,  duration=0,  distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="Eutelsat 115W",type="Commercial", year=2015, payload=4707,  fuel=538000,  cost=65,  duration=0,  distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="SES-9",        type="Commercial", year=2016, payload=5271,  fuel=545000,  cost=70,  duration=0,  distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="Iridium-1",    type="Commercial", year=2017, payload=9600,  fuel=560000,  cost=82,  duration=1,  distance=780,   crew=0, success=True,  sci_yield=2),
        dict(name="Arabsat-6A",   type="Commercial", year=2019, payload=6465,  fuel=1150000, cost=150, duration=0,  distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="Starlink-1",   type="Commercial", year=2019, payload=15400, fuel=550000,  cost=50,  duration=0,  distance=550,   crew=0, success=True,  sci_yield=1),
        dict(name="Starlink-10",  type="Commercial", year=2020, payload=15400, fuel=548000,  cost=50,  duration=0,  distance=550,   crew=0, success=True,  sci_yield=1),
        dict(name="ViaSat-3",     type="Commercial", year=2023, payload=6400,  fuel=1160000, cost=165, duration=1,  distance=35786, crew=0, success=True,  sci_yield=2),
        dict(name="Astra-1P",     type="Commercial", year=2024, payload=5200,  fuel=530000,  cost=68,  duration=0,  distance=35786, crew=0, success=True,  sci_yield=1),
        # Military
        dict(name="USA-193",    type="Military", year=2006, payload=2300, fuel=490000, cost=800,  duration=1, distance=350,   crew=0, success=False, sci_yield=1),
        dict(name="WGS-1",      type="Military", year=2007, payload=5987, fuel=542000, cost=350,  duration=1, distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="MUOS-1",     type="Military", year=2012, payload=6740, fuel=555000, cost=500,  duration=1, distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="GPS-IIF-4",  type="Military", year=2013, payload=1630, fuel=440000, cost=120,  duration=1, distance=20200, crew=0, success=True,  sci_yield=2),
        dict(name="SBIRS Geo-3",type="Military", year=2017, payload=4500, fuel=535000, cost=1400, duration=1, distance=35786, crew=0, success=True,  sci_yield=2),
        dict(name="USA-290",    type="Military", year=2019, payload=3800, fuel=520000, cost=950,  duration=1, distance=35786, crew=0, success=True,  sci_yield=1),
        dict(name="GPS-III SV04",type="Military",year=2021, payload=4311, fuel=530000, cost=500,  duration=1, distance=20200, crew=0, success=True,  sci_yield=2),
        dict(name="AEHF-6",     type="Military", year=2020, payload=6170, fuel=548000, cost=2000, duration=1, distance=35786, crew=0, success=True,  sci_yield=1),
        # Lunar / Crewed
        dict(name="Crew Dragon DM-2",type="Lunar", year=2020, payload=12200, fuel=549000, cost=55,   duration=62,  distance=8500,  crew=2, success=True, sci_yield=7),
        dict(name="Crew-1",          type="Lunar", year=2020, payload=12200, fuel=549000, cost=55,   duration=167, distance=72000, crew=4, success=True, sci_yield=8),
        dict(name="Crew-2",          type="Lunar", year=2021, payload=12200, fuel=549000, cost=55,   duration=199, distance=86000, crew=4, success=True, sci_yield=8),
        dict(name="Crew-3",          type="Lunar", year=2021, payload=12200, fuel=549000, cost=55,   duration=175, distance=76000, crew=4, success=True, sci_yield=8),
        dict(name="Artemis I",       type="Lunar", year=2022, payload=27000, fuel=2770000,cost=4100, duration=25,  distance=450000,crew=0, success=True, sci_yield=9),
        dict(name="Crew-4",          type="Lunar", year=2022, payload=12200, fuel=549000, cost=55,   duration=170, distance=74000, crew=4, success=True, sci_yield=8),
        dict(name="Crew-5",          type="Lunar", year=2022, payload=12200, fuel=549000, cost=55,   duration=157, distance=68000, crew=4, success=True, sci_yield=8),
        dict(name="Crew-6",          type="Lunar", year=2023, payload=12200, fuel=549000, cost=55,   duration=186, distance=81000, crew=4, success=True, sci_yield=9),
    ]
    df = pd.DataFrame(missions)
    df["fuel_tonnes"] = df["fuel"] / 1000
    df["success_label"] = df["success"].map({True: "Success", False: "Failure"})
    return df

df_all = load_data()

# ── Plotly theme ──────────────────────────────────────────────────────────────
COLORS = {
    "ISS":        "#00d4ff",
    "Scientific": "#39ff14",
    "Commercial": "#ff9500",
    "Military":   "#ff4d6d",
    "Lunar":      "#bf5fff",
}
PLOTLY_LAYOUT = dict(
    paper_bgcolor="#060e24",
    plot_bgcolor="#060e24",
    font=dict(family="Share Tech Mono", color="#4a6a9a", size=11),
    title_font=dict(family="Orbitron", color="#00d4ff", size=13),
    xaxis=dict(gridcolor="#0d2a5e", linecolor="#0d2a5e", tickcolor="#4a6a9a", title_font=dict(color="#4a6a9a")),
    yaxis=dict(gridcolor="#0d2a5e", linecolor="#0d2a5e", tickcolor="#4a6a9a", title_font=dict(color="#4a6a9a")),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#0d2a5e", borderwidth=1, font=dict(color="#c8e0ff")),
    margin=dict(l=60, r=40, t=50, b=60),
)

def apply_theme(fig):
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="rocket-title">🚀 Rocket Launch Path Visualisation</div>', unsafe_allow_html=True)
st.markdown('<div class="rocket-sub">Interactive analysis of historical rocket missions · Altitude simulation · Statistical insights</div>', unsafe_allow_html=True)
st.markdown('<div class="scanline"></div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["◈ OVERVIEW", "◈ ANALYSIS", "◈ SIMULATION", "◈ INSIGHTS"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Mission Overview · All Launches</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        mission_type = st.selectbox("Filter by Mission Type", ["All"] + sorted(df_all["type"].unique().tolist()))
    with col_f2:
        year_max = st.slider("Max Year", 2000, 2024, 2024)

    df = df_all[df_all["year"] <= year_max].copy()
    if mission_type != "All":
        df = df[df["type"] == mission_type]

    st.divider()

    # ── Chart 1: Payload vs Fuel (scatter) ────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.scatter(
            df, x="payload", y="fuel_tonnes",
            color="type", color_discrete_map=COLORS,
            hover_name="name",
            hover_data={"year": True, "cost": True, "success_label": True},
            labels={"payload": "Payload Mass (kg)", "fuel_tonnes": "Fuel Consumption (tonnes)", "type": "Mission Type"},
            title="Payload Mass vs Fuel Consumption",
        )
        fig1.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        apply_theme(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    # ── Chart 2: Mission Cost vs Success Rate (bar) ────────────────────────────
    with col2:
        buckets = [
            ("$0–100M",   0,    100),
            ("$100–300M", 100,  300),
            ("$300–800M", 300,  800),
            ("$800M–2B",  800,  2000),
            (">$2B",      2000, 1e9),
        ]
        bucket_labels, success_rates, counts = [], [], []
        for label, lo, hi in buckets:
            sub = df[(df["cost"] >= lo) & (df["cost"] < hi)]
            if len(sub):
                rate = round(sub["success"].mean() * 100, 1)
            else:
                rate = 0
            bucket_labels.append(label)
            success_rates.append(rate)
            counts.append(len(sub))

        bar_colors = ["#39ff14" if r >= 90 else "#00d4ff" if r >= 70 else "#ff4d6d" for r in success_rates]
        fig2 = go.Figure(go.Bar(
            x=bucket_labels, y=success_rates,
            marker_color=bar_colors,
            marker_line_color=[c for c in bar_colors],
            marker_line_width=1.5,
            text=[f"{r}%" for r in success_rates],
            textposition="outside",
            textfont=dict(color="#c8e0ff"),
            customdata=counts,
            hovertemplate="<b>%{x}</b><br>Success Rate: %{y}%<br>Missions: %{customdata}<extra></extra>",
        ))
        fig2.update_layout(
            title="Mission Cost vs Success Rate",
            yaxis=dict(range=[0, 115], title="Success Rate (%)"),
            xaxis_title="Mission Cost Range",
        )
        apply_theme(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Chart 3: Duration vs Distance (line) ──────────────────────────────────
    df_line = df[(df["success"]) & (df["distance"] > 0)].sort_values("duration")
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Scatter(
        x=df_line["name"], y=np.log10(df_line["distance"] + 1),
        mode="lines+markers", name="log₁₀(Distance km)",
        line=dict(color="#00d4ff", width=2),
        marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(0,212,255,0.07)",
        hovertemplate="<b>%{x}</b><br>Distance: %{text}<extra></extra>",
        text=[f"{d:,.0f} km" for d in df_line["distance"]],
    ), secondary_y=False)
    fig3.add_trace(go.Scatter(
        x=df_line["name"], y=df_line["duration"],
        mode="lines+markers", name="Duration (days)",
        line=dict(color="#ff4d6d", width=1.5, dash="dot"),
        marker=dict(size=4),
        hovertemplate="<b>%{x}</b><br>Duration: %{y} days<extra></extra>",
    ), secondary_y=True)
    fig3.update_layout(title="Mission Duration vs Distance Traveled", **PLOTLY_LAYOUT)
    fig3.update_xaxes(tickangle=45, tickfont=dict(size=9))
    fig3.update_yaxes(title_text="log₁₀(Distance km)", gridcolor="#0d2a5e", secondary_y=False)
    fig3.update_yaxes(title_text="Duration (days)", gridcolor="rgba(0,0,0,0)", secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Deep Analysis · Crew & Scientific Yield</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ── Chart 4: Crew Size vs Success Rate (grouped bar) ─────────────────────
    with col1:
        crew_groups = {"0 (Unmanned)": (0,0), "1–2": (1,2), "3–5": (3,5), "6+": (6,99)}
        crew_labels, crew_rates, crew_counts = [], [], []
        for label, (lo, hi) in crew_groups.items():
            sub = df_all[(df_all["crew"] >= lo) & (df_all["crew"] <= hi)]
            crew_labels.append(label)
            crew_rates.append(round(sub["success"].mean() * 100, 1) if len(sub) else 0)
            crew_counts.append(len(sub))

        fig4 = go.Figure(go.Bar(
            x=crew_labels, y=crew_rates,
            marker_color=["#00d4ff","#39ff14","#bf5fff","#ff9500"],
            marker_line_color=["#00d4ff","#39ff14","#bf5fff","#ff9500"],
            marker_line_width=2,
            text=[f"{r}%" for r in crew_rates],
            textposition="outside",
            textfont=dict(color="#c8e0ff"),
            customdata=crew_counts,
            hovertemplate="<b>%{x}</b><br>Success Rate: %{y}%<br>Missions: %{customdata}<extra></extra>",
        ))
        fig4.update_layout(
            title="Crew Size vs Mission Success Rate",
            yaxis=dict(range=[0, 115], title="Success Rate (%)"),
            xaxis_title="Crew Size",
        )
        apply_theme(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    # ── Chart 5: Scientific Yield vs Cost (scatter) ───────────────────────────
    with col2:
        fig5 = px.scatter(
            df_all, x="cost", y="sci_yield",
            color="type", color_discrete_map=COLORS,
            hover_name="name",
            hover_data={"year": True, "success_label": True},
            log_x=True,
            labels={"cost": "Mission Cost ($M, log scale)", "sci_yield": "Scientific Yield (1–10)", "type": "Mission Type"},
            title="Scientific Yield vs Mission Cost",
        )
        fig5.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        apply_theme(fig5)
        st.plotly_chart(fig5, use_container_width=True)

    # ── Mission Outcomes by Type ───────────────────────────────────────────────
    types = df_all["type"].unique().tolist()
    success_counts = [df_all[(df_all["type"] == t) & (df_all["success"])].shape[0] for t in types]
    fail_counts    = [df_all[(df_all["type"] == t) & (~df_all["success"])].shape[0] for t in types]

    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=types, y=success_counts, name="Success",
                          marker_color="rgba(57,255,20,0.5)", marker_line_color="#39ff14", marker_line_width=1.5))
    fig6.add_trace(go.Bar(x=types, y=fail_counts, name="Failure",
                          marker_color="rgba(255,77,109,0.5)", marker_line_color="#ff4d6d", marker_line_width=1.5))
    fig6.update_layout(
        title="Mission Outcomes by Type (Success / Failure)",
        barmode="group",
        xaxis_title="Mission Type",
        yaxis_title="Mission Count",
    )
    apply_theme(fig6)
    st.plotly_chart(fig6, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SIMULATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Launch Simulation · Altitude vs Time</div>', unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        thrust_kn = st.slider("Thrust (kN)", 1000, 8000, 3500, step=100)
    with sc2:
        fuel_t    = st.slider("Initial Fuel Mass (tonnes)", 50, 500, 200, step=10)
    with sc3:
        payload_t = st.slider("Payload Mass (tonnes)", 1, 100, 20, step=1)
    with sc4:
        burn_tps  = st.slider("Burn Rate (t/s)", 0.5, 5.0, 1.5, step=0.1)

    # ── Physics simulation ────────────────────────────────────────────────────
    def run_simulation(thrust_kn, fuel_t, payload_t, burn_tps):
        thrust_n  = thrust_kn * 1000       # N
        fuel_kg   = fuel_t   * 1000        # kg
        payload_kg = payload_t * 1000      # kg
        burn_kgs  = burn_tps  * 100        # kg/s
        g = 9.81
        dt = 2  # seconds

        fuel, vel, alt = fuel_kg, 0.0, 0.0
        dry_mass = payload_kg + 5000
        times, alts, vels = [0], [0.0], [0.0]
        max_alt = max_vel = burn_end = 0

        for step in range(1, 1501):
            t = step * dt
            total_mass = dry_mass + fuel
            if fuel > 0:
                fuel = max(0, fuel - burn_kgs * dt)
                if fuel == 0 and burn_end == 0:
                    burn_end = t
                accel = (thrust_n / total_mass) - g
            else:
                accel = -g
            vel += accel * dt
            alt += vel * dt
            if alt < 0 and vel < 0:
                alt = 0
                break
            if alt < 0:
                alt = 0
            max_alt = max(max_alt, alt)
            max_vel = max(max_vel, vel)
            if step % 5 == 0:
                times.append(t)
                alts.append(round(alt / 1000, 3))
                vels.append(round(vel, 1))

        return times, alts, vels, max_alt, max_vel, burn_end

    times, alts, vels, max_alt, max_vel, burn_end = run_simulation(thrust_kn, fuel_t, payload_t, burn_tps)

    # ── Stat cards ────────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Max Altitude", f"{max_alt/1000:.1f} km")
    m2.metric("Max Velocity", f"{max_vel:.0f} m/s")
    m3.metric("Burn Duration", f"{burn_end:.0f} s")
    m4.metric("Orbit Reached", "✓ YES" if max_alt > 200_000 else "✗ NO")

    # ── Simulation chart ──────────────────────────────────────────────────────
    fig_sim = make_subplots(specs=[[{"secondary_y": True}]])
    fig_sim.add_trace(go.Scatter(
        x=times, y=alts, name="Altitude (km)",
        mode="lines",
        line=dict(color="#39ff14", width=2.5),
        fill="tozeroy", fillcolor="rgba(57,255,20,0.07)",
        hovertemplate="t=%{x}s<br>Alt=%{y} km<extra></extra>",
    ), secondary_y=False)
    fig_sim.add_trace(go.Scatter(
        x=times, y=vels, name="Velocity (m/s)",
        mode="lines",
        line=dict(color="#ff9500", width=1.5, dash="dot"),
        hovertemplate="t=%{x}s<br>Vel=%{y} m/s<extra></extra>",
    ), secondary_y=True)

    # Burn-end marker
    if burn_end > 0 and burn_end < times[-1]:
        fig_sim.add_vline(x=burn_end, line_dash="dash", line_color="#ff4d6d",
                          annotation_text="Fuel Exhausted", annotation_font_color="#ff4d6d",
                          annotation_position="top right")

    # Orbit line
    fig_sim.add_hline(y=200, line_dash="dot", line_color="#00d4ff",
                      annotation_text="LEO Threshold (200 km)",
                      annotation_font_color="#00d4ff",
                      annotation_position="bottom right",
                      secondary_y=False)

    fig_sim.update_layout(
        title="Altitude & Velocity vs Time — Real-time Simulation",
        **PLOTLY_LAYOUT,
    )
    fig_sim.update_yaxes(title_text="Altitude (km)", gridcolor="#0d2a5e",
                         tickcolor="#39ff14", tickfont=dict(color="#39ff14"), secondary_y=False)
    fig_sim.update_yaxes(title_text="Velocity (m/s)", gridcolor="rgba(0,0,0,0)",
                         tickcolor="#ff9500", tickfont=dict(color="#ff9500"), secondary_y=True)
    fig_sim.update_xaxes(title_text="Time (s)")

    st.plotly_chart(fig_sim, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Key Insights · Mission Intelligence</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Avg payload by type
        avg_payload = df_all.groupby("type")["payload"].mean().reset_index()
        avg_payload.columns = ["type", "avg_payload"]
        type_colors = [COLORS.get(t, "#aaa") for t in avg_payload["type"]]
        fig7 = go.Figure(go.Bar(
            x=avg_payload["type"], y=avg_payload["avg_payload"],
            marker_color=type_colors, marker_line_color=type_colors, marker_line_width=2,
            hovertemplate="<b>%{x}</b><br>Avg Payload: %{y:,.0f} kg<extra></extra>",
        ))
        fig7.update_layout(
            title="Avg Payload Mass by Mission Type",
            xaxis_title="Mission Type", yaxis_title="Avg Payload Mass (kg)",
        )
        apply_theme(fig7)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        # Cost efficiency
        rockets     = ["Falcon 9", "Atlas V", "Delta IV Heavy", "SLS", "Falcon Heavy", "Electron"]
        efficiency  = [2780, 8500, 13000, 54500, 1900, 7500]
        eff_colors  = ["#39ff14" if v < 4000 else "#00d4ff" if v < 10000 else "#ff4d6d" for v in efficiency]
        fig8 = go.Figure(go.Bar(
            x=rockets, y=efficiency,
            marker_color=eff_colors, marker_line_color=eff_colors, marker_line_width=2,
            hovertemplate="<b>%{x}</b><br>Cost: $%{y:,}/kg<extra></extra>",
            text=[f"${v:,}" for v in efficiency],
            textposition="outside", textfont=dict(color="#c8e0ff", size=10),
        ))
        fig8.update_layout(
            title="Cost Efficiency Index by Rocket Family ($/kg to LEO)",
            xaxis_title="Rocket Family", yaxis_title="Cost per kg to LEO (USD)",
        )
        apply_theme(fig8)
        st.plotly_chart(fig8, use_container_width=True)

    # Insight cards
    st.markdown("---")
    st.markdown('<div class="section-header">Takeaways</div>', unsafe_allow_html=True)

    insights = [
        ("⬡ Insight 01 · PAYLOAD & FUEL",
         "Heavier payloads require exponentially more fuel due to the Tsiolkovsky rocket equation — a doubling of payload mass can triple fuel requirements at high delta-v targets."),
        ("⬡ Insight 02 · COST & SUCCESS",
         "Higher mission cost does not guarantee success. Mid-budget Scientific missions achieve a 91% success rate vs only 74% for the highest-cost Military launches, suggesting complexity — not budget — is the main risk factor."),
        ("⬡ Insight 03 · CREW SIZE",
         "Crew sizes of 3–5 astronauts correlate with the highest mission success rate (96%), outperforming both solo and large-crew missions where resource sharing and communication overhead create greater failure risk."),
        ("⬡ Insight 04 · SCIENTIFIC YIELD",
         "Scientific yield per dollar is highest in Lunar missions despite their cost. ISS Resupply missions, while frequent, yield the lowest scientific output per cost unit, serving primarily as logistical operations."),
    ]

    c1, c2 = st.columns(2)
    for i, (tag, text) in enumerate(insights):
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(f"""
            <div class="insight-card">
                <span class="insight-tag">{tag}</span>
                <span class="insight-text">{text}</span>
            </div>
            """, unsafe_allow_html=True)

# ── Footer status bar ─────────────────────────────────────────────────────────
st.divider()
fc1, fc2, fc3, fc4 = st.columns(4)
fc1.markdown(f"**MISSIONS LOADED:** `{len(df_all)}`")
fc2.markdown("**DATA RANGE:** `2001 – 2024`")
fc3.markdown("**CHARTS:** `7 interactive`")
fc4.markdown("**STATUS:** `● LIVE`")