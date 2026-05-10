# IBEX 35 — Dashboard Web Financiero

Dashboard web interactivo con datos financieros en tiempo real de las 35 empresas del IBEX 35.

🔗 **Demo en vivo:** https://ibex35-dashboard-web-sjylyzhrzxwvyqzmb4xbhi.streamlit.app/

## Herramientas
- Python (yfinance, pandas, plotly, streamlit)
- Streamlit Cloud (despliegue gratuito)

## Funcionalidades
- Market Cap — ranking y distribución por sector
- Márgenes — comparativa bruto y neto por empresa y sector
- Fundamentales — mapa PER vs ROE, tabla filtrable por sector
- Histórico — evolución del precio de cualquier empresa hasta 5 años

## Datos
Los datos se actualizan automáticamente cada hora via Yahoo Finance.

## Ejecutar en local
```bash
pip install -r requirements.txt
streamlit run app.py
```
