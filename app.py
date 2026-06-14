import streamlit as st
st.set_page_config(page_title="Village Development Planner AI", page_icon="🏘️", layout="wide")

from utils.azure_client import get_ai_response
from utils.data import get_village_data, SCHEMES
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: #f8fafc; }
[data-testid="stSidebar"] { background: #1e293b !important; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .sidebar-title { color: #fff !important; font-size: 18px; font-weight: 700; }

.metric-card {
  background: white; border-radius: 12px; padding: 1.2rem 1.4rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07); border: 1px solid #e2e8f0;
}
.metric-label { font-size: 12px; color: #64748b; font-weight: 500; margin-bottom: 4px; }
.metric-value { font-size: 26px; font-weight: 700; color: #1e293b; }
.metric-sub { font-size: 12px; margin-top: 4px; }
.green { color: #16a34a; } .orange { color: #d97706; } .red { color: #dc2626; }

.agent-card {
  background: white; border-radius: 12px; padding: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07); border: 1px solid #e2e8f0;
  text-align: center; height: 100%;
}
.agent-icon { font-size: 28px; margin-bottom: 6px; }
.agent-name { font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 8px; }
.agent-score { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.priority-badge {
  display: inline-block; font-size: 11px; font-weight: 500;
  padding: 2px 10px; border-radius: 20px;
}
.high { background: #fee2e2; color: #dc2626; }
.medium { background: #fef3c7; color: #d97706; }
.low { background: #dcfce7; color: #16a34a; }

.phase-card {
  background: white; border-radius: 12px; padding: 1.2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07); border: 1px solid #e2e8f0; height: 100%;
}
.phase-title { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
.phase-duration { font-size: 12px; color: #64748b; margin-bottom: 10px; }
.phase-budget { font-size: 14px; font-weight: 600; margin-top: 10px; }

.scheme-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 8px 0; border-bottom: 1px solid #f1f5f9;
}
.scheme-name { font-size: 13px; color: #1e293b; }
.scheme-amount { font-size: 13px; font-weight: 600; color: #2563eb; }

.section-title { font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 4px; }
.section-sub { font-size: 13px; color: #64748b; margin-bottom: 1rem; }

.sim-card {
  background: white; border-radius: 12px; padding: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.07); border: 1px solid #e2e8f0;
  text-align: center;
}
.sim-icon { font-size: 24px; margin-bottom: 6px; }
.sim-q { font-size: 13px; font-weight: 600; color: #1e293b; margin-bottom: 4px; }
.sim-a { font-size: 12px; color: #64748b; }

.priority-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
.priority-num { width: 24px; height: 24px; border-radius: 50%; background: #1e293b; color: white; font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.priority-name { flex: 1; font-size: 13px; font-weight: 500; color: #1e293b; }
.priority-impact { font-size: 11px; font-weight: 500; }

.stButton > button {
  background: #1e293b !important; color: white !important;
  border-radius: 8px !important; border: none !important;
  font-weight: 500 !important; font-size: 13px !important;
}
.new-analysis-btn > button {
  background: #16a34a !important; color: white !important;
  border-radius: 8px !important;
}
div[data-testid="column"] { padding: 0 4px; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "village" not in st.session_state:
    st.session_state.village = "Rampur Village"
if "data" not in st.session_state:
    st.session_state.data = get_village_data("Rampur Village")
if "ai_plan" not in st.session_state:
    st.session_state.ai_plan = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding:0.5rem 0 1.5rem;'>
      <div style='width:40px;height:40px;background:#16a34a;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;'>🏘️</div>
      <div>
        <div style='color:white;font-size:15px;font-weight:700;'>Village Development</div>
        <div style='color:#94a3b8;font-size:11px;'>Planner AI</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    pages = ["Dashboard", "Village Profile", "Agent Analysis", "Budget Allocation",
             "Development Roadmap", "Scheme Intelligence", "What-If Simulation", "Reports"]
    icons = ["🏠", "🏡", "🤖", "💰", "🗺️", "📋", "🔬", "📊"]

    for icon, page in zip(icons, pages):
        active = st.session_state.page == page
        style = "background:#334155;border-radius:8px;" if active else ""
        if st.sidebar.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("<div style='color:#94a3b8;font-size:11px;padding:0.5rem;'>Built with ❤️ using Streamlit & Azure AI Foundry · Empowering Rural India</div>", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
d = st.session_state.data
agents = d["agents"]

# ── DASHBOARD PAGE ────────────────────────────────────────────────────────────
if st.session_state.page == "Dashboard":

    # Header
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"<h2 style='margin:0;color:#1e293b;'>Welcome back, Bhanu Pratap! 👋</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#64748b;margin:4px 0 1rem;'>Here's the development overview for {st.session_state.village}</p>", unsafe_allow_html=True)
    with col_h2:
        village_options = ["Rampur Village", "Sundarpur Village", "Krishnapur Village"]
        selected = st.selectbox("", village_options, index=village_options.index(st.session_state.village) if st.session_state.village in village_options else 0, label_visibility="collapsed")
        if selected != st.session_state.village:
            st.session_state.village = selected
            st.session_state.data = get_village_data(selected)
            st.session_state.ai_plan = None
            st.rerun()
        if st.button("✨ New Analysis", use_container_width=True):
            with st.spinner("Azure AI Foundry agents analyzing your village..."):
                st.session_state.ai_plan = get_ai_response(st.session_state.village, d)
            st.success("Analysis complete!")

    # Top Metrics
    m = d["metrics"]
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>👥 Population</div>
          <div class='metric-value'>{m['population']:,}</div>
          <div class='metric-sub green'>+{m['pop_growth']} from last year</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        color = "green" if m['dev_score'] >= 70 else "orange" if m['dev_score'] >= 50 else "red"
        label = "Good" if m['dev_score'] >= 70 else "Moderate" if m['dev_score'] >= 50 else "Poor"
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>🎯 Overall Dev Score</div>
          <div class='metric-value'>{m['dev_score']} / 100</div>
          <div class='metric-sub {color}'>{label}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>💰 Total Budget Available</div>
          <div class='metric-value'>₹{m['budget']}</div>
          <div class='metric-sub' style='color:#64748b;'>For 2024-25</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>🚩 Priority Areas</div>
          <div class='metric-value red'>{m['priority_areas']}</div>
          <div class='metric-sub red'>High Priority</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class='metric-card'>
          <div class='metric-label'>🤖 Agents Activated</div>
          <div class='metric-value green'>7 / 7</div>
          <div class='metric-sub green'>All Agents Active</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Agent Analysis + Budget Chart
    left, right = st.columns([2, 1])

    with left:
        st.markdown("<div class='section-title'>Agent Analysis Overview</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>AI Agents analyze different aspects of village development</div>", unsafe_allow_html=True)
        cols = st.columns(7)
        for i, (name, info) in enumerate(agents.items()):
            score = info["score"]
            color = "red" if score < 50 else "orange" if score < 70 else "green"
            priority = "High Priority" if score < 50 else "Medium Priority" if score < 70 else "Low Priority"
            badge = "high" if score < 50 else "medium" if score < 70 else "low"
            with cols[i]:
                st.markdown(f"""<div class='agent-card'>
                  <div class='agent-icon'>{info['icon']}</div>
                  <div class='agent-name'>{name}<br>Agent</div>
                  <div class='agent-score {color}'>{score}/100</div>
                  <span class='priority-badge {badge}'>{priority}</span>
                </div>""", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='section-title'>Budget Allocation (₹ in Lakhs)</div>", unsafe_allow_html=True)
        budget_data = d["budget_allocation"]
        fig = go.Figure(data=[go.Pie(
            labels=list(budget_data.keys()),
            values=list(budget_data.values()),
            hole=0.6,
            textinfo='none',
            marker=dict(colors=['#3b82f6','#ef4444','#22c55e','#f59e0b','#8b5cf6','#06b6d4'])
        )])
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), height=200,
            showlegend=True,
            legend=dict(orientation="v", x=1, y=0.5, font=dict(size=11)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        total = sum(budget_data.values())
        st.markdown(f"<p style='text-align:center;font-size:13px;color:#64748b;'>Total Allocated: <strong>₹{total:.2f} Lakh</strong></p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Roadmap + Priorities + Schemes
    r1, r2, r3 = st.columns([3, 1, 1])

    with r1:
        st.markdown("<div class='section-title'>Development Roadmap <span style='font-size:14px;font-weight:400;color:#64748b;'>(3 Year Plan)</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>AI generated phased development plan for sustainable growth</div>", unsafe_allow_html=True)
        phases = d["phases"]
        pc1, pc2, pc3 = st.columns(3)
        colors = ["#16a34a", "#2563eb", "#7c3aed"]
        for col, phase, color in zip([pc1, pc2, pc3], phases, colors):
            with col:
                items = "".join([f"<li style='font-size:12px;color:#475569;margin-bottom:3px;'>{item}</li>" for item in phase["items"]])
                st.markdown(f"""<div class='phase-card'>
                  <div class='phase-title' style='color:{color};'>📌 {phase['name']}</div>
                  <div class='phase-duration' style='color:{color};'>{phase['duration']}</div>
                  <ul style='padding-left:16px;margin:0;'>{items}</ul>
                  <div class='phase-budget' style='color:{color};'>Budget: ₹{phase['budget']}</div>
                </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("<div class='section-title'>Top Priorities</div>", unsafe_allow_html=True)
        for i, p in enumerate(d["priorities"], 1):
            impact_color = "#dc2626" if p["impact"] == "High Impact" else "#d97706"
            st.markdown(f"""<div class='priority-row'>
              <div class='priority-num'>{i}</div>
              <div class='priority-name'>{p['name']}</div>
              <div class='priority-impact' style='color:{impact_color};'>{p['impact']}</div>
            </div>""", unsafe_allow_html=True)

    with r3:
        st.markdown("<div class='section-title'>Scheme Intelligence</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub' style='font-size:11px;'>Top govt schemes for this village</div>", unsafe_allow_html=True)
        for scheme in SCHEMES[:4]:
            st.markdown(f"""<div class='scheme-item'>
              <div><span style='color:#16a34a;'>✓</span> <span class='scheme-name'>{scheme['name']}</span></div>
              <div class='scheme-amount'>₹{scheme['amount']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # What-If Simulation
    st.markdown("<div class='section-title'>What-If Simulation <span style='font-size:13px;font-weight:400;color:#64748b;'>Test different scenarios and see potential impacts</span></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    sims = [
        ("🌧️", "What if rainfall decreases by 20%?", "Water risk increases by 35%"),
        ("💰", "What if budget increases by 10%?", "Overall score can improve to 72/100"),
        ("📚", "What if we focus more on education?", "Long term employment can improve"),
        ("➕", "Create Custom Scenario", "Define your own scenario"),
    ]
    for col, (icon, q, a) in zip([s1, s2, s3, s4], sims):
        with col:
            st.markdown(f"""<div class='sim-card'>
              <div class='sim-icon'>{icon}</div>
              <div class='sim-q'>{q}</div>
              <div class='sim-a'>{a}</div>
            </div>""", unsafe_allow_html=True)
            st.button("Simulate" if icon != "➕" else "Create New", key=f"sim_{q[:10]}", use_container_width=True)

    # AI Plan output
    if st.session_state.ai_plan:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🤖 Azure AI Foundry — Agent Reasoning Output</div>", unsafe_allow_html=True)
        st.markdown(f"""<div style='background:white;border-radius:12px;padding:1.5rem;border:1px solid #e2e8f0;'>
          <p style='color:#475569;font-size:14px;line-height:1.7;'>{st.session_state.ai_plan}</p>
        </div>""", unsafe_allow_html=True)

# ── AGENT ANALYSIS PAGE ───────────────────────────────────────────────────────
elif st.session_state.page == "Agent Analysis":
    st.markdown("<h2 style='color:#1e293b;'>🤖 Agent Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Each AI agent analyzes a specific domain of village development</p>", unsafe_allow_html=True)

    for name, info in agents.items():
        with st.expander(f"{info['icon']} {name} Agent — Score: {info['score']}/100"):
            c1, c2 = st.columns([1, 2])
            with c1:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=info["score"],
                    gauge=dict(
                        axis=dict(range=[0, 100]),
                        bar=dict(color="#16a34a" if info["score"] >= 70 else "#d97706" if info["score"] >= 50 else "#dc2626"),
                        bgcolor="white",
                        steps=[dict(range=[0,50], color="#fee2e2"), dict(range=[50,70], color="#fef3c7"), dict(range=[70,100], color="#dcfce7")]
                    ),
                    domain=dict(x=[0,1], y=[0,1])
                ))
                fig.update_layout(height=200, margin=dict(t=20,b=0,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.markdown(f"**Key Issues:** {', '.join(info['issues'])}")
                st.markdown(f"**Recommendations:**")
                for rec in info['recommendations']:
                    st.markdown(f"- {rec}")
                if st.button(f"Run {name} Agent Analysis", key=f"agent_{name}"):
                    with st.spinner(f"Azure AI Foundry {name} agent analyzing..."):
                        result = get_ai_response(st.session_state.village, d, agent=name)
                    st.success(result)

# ── BUDGET PAGE ───────────────────────────────────────────────────────────────
elif st.session_state.page == "Budget Allocation":
    st.markdown("<h2 style='color:#1e293b;'>💰 Budget Allocation</h2>", unsafe_allow_html=True)
    budget_data = d["budget_allocation"]
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(values=list(budget_data.values()), names=list(budget_data.keys()), hole=0.5, title="Budget Distribution")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        df = pd.DataFrame({"Sector": list(budget_data.keys()), "Amount (₹ Lakh)": list(budget_data.values())})
        fig2 = px.bar(df, x="Sector", y="Amount (₹ Lakh)", color="Sector", title="Sector-wise Allocation")
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    st.dataframe(df, use_container_width=True)

# ── SCHEME INTELLIGENCE PAGE ──────────────────────────────────────────────────
elif st.session_state.page == "Scheme Intelligence":
    st.markdown("<h2 style='color:#1e293b;'>📋 Scheme Intelligence</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Top government schemes recommended for your village</p>", unsafe_allow_html=True)
    for scheme in SCHEMES:
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1: st.markdown(f"**✅ {scheme['name']}**")
            with c2: st.markdown(f"₹{scheme['amount']}")
            with c3: st.button("Apply", key=f"scheme_{scheme['name']}")
            st.divider()

# ── WHAT-IF PAGE ──────────────────────────────────────────────────────────────
elif st.session_state.page == "What-If Simulation":
    st.markdown("<h2 style='color:#1e293b;'>🔬 What-If Simulation</h2>", unsafe_allow_html=True)
    scenario = st.text_area("Describe your scenario:", placeholder="e.g. What if we build a solar plant and provide free electricity to all homes?")
    if st.button("🚀 Run AI Simulation") and scenario:
        with st.spinner("Azure AI Foundry reasoning through your scenario..."):
            result = get_ai_response(st.session_state.village, d, scenario=scenario)
        st.markdown("### Simulation Result")
        st.markdown(f"""<div style='background:white;border-radius:12px;padding:1.5rem;border:1px solid #e2e8f0;'>
          <p style='color:#475569;font-size:14px;line-height:1.7;'>{result}</p>
        </div>""", unsafe_allow_html=True)

# ── OTHER PAGES ───────────────────────────────────────────────────────────────
else:
    st.markdown(f"<h2 style='color:#1e293b;'>{st.session_state.page}</h2>", unsafe_allow_html=True)
    st.info("This section is coming soon. Use the Dashboard to explore village insights!")
