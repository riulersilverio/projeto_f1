"""Identidade visual compartilhada pelas páginas: tema escuro, cores de equipe/pneu.

Centraliza a configuração de página, o template Plotly e os mapas de cor
usados pelos gráficos, para que o dashboard tenha uma aparência consistente
em vez de depender das paletas padrão do Streamlit/Plotly.
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

from f1.domain.models import Driver

FALLBACK_DRIVER_COLOR = "#8E8E93"

TYRE_COMPOUND_COLORS: dict[str, str] = {
    "SOFT": "#DA291C",
    "MEDIUM": "#FFD400",
    "HARD": "#F5F5F5",
    "INTERMEDIATE": "#43B02A",
    "WET": "#0067AD",
}

_PLOTLY_TEMPLATE_NAME = "f1_dark"

pio.templates[_PLOTLY_TEMPLATE_NAME] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#15151E",
        plot_bgcolor="#15151E",
        font={"color": "#F5F5F5", "family": "sans-serif"},
        colorway=["#E10600", "#00D2BE", "#FFD400", "#43B02A", "#0067AD", "#8E8E93"],
        xaxis={"gridcolor": "#2A2A35", "zerolinecolor": "#2A2A35"},
        yaxis={"gridcolor": "#2A2A35", "zerolinecolor": "#2A2A35"},
        legend={"bgcolor": "rgba(0,0,0,0)"},
    )
)
pio.templates.default = _PLOTLY_TEMPLATE_NAME

_CSS = """
<style>
[data-testid="stMetric"] {
    background-color: #15151E;
    border: 1px solid #2A2A35;
    border-radius: 10px;
    padding: 1rem;
}
.f1-banner {
    background: linear-gradient(90deg, #E10600 0%, #15151E 85%);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.f1-banner h1 {
    margin: 0;
    font-size: 2rem;
    color: #F5F5F5;
}
.f1-banner p {
    margin: 0.25rem 0 0;
    color: #E8E8E8;
    opacity: 0.85;
}
</style>
"""


def _lighten(hex_color: str, factor: float) -> str:
    """Clareia uma cor hex misturando-a com branco na proporção `factor` (0-1)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(channel + (255 - channel) * factor) for channel in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def driver_color_map(drivers: list[Driver]) -> dict[int, str]:
    """Monta um mapa `driver_number -> cor` a partir da cor de equipe.

    A OpenF1 retorna a mesma `team_colour` para os dois pilotos de um time,
    então companheiros de equipe são progressivamente clareados para
    permanecerem distinguíveis nos gráficos.

    Args:
        drivers: pilotos participantes de uma sessão.

    Returns:
        Mapa pronto para ser usado como `color_discrete_map` do Plotly.
    """
    colors: dict[int, str] = {}
    seen_counts: dict[str, int] = {}
    for driver in drivers:
        raw = (driver.team_colour or "").strip().lstrip("#")
        base_color = f"#{raw}" if raw else FALLBACK_DRIVER_COLOR
        count = seen_counts.get(raw, 0)
        seen_counts[raw] = count + 1
        factor = min(count * 0.35, 0.8)
        colors[driver.driver_number] = _lighten(base_color, factor) if factor else base_color
    return colors


def configure_page(title: str, icon: str, subtitle: str | None = None) -> None:
    """Configura a página Streamlit com layout, tema escuro e banner padrão.

    Deve ser a primeira chamada Streamlit de cada página, substituindo
    `st.set_page_config` + `st.title` manuais.

    Args:
        title: título exibido no banner e na aba do navegador.
        icon: emoji usado como ícone da página e do banner.
        subtitle: texto opcional exibido abaixo do título no banner.
    """
    st.set_page_config(page_title=title, page_icon=icon, layout="wide")
    st.markdown(_CSS, unsafe_allow_html=True)
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="f1-banner"><h1>{icon} {title}</h1>{subtitle_html}</div>',
        unsafe_allow_html=True,
    )
