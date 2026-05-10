import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="IBEX 35 Dashboard",
    page_icon="📊",
    layout="wide"
)

IBEX35 = {
    "Acciona": "ANA.MC", "Acciona Energía": "ANE.MC",
    "Acerinox": "ACX.MC", "ACS": "ACS.MC", "AENA": "AENA.MC",
    "Amadeus": "AMS.MC", "ArcelorMittal": "MTS.MC",
    "Banco Sabadell": "SAB.MC", "Bankinter": "BKT.MC",
    "BBVA": "BBVA.MC", "CaixaBank": "CABK.MC", "Cellnex": "CLNX.MC",
    "Enagás": "ENG.MC", "Endesa": "ELE.MC", "Ferrovial": "FER.MC",
    "Fluidra": "FDR.MC", "Grifols": "GRF.MC", "IAG": "IAG.MC",
    "Iberdrola": "IBE.MC", "Inditex": "ITX.MC", "Indra": "IDR.MC",
    "Colonial": "COL.MC", "Logista": "LOG.MC", "Mapfre": "MAP.MC",
    "Meliá": "MEL.MC", "Merlin": "MRL.MC", "Naturgy": "NTGY.MC",
    "Redeia": "RED.MC", "Repsol": "REP.MC", "Rovi": "ROVI.MC",
    "Sacyr": "SCYR.MC", "Santander": "SAN.MC", "Solaria": "SLR.MC",
    "Telefónica": "TEF.MC", "Unicaja": "UNI.MC"
}

SECTORES = {
    "Acciona": "Utilities", "Acciona Energía": "Utilities",
    "Acerinox": "Materiales", "ACS": "Construcción", "AENA": "Transporte",
    "Amadeus": "Tecnología", "ArcelorMittal": "Materiales",
    "Banco Sabadell": "Banca", "Bankinter": "Banca",
    "BBVA": "Banca", "CaixaBank": "Banca", "Cellnex": "Telecomunicaciones",
    "Enagás": "Utilities", "Endesa": "Utilities", "Ferrovial": "Construcción",
    "Fluidra": "Industrial", "Grifols": "Salud", "IAG": "Transporte",
    "Iberdrola": "Utilities", "Inditex": "Consumo", "Indra": "Tecnología",
    "Colonial": "Inmobiliario", "Logista": "Logística", "Mapfre": "Seguros",
    "Meliá": "Turismo", "Merlin": "Inmobiliario", "Naturgy": "Utilities",
    "Redeia": "Utilities", "Repsol": "Energía", "Rovi": "Salud",
    "Sacyr": "Construcción", "Santander": "Banca", "Solaria": "Utilities",
    "Telefónica": "Telecomunicaciones", "Unicaja": "Banca"
}

@st.cache_data(ttl=3600)
def cargar_datos():
    resultados = []
    for nombre, ticker in IBEX35.items():
        try:
            info = yf.Ticker(ticker).info
            ingresos = info.get("totalRevenue", 0) or 0
            beneficio_bruto = info.get("grossProfits", 0) or 0
            beneficio_neto = info.get("netIncomeToCommon", 0) or 0
            ebitda = info.get("ebitda", 0) or 0
            market_cap = info.get("marketCap", 0) or 0
            deuda = info.get("totalDebt", 0) or 0
            per = info.get("trailingPE", 0) or 0
            roe = info.get("returnOnEquity", 0) or 0
            precio = info.get("currentPrice", 0) or 0
            margen_bruto = round(beneficio_bruto / ingresos * 100, 2) if ingresos else 0
            margen_neto = round(beneficio_neto / ingresos * 100, 2) if ingresos else 0
            deuda_ebitda = round(deuda / ebitda, 2) if ebitda else 0
            resultados.append({
                "Empresa": nombre, "Ticker": ticker,
                "Sector": SECTORES.get(nombre, "Otros"),
                "Precio (€)": round(precio, 2),
                "Market Cap (M€)": round(market_cap / 1e6, 2),
                "Ingresos (M€)": round(ingresos / 1e6, 2),
                "Margen Bruto %": margen_bruto,
                "Margen Neto %": margen_neto,
                "EBITDA (M€)": round(ebitda / 1e6, 2),
                "PER": round(per, 2),
                "ROE %": round(roe * 100, 2),
                "Deuda/EBITDA": deuda_ebitda
            })
        except:
            continue
    return pd.DataFrame(resultados)

@st.cache_data(ttl=3600)
def cargar_historico(ticker, periodo):
    datos = yf.Ticker(ticker).history(period=periodo)
    return datos["Close"]

# ── HEADER ──────────────────────────────────────────────
st.title("📊 IBEX 35 — Dashboard Financiero")
st.caption("Datos en tiempo real via Yahoo Finance")

with st.spinner("Cargando datos del IBEX 35..."):
    df = cargar_datos()

# ── KPIs ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Empresas analizadas", len(df))
col2.metric("Mayor Market Cap", df.loc[df["Market Cap (M€)"].idxmax(), "Empresa"])
col3.metric("Mejor Margen Neto", df.loc[df["Margen Neto %"].idxmax(), "Empresa"])
col4.metric("Mayor ROE", df.loc[df["ROE %"].idxmax(), "Empresa"])

st.divider()

# ── TABS ────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Cap", "💹 Márgenes", "🔍 Fundamentales", "📉 Histórico"])

with tab1:
    top_n = st.slider("Número de empresas", 5, 35, 15)
    top = df.nlargest(top_n, "Market Cap (M€)")
    fig = px.bar(top, x="Market Cap (M€)", y="Empresa", orientation="h",
                 color="Sector", title=f"Top {top_n} empresas por Market Cap")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(df.groupby("Sector")["Market Cap (M€)"].sum().reset_index(),
                  values="Market Cap (M€)", names="Sector",
                  title="Distribución del IBEX 35 por sector")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    df_valido = df[(df["Margen Bruto %"] > 0) & (df["Margen Neto %"].between(-50, 150))]
    fig = px.bar(df_valido.sort_values("Margen Bruto %", ascending=False),
                 x="Empresa", y=["Margen Bruto %", "Margen Neto %"],
                 barmode="group", title="Comparativa de márgenes por empresa",
                 color_discrete_map={"Margen Bruto %": "#00a0e0", "Margen Neto %": "#e31937"})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    sector_df = df.groupby("Sector")[["Margen Bruto %", "Margen Neto %"]].mean().reset_index()
    fig2 = px.bar(sector_df.sort_values("Margen Neto %", ascending=False),
                  x="Sector", y=["Margen Bruto %", "Margen Neto %"],
                  barmode="group", title="Márgenes medios por sector")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig = px.scatter(df[(df["PER"] > 0) & (df["PER"] < 60) & (df["ROE %"] > 0)],
                     x="PER", y="ROE %", size="Market Cap (M€)",
                     color="Sector", hover_name="Empresa",
                     title="PER vs ROE — Mapa de valoración IBEX 35")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tabla completa")
    sector_filtro = st.multiselect("Filtrar por sector", df["Sector"].unique(), default=df["Sector"].unique())
    df_filtrado = df[df["Sector"].isin(sector_filtro)]
    st.dataframe(df_filtrado.sort_values("Market Cap (M€)", ascending=False), use_container_width=True)

with tab4:
    empresa = st.selectbox("Selecciona empresa", df["Empresa"].tolist())
    periodo = st.radio("Período", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3, horizontal=True)
    ticker = IBEX35[empresa]
    
    with st.spinner(f"Cargando histórico de {empresa}..."):
        historico = cargar_historico(ticker, periodo)
    
    if not historico.empty:
        fig = px.line(historico, title=f"Evolución del precio — {empresa}",
                      labels={"value": "Precio (€)", "index": "Fecha"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos históricos disponibles")