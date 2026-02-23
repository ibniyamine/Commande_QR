import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import locale

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Analyse Commandes QR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design professionnel
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: white;
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    
    .kpi-title {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .kpi-change {
        font-size: 1rem;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        display: inline-block;
    }
    
    .positive {
        background-color: #28a745;
        color: white;
    }
    
    .negative {
        background-color: #dc3545;
        color: white;
    }
    
    .neutral {
        background-color: #6c757d;
        color: white;
    }
    
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Chargement et préparation des données
@st.cache_data
def load_data():
    df = pd.read_csv('Assurance_Commandes_QR.csv', sep=';', decimal='.')
    
    # Conversion des colonnes de date
    df['DateValidation'] = pd.to_datetime(df['DateValidation'], format='%d/%m/%Y', errors='coerce')
    df['DateCmde'] = pd.to_datetime(df['DateCmde'], format='%d/%m/%Y', errors='coerce')
    
    # Conversion des colonnes numériques
    df['NbQR'] = pd.to_numeric(df['NbQR'], errors='coerce')
    df['cmd_montant'] = pd.to_numeric(df['cmd_montant'], errors='coerce')
    
    # Suppression des lignes avec des valeurs manquantes critiques
    df = df.dropna(subset=['DateValidation', 'NbQR', 'cmd_montant'])
    
    # Ajout de colonnes temporelles
    df['Mois'] = df['DateValidation'].dt.month
    df['Annee'] = df['DateValidation'].dt.year
    df['MoisAnnee'] = df['DateValidation'].dt.to_period('M')
    
    return df

# Calcul des taux de variation
def calculate_variation(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Fonction pour créer des cartes KPI stylisées
def create_kpi_card(title, value, change, change_label=""):
    change_class = "positive" if change > 0 else "negative" if change < 0 else "neutral"
    change_symbol = "↑" if change > 0 else "↓" if change < 0 else "→"
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value:,.0f}</div>
        <div class="kpi-change {change_class}">
            {change_symbol} {abs(change):.1f}% {change_label}
        </div>
    </div>
    """

# Chargement des données
df = load_data()

# En-tête du dashboard
st.markdown('<h1 class="main-header">📊 Dashboard Analyse Commandes QR</h1>', unsafe_allow_html=True)

# Filtres principaux en haut de la page
st.markdown("### 📅 Filtres de période")
col1, col2 = st.columns(2)

with col1:
    date_min = df['DateValidation'].min().date()
    date_max = df['DateValidation'].max().date()
    date_debut = st.date_input("Date de début", date_min, min_value=date_min, max_value=date_max)

with col2:
    date_fin = st.date_input("Date de fin", date_max, min_value=date_min, max_value=date_max)

# Sidebar avec filtres supplémentaires
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown("### 🔍 Filtres avancés")

# Filtre par compagnie
compagnies_disponibles = ['Toutes'] + sorted(df['Compagnie'].unique())
compagnie_selectionnee = st.sidebar.selectbox("Compagnie", compagnies_disponibles)

# Filtre par mois
mois_disponibles = ['Tous'] + list(range(1, 13))
mois_selectionne = st.sidebar.selectbox("Mois", mois_disponibles, 
                                       format_func=lambda x: "Tous" if x == "Tous" else datetime(2024, x, 1).strftime("%B"))

# Filtre par année
annees_disponibles = ['Toutes'] + sorted(df['Annee'].unique())
annee_selectionnee = st.sidebar.selectbox("Année", annees_disponibles)

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Application des filtres
df_filtre = df.copy()

# Filtre de période
df_filtre = df_filtre[
    (df_filtre['DateValidation'] >= pd.to_datetime(date_debut)) &
    (df_filtre['DateValidation'] <= pd.to_datetime(date_fin))
]

# Filtres supplémentaires
if compagnie_selectionnee != 'Toutes':
    df_filtre = df_filtre[df_filtre['Compagnie'] == compagnie_selectionnee]

if mois_selectionne != 'Tous':
    df_filtre = df_filtre[df_filtre['Mois'] == mois_selectionne]

if annee_selectionnee != 'Toutes':
    df_filtre = df_filtre[df_filtre['Annee'] == annee_selectionnee]

# Calcul des KPI
total_qr = df_filtre['NbQR'].sum()
total_montant = df_filtre['cmd_montant'].sum()

# Calcul des variations mensuelles
if len(df_filtre) > 0:
    periodes = sorted(df_filtre['MoisAnnee'].unique())
    if len(periodes) >= 2:
        periode_actuelle = periodes[-1]
        periode_precedente = periodes[-2]
        
        donnees_actuelles = df_filtre[df_filtre['MoisAnnee'] == periode_actuelle]
        donnees_precedentes = df_filtre[df_filtre['MoisAnnee'] == periode_precedente]
        
        qr_mois_actuel = donnees_actuelles['NbQR'].sum()
        qr_mois_precedent = donnees_precedentes['NbQR'].sum()
        montant_mois_actuel = donnees_actuelles['cmd_montant'].sum()
        montant_mois_precedent = donnees_precedentes['cmd_montant'].sum()
        
        variation_qr_mensuel = calculate_variation(qr_mois_actuel, qr_mois_precedent)
        variation_montant_mensuel = calculate_variation(montant_mois_actuel, montant_mois_precedent)
    else:
        variation_qr_mensuel = 0
        variation_montant_mensuel = 0
    
    # Calcul des variations annuelles
    annees = sorted(df_filtre['Annee'].unique())
    if len(annees) >= 2:
        annee_actuelle = annees[-1]
        annee_precedente = annees[-2]
        
        donnees_annee_actuelle = df_filtre[df_filtre['Annee'] == annee_actuelle]
        donnees_annee_precedente = df_filtre[df_filtre['Annee'] == annee_precedente]
        
        qr_annee_actuelle = donnees_annee_actuelle['NbQR'].sum()
        qr_annee_precedente = donnees_annee_precedente['NbQR'].sum()
        montant_annee_actuelle = donnees_annee_actuelle['cmd_montant'].sum()
        montant_annee_precedente = donnees_annee_precedente['cmd_montant'].sum()
        
        variation_qr_annuel = calculate_variation(qr_annee_actuelle, qr_annee_precedente)
        variation_montant_annuel = calculate_variation(montant_annee_actuelle, montant_annee_precedente)
    else:
        variation_qr_annuel = 0
        variation_montant_annuel = 0
else:
    variation_qr_mensuel = variation_montant_mensuel = 0
    variation_qr_annuel = variation_montant_annuel = 0

# Affichage des KPI
st.markdown("## 📈 Indicateurs Clés de Performance")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(create_kpi_card("Total Commandes QR", total_qr, variation_qr_mensuel, "ce mois"), 
                unsafe_allow_html=True)

with col2:
    st.markdown(create_kpi_card("Montant Total", total_montant, variation_montant_mensuel, "ce mois"), 
                unsafe_allow_html=True)

with col3:
    st.markdown(create_kpi_card("Variation Mensuelle (%)", variation_montant_mensuel, variation_montant_mensuel, ""), 
                unsafe_allow_html=True)

with col4:
    st.markdown(create_kpi_card("Variation Annuelle (%)", variation_montant_annuel, variation_montant_annuel, ""), 
                unsafe_allow_html=True)

with col5:
    montant_global = df['cmd_montant'].sum()
    variation_globale = (total_montant / montant_global) * 100 if montant_global > 0 else 0
    st.markdown(
        create_kpi_card(
            "Part du Total Global (%)",
            variation_globale,
            variation_globale,
            ""
        ),
        unsafe_allow_html=True
    )


# Visualisations
st.markdown("## 📊 Visualisations Analytiques")

# Tableau récapitulatif par compagnie
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### Tableau récapitulatif par compagnie")

if len(df_filtre) > 0:
    recap_compagnie = df_filtre.groupby('Compagnie').agg({
        'NbQR': 'sum',
        'cmd_montant': 'sum'
    }).reset_index()
    recap_compagnie = recap_compagnie.sort_values('cmd_montant', ascending=False)
    recap_compagnie['cmd_montant'] = recap_compagnie['cmd_montant'].round(2)
    recap_compagnie.columns = ['Compagnie', 'Total QR', 'Montant Total (€)']
    
    st.dataframe(recap_compagnie, width='stretch', hide_index=True)
else:
    st.warning("Aucune donnée disponible pour les filtres sélectionnés")
st.markdown('</div>', unsafe_allow_html=True)

# Graphiques en ligne
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Histogramme des montants par compagnie")
    
    if len(df_filtre) > 0:
        fig_hist = px.bar(
            recap_compagnie.head(10),
            x='Compagnie',
            y='Montant Total (€)',
            title="Top 10 des compagnies par montant",
            color='Montant Total (€)',
            color_continuous_scale='viridis'
        )
        fig_hist.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_hist, width='stretch')
    else:
        st.warning("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Évolution mensuelle")
    
    if len(df_filtre) > 0:
        evolution_mensuelle = df_filtre.groupby('MoisAnnee').agg({
            'cmd_montant': 'sum',
            'NbQR': 'sum'
        }).reset_index()
        evolution_mensuelle['MoisAnnee'] = evolution_mensuelle['MoisAnnee'].astype(str)
        
        fig_evolution = px.line(
            evolution_mensuelle,
            x='MoisAnnee',
            y='cmd_montant',
            title="Évolution des montants mensuels",
            markers=True,
            line_shape='linear'
        )
        fig_evolution.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_evolution, width='stretch')
    else:
        st.warning("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)

# Graphiques en deuxième ligne
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Répartition des commandes QR par compagnie")
    
    if len(df_filtre) > 0:
        fig_pie_qr = px.pie(
            recap_compagnie.head(8),
            values='Total QR',
            names='Compagnie',
            title="Répartition des commandes QR"
        )
        st.plotly_chart(fig_pie_qr, width='stretch')
    else:
        st.warning("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("### Part de marché par montant")
    
    if len(df_filtre) > 0:
        recap_compagnie['Part de marché (%)'] = (recap_compagnie['Montant Total (€)'] / 
                                                 recap_compagnie['Montant Total (€)'].sum() * 100).round(2)
        
        fig_marche = px.bar(
            recap_compagnie.head(10),
            x='Compagnie',
            y='Part de marché (%)',
            title="Part de marché par compagnie",
            color='Part de marché (%)',
            color_continuous_scale='plasma'
        )
        fig_marche.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_marche, width='stretch')
    else:
        st.warning("Aucune donnée disponible")
    st.markdown('</div>', unsafe_allow_html=True)

# Tendance par compagnie
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown("### Tendance des montants par compagnie")

if len(df_filtre) > 0:
    tendance_compagnie = df_filtre.groupby(['MoisAnnee', 'Compagnie']).agg({
        'cmd_montant': 'sum'
    }).reset_index()
    tendance_compagnie['MoisAnnee'] = tendance_compagnie['MoisAnnee'].astype(str)
    
    # Top 5 des compagnies pour la lisibilité
    top_compagnies = recap_compagnie.head(5)['Compagnie'].tolist()
    tendance_top = tendance_compagnie[tendance_compagnie['Compagnie'].isin(top_compagnies)]
    
    fig_tendance = px.line(
        tendance_top,
        x='MoisAnnee',
        y='cmd_montant',
        color='Compagnie',
        title="Tendance des montants par compagnie (Top 5)",
        markers=True
    )
    fig_tendance.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_tendance, width='stretch')
else:
    st.warning("Aucune donnée disponible")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666; margin-top: 2rem;">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
