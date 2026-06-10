import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="NEW PATH TENNIS LEAGUE",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── THEME ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --court: #1a2a1a;
    --court-mid: #1e3a2e;
    --lime: #c8f135;
    --lime-dim: #8faa20;
    --red: #ff3b30;
    --gold: #f5c542;
    --white: #f0f4f0;
    --muted: #6b8c6b;
    --card: #111f11;
    --border: #2a3f2a;
}

html, body, [data-testid="stApp"] {
    background-color: var(--court) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.stDeployButton { display: none; }

/* Main container */
.main .block-container {
    padding: 0.5rem 1rem 2rem 1rem;
    max-width: 900px;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0d1f0d 0%, #1e3a2e 50%, #0d1f0d 100%);
    border: 1px solid var(--lime);
    border-radius: 4px;
    padding: 1.5rem 1.5rem 1rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(200,241,53,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 2.8rem;
    letter-spacing: 0.08em;
    color: var(--lime);
    line-height: 1;
    margin: 0;
}
.hero-sub {
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 0.25rem;
}
.hero-badge {
    display: inline-block;
    background: var(--lime);
    color: #0d1f0d;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
    margin-top: 0.5rem;
}

/* Nav tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card);
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: var(--muted) !important;
    padding: 0.6rem 1rem;
    border-radius: 0;
    background: transparent !important;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--lime) !important;
    border-bottom: 2px solid var(--lime) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 1rem 0 0 0;
    background: transparent !important;
}

/* Cards */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.card-accent {
    border-left: 3px solid var(--lime);
}

/* Rank row */
.rank-row {
    display: flex;
    align-items: center;
    padding: 0.6rem 0.75rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 3px;
    margin-bottom: 0.4rem;
    gap: 0.75rem;
    transition: border-color 0.15s;
}
.rank-row:hover { border-color: var(--lime); }
.rank-num {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.4rem;
    color: var(--muted);
    width: 1.8rem;
    text-align: center;
    flex-shrink: 0;
}
.rank-num.top1 { color: var(--gold); }
.rank-num.top2 { color: #aaa; }
.rank-num.top3 { color: #cd7f32; }
.rank-name {
    font-weight: 600;
    font-size: 0.9rem;
    flex: 1;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.rank-pts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    color: var(--lime);
    font-weight: 600;
    flex-shrink: 0;
}
.rank-elo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    flex-shrink: 0;
}
.rank-level {
    font-size: 0.65rem;
    background: var(--border);
    padding: 0.1rem 0.35rem;
    border-radius: 2px;
    color: var(--white);
    flex-shrink: 0;
}
.streak-badge {
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    flex-shrink: 0;
}

/* Stat chip */
.chip {
    display: inline-block;
    background: var(--border);
    border-radius: 3px;
    padding: 0.15rem 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--white);
    margin: 0.15rem;
}
.chip.green { background: rgba(200,241,53,0.15); color: var(--lime); }
.chip.red { background: rgba(255,59,48,0.15); color: var(--red); }

/* Section header */
.section-head {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.2rem;
    letter-spacing: 0.1em;
    color: var(--lime);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.3rem;
    margin: 1.2rem 0 0.75rem 0;
}

/* Match row */
.match-row {
    display: flex;
    align-items: center;
    padding: 0.5rem 0.75rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 3px;
    margin-bottom: 0.3rem;
    gap: 0.5rem;
    font-size: 0.8rem;
}
.match-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    flex-shrink: 0;
    width: 5rem;
}
.match-winner { font-weight: 600; color: var(--lime); }
.match-loser { color: var(--muted); }
.match-score {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--white);
    flex-shrink: 0;
}
.match-bonus {
    font-size: 0.65rem;
    color: var(--gold);
    flex-shrink: 0;
}

/* Profile card */
.profile-header {
    background: linear-gradient(135deg, #0d1f0d, #1e3a2e);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem;
    margin-bottom: 0.75rem;
}
.profile-name {
    font-family: 'Bebas Neue', cursive;
    font-size: 2rem;
    letter-spacing: 0.05em;
    color: var(--white);
    line-height: 1.1;
}
.profile-desc {
    font-size: 0.75rem;
    color: var(--muted);
    font-style: italic;
    margin-top: 0.4rem;
    line-height: 1.4;
}

/* Skill bar */
.skill-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}
.skill-label {
    font-size: 0.7rem;
    color: var(--muted);
    width: 80px;
    flex-shrink: 0;
}
.skill-bar-bg {
    flex: 1;
    height: 6px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}
.skill-bar-fill {
    height: 100%;
    background: var(--lime);
    border-radius: 3px;
}
.skill-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--lime);
    width: 1.5rem;
    text-align: right;
}

/* Trophy row */
.trophy-row {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.6rem 0.75rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 3px;
    margin-bottom: 0.35rem;
}
.trophy-icon { font-size: 1.2rem; flex-shrink: 0; }
.trophy-name { font-weight: 600; font-size: 0.85rem; }
.trophy-winner { color: var(--lime); font-size: 0.8rem; }
.trophy-detail { color: var(--muted); font-size: 0.7rem; margin-top: 0.1rem; }

/* Rivalry row */
.rivalry-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 3px;
    margin-bottom: 0.3rem;
    font-size: 0.8rem;
}

/* Plotly dark override */
.js-plotly-plot .plotly { background: transparent !important; }

/* Select box */
.stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--white) !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.6rem 0.8rem;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.65rem !important;
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Bebas Neue', cursive !important;
    font-size: 1.8rem !important;
    color: var(--lime) !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.7rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    xl = pd.ExcelFile("NEWPATH_TENNIS_LEAGUE_2026.xlsx")

    # CLASSEMENT
    cl = pd.read_excel(xl, sheet_name='CLASSEMENT', header=0).iloc[:10]
    cl = cl[['Joueur', 'Points NewPath', 'Matchs', 'Victoires', 'Ratio victoire', 'Diff jeux / match', 'Niveau']].dropna(subset=['Joueur'])
    cl.columns = ['joueur', 'pts', 'matchs', 'victoires', 'ratio', 'diff_jeux', 'niveau']
    cl = cl.sort_values('pts', ascending=False).reset_index(drop=True)
    cl['rang'] = range(1, len(cl) + 1)

    # MATCHS
    mt = pd.read_excel(xl, sheet_name='MATCHS', header=1)
    mt = mt[['Date', 'Joueur A', 'Joueur B', 'Résultat (A-B)', 'Bonus ⚡ (0/5)',
              'Set1 A', 'Set1 B', 'Set2 A', 'Set2 B', 'Set3 A', 'Set3 B',
              'Points A', 'Points B', 'Vainqueur']].dropna(subset=['Vainqueur'])
    mt['Date'] = pd.to_datetime(mt['Date'], errors='coerce')
    mt = mt.dropna(subset=['Date'])
    mt = mt.sort_values('Date', ascending=False).reset_index(drop=True)

    # SKILLS
    sk = pd.read_excel(xl, sheet_name='SKILLS_DATA', header=0).dropna(subset=['Joueur'])
    sk = sk[['Joueur', 'Service', 'Coup droit', 'Revers', 'Vitesse', 'Mental',
              'Défense', 'Agressivité', 'Physique', 'Technique', 'Age', 'Taille', 'Poids', 'Main', 'Description']]
    sk.columns = ['joueur', 'service', 'coup_droit', 'revers', 'vitesse', 'mental',
                  'defense', 'agressivite', 'physique', 'technique', 'age', 'taille', 'poids', 'main', 'description']

    # ELO
    elo_df = pd.read_excel(xl, sheet_name='ELO_LOG', header=1)
    elo_df = elo_df[['Joueur', 'Elo après']].dropna()
    last_elo = elo_df.groupby('Joueur')['Elo après'].last().reset_index()
    last_elo.columns = ['joueur', 'elo']

    # ELO history per player
    elo_hist = elo_df.copy()
    elo_hist.columns = ['joueur', 'elo']
    elo_hist = elo_hist.reset_index()
    elo_hist.rename(columns={'index': 'match_num'}, inplace=True)

    # TROPHEES
    tr = pd.read_excel(xl, sheet_name='🏆 TROPHÉES DE LA SAISON', header=None)
    trophees = tr.iloc[3:].dropna(subset=[0])
    trophees = trophees[[0, 1, 2, 3]].copy()
    trophees.columns = ['trophee', 'joueur', 'valeur', 'detail']
    trophees = trophees[trophees['trophee'].str.strip() != 'NaN'].dropna(how='all')

    # RIVALITES top 5
    riv = pd.read_excel(xl, sheet_name='RIVALITES', header=None)
    top_riv = riv.iloc[13:18, :3].copy()
    top_riv.columns = ['rank', 'paire', 'matchs']
    top_riv = top_riv.dropna(subset=['paire'])

    # POINTS (stats table)
    pts = pd.read_excel(xl, sheet_name='POINTS', header=0).dropna(subset=['Joueurs'])
    pts.columns = ['joueur', 'matchs_joues', 'victoires', 'defaites',
                   'vic_seches', 'vic_disputees', 'def_meritantes', 'def_seches',
                   'points', 'diff_jeux_tot', 'diff_jeux_match', 'cle']

    return cl, mt, sk, last_elo, elo_hist, trophees, top_riv, pts


cl, mt, sk, last_elo, elo_hist, trophees, top_riv, pts = load_data()

# Merge ELO into classement
cl = cl.merge(last_elo, on='joueur', how='left')

# ─── HEADER ────────────────────────────────────────────────────────────────────
last_match_date = mt['Date'].max().strftime('%d %b %Y') if not mt.empty else '—'
st.markdown(f"""
<div class="hero">
  <div class="hero-title">NEW PATH<br>TENNIS LEAGUE</div>
  <div class="hero-sub">Saison 2026 · {len(cl)} joueurs · {len(mt)} matchs</div>
  <div class="hero-badge">⚡ Dernière mise à jour : {last_match_date}</div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏆 CLASSEMENT", "🎾 MATCHS", "👤 JOUEURS", "⚔️ RIVALITÉS", "🥇 TROPHÉES", "📈 ELO"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CLASSEMENT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # Top 3 metrics
    top3 = cl.head(3)
    col1, col2, col3 = st.columns(3)
    medals = ['🥇', '🥈', '🥉']
    cols = [col1, col2, col3]
    for i, (col, (_, row)) in enumerate(zip(cols, top3.iterrows())):
        with col:
            elo_val = int(row['elo']) if pd.notna(row.get('elo', None)) else '—'
            st.metric(
                label=f"{medals[i]} {row['joueur'].split()[0]}",
                value=f"{int(row['pts'])} pts",
                delta=f"ELO {elo_val}"
            )

    st.markdown('<div class="section-head">LEADERBOARD</div>', unsafe_allow_html=True)

    # Streak helper from last matches
    def get_streak(player, matchs_df, n=3):
        player_matches = matchs_df[
            (matchs_df['Joueur A'] == player) | (matchs_df['Joueur B'] == player)
        ].head(n)
        streak = ""
        for _, m in player_matches.iterrows():
            streak += "✅" if m['Vainqueur'] == player else "❌"
        return streak

    for _, row in cl.iterrows():
        rang = int(row['rang'])
        rank_class = "top1" if rang == 1 else ("top2" if rang == 2 else ("top3" if rang == 3 else ""))
        elo_val = int(row['elo']) if pd.notna(row.get('elo', None)) else '—'
        ratio_pct = f"{row['ratio']*100:.0f}%"
        niveau = int(row['niveau']) if pd.notna(row['niveau']) else '—'
        streak = get_streak(row['joueur'], mt, 3)

        st.markdown(f"""
        <div class="rank-row">
            <div class="rank-num {rank_class}">{rang}</div>
            <div class="rank-name">{row['joueur']}</div>
            <div class="streak-badge">{streak}</div>
            <div class="rank-level">LV{niveau}</div>
            <div class="rank-elo">ELO {elo_val}</div>
            <div class="rank-pts">{int(row['pts'])}</div>
        </div>
        """, unsafe_allow_html=True)

    # Mini stats table
    st.markdown('<div class="section-head">STATISTIQUES</div>', unsafe_allow_html=True)

    stats_display = cl[['joueur', 'matchs', 'victoires', 'ratio', 'diff_jeux']].copy()
    stats_display.columns = ['Joueur', 'Matchs', 'Victoires', 'W%', 'Diff J/M']
    stats_display['W%'] = (stats_display['W%'] * 100).round(1).astype(str) + '%'
    stats_display['Diff J/M'] = stats_display['Diff J/M'].round(2)
    stats_display = stats_display.reset_index(drop=True)

    st.dataframe(
        stats_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Joueur": st.column_config.TextColumn(width="medium"),
            "Matchs": st.column_config.NumberColumn(width="small"),
            "Victoires": st.column_config.NumberColumn(width="small"),
            "W%": st.column_config.TextColumn(width="small"),
            "Diff J/M": st.column_config.NumberColumn(width="small", format="%.2f"),
        }
    )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MATCHS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    all_players = sorted(list(set(mt['Joueur A'].dropna().tolist() + mt['Joueur B'].dropna().tolist())))

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_player = st.selectbox("Filtrer par joueur", ["Tous"] + all_players, key="match_filter")
    with col_f2:
        show_n = st.selectbox("Afficher", [10, 20, 50, 100], index=0, key="match_n")

    mt_filtered = mt.copy()
    if filter_player != "Tous":
        mt_filtered = mt_filtered[
            (mt_filtered['Joueur A'] == filter_player) | (mt_filtered['Joueur B'] == filter_player)
        ]

    mt_show = mt_filtered.head(show_n)

    st.markdown(f'<div class="section-head">{len(mt_filtered)} MATCHS</div>', unsafe_allow_html=True)

    for _, m in mt_show.iterrows():
        date_str = m['Date'].strftime('%d/%m') if pd.notna(m['Date']) else '—'
        winner = str(m['Vainqueur'])
        player_a = str(m['Joueur A'])
        player_b = str(m['Joueur B'])
        result = str(m['Résultat (A-B)']) if pd.notna(m['Résultat (A-B)']) else '?'
        bonus = int(m['Bonus ⚡ (0/5)']) if pd.notna(m['Bonus ⚡ (0/5)']) else 0

        # Build score string
        sets = []
        for s in [('Set1 A', 'Set1 B'), ('Set2 A', 'Set2 B'), ('Set3 A', 'Set3 B')]:
            if pd.notna(m.get(s[0])) and pd.notna(m.get(s[1])):
                sets.append(f"{int(m[s[0]])}-{int(m[s[1]])}")
        score_str = " / ".join(sets)

        a_style = "match-winner" if player_a == winner else "match-loser"
        b_style = "match-winner" if player_b == winner else "match-loser"
        bonus_html = f'<div class="match-bonus">⚡{bonus}</div>' if bonus > 0 else ''

        st.markdown(f"""
        <div class="match-row">
            <div class="match-date">{date_str}</div>
            <div class="{a_style}" style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:0.8rem">{player_a}</div>
            <div style="color:var(--muted);font-size:0.7rem;flex-shrink:0">vs</div>
            <div class="{b_style}" style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:0.8rem">{player_b}</div>
            <div class="match-score">{score_str}</div>
            {bonus_html}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — JOUEURS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    players_list = sk['joueur'].tolist()
    selected_player = st.selectbox("Choisir un joueur", players_list, key="player_select")

    player_data = sk[sk['joueur'] == selected_player].iloc[0]
    player_cl = cl[cl['joueur'] == selected_player]
    player_pts_row = pts[pts['joueur'] == selected_player] if not pts.empty else pd.DataFrame()

    # Header
    rang_str = f"#{int(player_cl.iloc[0]['rang'])}" if not player_cl.empty else "—"
    pts_str = f"{int(player_cl.iloc[0]['pts'])}" if not player_cl.empty else "—"
    elo_str = f"{int(player_cl.iloc[0]['elo'])}" if not player_cl.empty and pd.notna(player_cl.iloc[0].get('elo')) else "—"
    niveau_str = f"LV{int(player_cl.iloc[0]['niveau'])}" if not player_cl.empty else "—"

    st.markdown(f"""
    <div class="profile-header">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div class="profile-name">{selected_player}</div>
                <div style="display:flex;gap:0.5rem;margin-top:0.4rem;flex-wrap:wrap">
                    <span class="chip green">{rang_str}</span>
                    <span class="chip green">{pts_str} pts</span>
                    <span class="chip green">ELO {elo_str}</span>
                    <span class="chip">{niveau_str}</span>
                    <span class="chip">{player_data.get('age', '?')} ans</span>
                    <span class="chip">{player_data.get('taille', '?')}</span>
                    <span class="chip">{'🫲' if str(player_data.get('main','')).lower() == 'gauche' else '🫱'} {player_data.get('main', '?')}</span>
                </div>
            </div>
        </div>
        <div class="profile-desc">"{player_data.get('description', '')}"</div>
    </div>
    """, unsafe_allow_html=True)

    col_s, col_r = st.columns([1, 1])

    with col_s:
        st.markdown('<div class="section-head">SKILLS</div>', unsafe_allow_html=True)
        skills = [
            ('Service', player_data['service']),
            ('Coup droit', player_data['coup_droit']),
            ('Revers', player_data['revers']),
            ('Vitesse', player_data['vitesse']),
            ('Mental', player_data['mental']),
            ('Défense', player_data['defense']),
            ('Agressivité', player_data['agressivite']),
            ('Physique', player_data['physique']),
            ('Technique', player_data['technique']),
        ]
        for skill_name, val in skills:
            try:
                v = int(val)
            except:
                v = 0
            pct = v * 10
            color = '#c8f135' if v >= 7 else ('#f5c542' if v >= 5 else '#ff3b30')
            st.markdown(f"""
            <div class="skill-row">
                <div class="skill-label">{skill_name}</div>
                <div class="skill-bar-bg">
                    <div class="skill-bar-fill" style="width:{pct}%;background:{color}"></div>
                </div>
                <div class="skill-val">{v}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-head">STATS SAISON</div>', unsafe_allow_html=True)
        if not player_pts_row.empty:
            r = player_pts_row.iloc[0]
            st.markdown(f"""
            <div class="card">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem">
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Matchs</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:var(--lime)">{int(r['matchs_joues'])}</div></div>
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Victoires</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:var(--lime)">{int(r['victoires'])}</div></div>
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Vic. nettes</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:#f5c542">{int(r['vic_seches'])}</div></div>
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Vic. 2-1</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:#f5c542">{int(r['vic_disputees'])}</div></div>
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Défaites</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:var(--red)">{int(r['defaites'])}</div></div>
                    <div><div style="font-size:0.65rem;color:var(--muted);text-transform:uppercase">Diff jeux</div><div style="font-family:'Bebas Neue';font-size:1.4rem;color:{'var(--lime)' if r['diff_jeux_tot']>=0 else 'var(--red)'}">{"+" if r['diff_jeux_tot']>0 else ""}{int(r['diff_jeux_tot'])}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Radar chart
        st.markdown('<div class="section-head">RADAR</div>', unsafe_allow_html=True)
        skill_names = ['Service', 'Coup droit', 'Revers', 'Vitesse', 'Mental', 'Défense', 'Agressivité', 'Physique', 'Technique']
        skill_vals = [int(player_data[k.lower().replace(' ', '_').replace('é', 'e').replace('è', 'e')]) 
                      for k in ['service', 'coup_droit', 'revers', 'vitesse', 'mental', 'defense', 'agressivite', 'physique', 'technique']]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=skill_vals + [skill_vals[0]],
            theta=skill_names + [skill_names[0]],
            fill='toself',
            fillcolor='rgba(200,241,53,0.15)',
            line=dict(color='#c8f135', width=2),
            name=selected_player
        ))
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 10], gridcolor='#2a3f2a', tickfont=dict(color='#6b8c6b', size=9)),
                angularaxis=dict(gridcolor='#2a3f2a', tickfont=dict(color='#f0f4f0', size=10))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20),
            height=230,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Recent matches
    st.markdown('<div class="section-head">DERNIERS MATCHS</div>', unsafe_allow_html=True)
    p_matches = mt[
        (mt['Joueur A'] == selected_player) | (mt['Joueur B'] == selected_player)
    ].head(8)

    for _, m in p_matches.iterrows():
        date_str = m['Date'].strftime('%d/%m/%y') if pd.notna(m['Date']) else '—'
        opponent = m['Joueur B'] if m['Joueur A'] == selected_player else m['Joueur A']
        won = m['Vainqueur'] == selected_player
        result_icon = "✅" if won else "❌"
        result_txt = "VICTOIRE" if won else "DÉFAITE"
        result_color = "var(--lime)" if won else "var(--red)"

        sets = []
        for s in [('Set1 A', 'Set1 B'), ('Set2 A', 'Set2 B'), ('Set3 A', 'Set3 B')]:
            if pd.notna(m.get(s[0])) and pd.notna(m.get(s[1])):
                sets.append(f"{int(m[s[0]])}-{int(m[s[1]])}")
        score_str = " / ".join(sets)

        st.markdown(f"""
        <div class="match-row">
            <div>{result_icon}</div>
            <div class="match-date">{date_str}</div>
            <div style="flex:1;font-size:0.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{opponent}</div>
            <div class="match-score">{score_str}</div>
            <div style="font-size:0.65rem;font-weight:600;color:{result_color};flex-shrink:0">{result_txt}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — RIVALITÉS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-head">🔥 TOP 5 RIVALITÉS</div>', unsafe_allow_html=True)

    for _, r in top_riv.iterrows():
        st.markdown(f"""
        <div class="rivalry-row">
            <div style="font-family:'Bebas Neue';font-size:1.2rem;color:var(--muted);width:1.5rem">{int(r['rank'])}</div>
            <div style="flex:1;font-weight:600">{r['paire']}</div>
            <div style="font-family:'JetBrains Mono';font-size:0.75rem;color:var(--lime)">{int(r['matchs'])} matchs</div>
        </div>
        """, unsafe_allow_html=True)

    # H2H tool
    st.markdown('<div class="section-head">HEAD-TO-HEAD</div>', unsafe_allow_html=True)
    all_pl = sorted(cl['joueur'].tolist())
    h2h_col1, h2h_col2 = st.columns(2)
    with h2h_col1:
        p1 = st.selectbox("Joueur 1", all_pl, key="h2h_p1")
    with h2h_col2:
        p2 = st.selectbox("Joueur 2", [p for p in all_pl if p != p1], key="h2h_p2")

    h2h_matches = mt[
        ((mt['Joueur A'] == p1) & (mt['Joueur B'] == p2)) |
        ((mt['Joueur A'] == p2) & (mt['Joueur B'] == p1))
    ]

    p1_wins = (h2h_matches['Vainqueur'] == p1).sum()
    p2_wins = (h2h_matches['Vainqueur'] == p2).sum()
    total = len(h2h_matches)

    if total > 0:
        st.markdown(f"""
        <div class="card card-accent">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem">
                <div style="text-align:center;flex:1">
                    <div style="font-family:'Bebas Neue';font-size:2rem;color:var(--lime)">{p1_wins}</div>
                    <div style="font-size:0.7rem;color:var(--muted)">{p1.split()[0]}</div>
                </div>
                <div style="text-align:center;padding:0 1rem">
                    <div style="font-family:'JetBrains Mono';font-size:0.75rem;color:var(--muted)">{total} matchs</div>
                    <div style="font-size:0.8rem;color:var(--white);margin-top:0.2rem">vs</div>
                </div>
                <div style="text-align:center;flex:1">
                    <div style="font-family:'Bebas Neue';font-size:2rem;color:var(--lime)">{p2_wins}</div>
                    <div style="font-size:0.7rem;color:var(--muted)">{p2.split()[0]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for _, m in h2h_matches.sort_values('Date', ascending=False).iterrows():
            date_str = m['Date'].strftime('%d/%m/%y') if pd.notna(m['Date']) else '—'
            winner = str(m['Vainqueur'])
            sets = []
            for s in [('Set1 A', 'Set1 B'), ('Set2 A', 'Set2 B'), ('Set3 A', 'Set3 B')]:
                if pd.notna(m.get(s[0])) and pd.notna(m.get(s[1])):
                    sets.append(f"{int(m[s[0]])}-{int(m[s[1]])}")
            score_str = " / ".join(sets)

            a_style = "match-winner" if m['Joueur A'] == winner else "match-loser"
            b_style = "match-winner" if m['Joueur B'] == winner else "match-loser"
            st.markdown(f"""
            <div class="match-row">
                <div class="match-date">{date_str}</div>
                <div class="{a_style}" style="flex:1;font-size:0.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{m['Joueur A']}</div>
                <div style="color:var(--muted);font-size:0.7rem;flex-shrink:0">vs</div>
                <div class="{b_style}" style="flex:1;font-size:0.8rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{m['Joueur B']}</div>
                <div class="match-score">{score_str}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="card"><div style="color:var(--muted);font-size:0.85rem">Aucun match entre ces deux joueurs pour l\'instant.</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — TROPHÉES
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-head">🏆 PALMARÈS DE LA SAISON</div>', unsafe_allow_html=True)

    for _, t in trophees.iterrows():
        trophy_name = str(t['trophee']).strip()
        trophy_player = str(t['joueur']).strip() if pd.notna(t['joueur']) else '—'
        trophy_val = str(t['valeur']).strip() if pd.notna(t['valeur']) else ''
        trophy_detail = str(t['detail']).strip() if pd.notna(t['detail']) else ''

        if trophy_name in ['NaN', 'nan', ''] or not trophy_name:
            continue

        val_display = f" · {trophy_val}" if trophy_val and trophy_val not in ['—', 'NaN', 'nan'] else ''
        player_display = f"<div class='trophy-winner'>{trophy_player}{val_display}</div>" if trophy_player != '—' else ''

        st.markdown(f"""
        <div class="trophy-row">
            <div class="trophy-info">
                <div class="trophy-name">{trophy_name}</div>
                {player_display}
                <div class="trophy-detail">{trophy_detail}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — ELO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-head">CLASSEMENT ELO</div>', unsafe_allow_html=True)

    elo_sorted = last_elo.sort_values('elo', ascending=False).reset_index(drop=True)

    for i, row in elo_sorted.iterrows():
        elo_val = int(row['elo'])
        bar_width = max(10, (elo_val - 1200) / (1700 - 1200) * 100)
        color = '#c8f135' if elo_val >= 1550 else ('#f5c542' if elo_val >= 1450 else '#6b8c6b')
        st.markdown(f"""
        <div class="rank-row">
            <div class="rank-num">{i+1}</div>
            <div class="rank-name">{row['joueur']}</div>
            <div style="flex:1;height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                <div style="width:{bar_width:.0f}%;height:100%;background:{color};border-radius:3px"></div>
            </div>
            <div style="font-family:'JetBrains Mono';font-size:0.9rem;color:{color};font-weight:600;flex-shrink:0;width:3rem;text-align:right">{elo_val}</div>
        </div>
        """, unsafe_allow_html=True)

    # ELO evolution chart
    st.markdown('<div class="section-head">ÉVOLUTION ELO</div>', unsafe_allow_html=True)

    elo_raw = pd.read_excel("NEWPATH_TENNIS_LEAGUE_2026.xlsx", sheet_name='ELO_LOG', header=1)
    elo_raw = elo_raw[['Joueur clean', 'ELO après num', 'Occurrence joueur']].dropna(subset=['Joueur clean', 'ELO après num'])
    elo_raw.columns = ['joueur', 'elo', 'occurrence']

    selected_elo_players = st.multiselect(
        "Joueurs à afficher",
        options=sorted(elo_raw['joueur'].unique().tolist()),
        default=sorted(elo_raw['joueur'].unique().tolist())[:4],
        key="elo_multi"
    )

    if selected_elo_players:
        fig2 = go.Figure()
        colors_palette = ['#c8f135', '#f5c542', '#ff3b30', '#4fc3f7', '#ce93d8', '#80cbc4', '#ffb74d', '#e57373', '#aed581', '#4dd0e1']
        for idx, player in enumerate(selected_elo_players):
            player_elo = elo_raw[elo_raw['joueur'] == player].sort_values('occurrence')
            fig2.add_trace(go.Scatter(
                x=player_elo['occurrence'],
                y=player_elo['elo'],
                mode='lines',
                name=player.split()[0],
                line=dict(color=colors_palette[idx % len(colors_palette)], width=2),
                hovertemplate=f"<b>{player}</b><br>Match %{{x}}<br>ELO: %{{y}}<extra></extra>"
            ))

        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(17,31,17,0.8)',
            font=dict(color='#f0f4f0', family='Inter'),
            xaxis=dict(
                gridcolor='#2a3f2a', title='Matchs joués',
                title_font=dict(size=10), tickfont=dict(size=9),
                showgrid=True,
            ),
            yaxis=dict(
                gridcolor='#2a3f2a', title='ELO',
                title_font=dict(size=10), tickfont=dict(size=9),
                showgrid=True,
            ),
            legend=dict(
                bgcolor='rgba(17,31,17,0.9)', bordercolor='#2a3f2a', borderwidth=1,
                font=dict(size=10), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
            ),
            margin=dict(l=40, r=10, t=30, b=40),
            height=320,
            hovermode='x unified',
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
