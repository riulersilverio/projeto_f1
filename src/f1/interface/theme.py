"""Identidade visual compartilhada pelas páginas: tema escuro, cores de equipe/pneu.

Centraliza a configuração de página, o template Plotly e os mapas de cor
usados pelos gráficos, para que o dashboard tenha uma aparência consistente
em vez de depender das paletas padrão do Streamlit/Plotly.
"""

from __future__ import annotations

import html

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
.f1-driver-card {
    background-color: #15151E;
    border: 1px solid #2A2A35;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.f1-avatar {
    border-radius: 50%;
    border-style: solid;
    border-width: 3px;
    object-fit: cover;
    display: block;
    margin: 0 auto 0.5rem;
}
.f1-avatar-fallback {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 0.5rem;
    font-weight: 700;
    color: #F5F5F5;
}
.f1-card-name {
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.f1-card-extra {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    opacity: 0.85;
}
.f1-team-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    border-style: solid;
    border-width: 1px;
    font-size: 0.75rem;
}
.f1-roster {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.f1-roster-chip {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 56px;
    font-size: 0.7rem;
    text-align: center;
}
.f1-roster-chip span {
    margin-top: 0.25rem;
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


def _avatar_html(driver: Driver | None, driver_number: int, color: str, size: int = 64) -> str:
    """HTML de um avatar circular: foto do piloto ou, na falta dela, a sigla.

    Args:
        driver: piloto correspondente, se conhecido.
        driver_number: usado como rótulo de fallback quando não há sigla.
        color: cor da borda (foto) ou do fundo (fallback), na cor da equipe.
        size: diâmetro do avatar em pixels.

    Returns:
        Fragmento HTML de uma `<img>` (foto) ou `<div>` (iniciais).
    """
    fallback_label = driver.name_acronym if driver and driver.name_acronym else str(driver_number)
    label = html.escape(fallback_label)
    if driver and driver.headshot_url:
        url = html.escape(driver.headshot_url)
        return (
            f'<img class="f1-avatar" src="{url}" alt="{label}" '
            f'style="width:{size}px;height:{size}px;border-color:{color}">'
        )
    return (
        f'<div class="f1-avatar-fallback" '
        f'style="width:{size}px;height:{size}px;border:3px solid {color};'
        f'background:{color}33;border-radius:50%">{label}</div>'
    )


def _driver_card_html(
    driver: Driver | None, driver_number: int, color: str, extra: str | None = None
) -> str:
    """HTML de um card de piloto: avatar, nome completo e badge de equipe."""
    name = html.escape(driver.full_name if driver and driver.full_name else str(driver_number))
    team = html.escape(driver.team_name if driver and driver.team_name else "—")
    extra_html = f'<div class="f1-card-extra">{html.escape(extra)}</div>' if extra else ""
    return (
        f'<div class="f1-driver-card">'
        f"{_avatar_html(driver, driver_number, color, size=72)}"
        f'<div class="f1-card-name">{name}</div>'
        f'<span class="f1-team-badge" style="border-color:{color};color:{color}">{team}</span>'
        f"{extra_html}"
        f"</div>"
    )


def _roster_html(drivers: list[Driver], color_map: dict[int, str]) -> str:
    """HTML de uma tira horizontal com avatar pequeno + sigla de cada piloto."""
    chips = []
    for driver in drivers:
        color = color_map.get(driver.driver_number, FALLBACK_DRIVER_COLOR)
        label = html.escape(driver.name_acronym or str(driver.driver_number))
        chips.append(
            '<div class="f1-roster-chip">'
            f"{_avatar_html(driver, driver.driver_number, color, size=40)}"
            f"<span>{label}</span>"
            "</div>"
        )
    return f'<div class="f1-roster">{"".join(chips)}</div>'


def driver_card(
    container: st.delta_generator.DeltaGenerator,
    driver: Driver | None,
    driver_number: int,
    color: str,
    extra: str | None = None,
) -> None:
    """Renderiza um card de piloto (avatar, nome e badge de equipe).

    Args:
        container: coluna/container Streamlit onde o card será desenhado.
        driver: piloto correspondente, se conhecido.
        driver_number: usado como rótulo de fallback quando `driver` é `None`.
        color: cor da equipe (ver `driver_color_map`).
        extra: linha adicional opcional (ex: posição na classificação).
    """
    container.markdown(
        _driver_card_html(driver, driver_number, color, extra), unsafe_allow_html=True
    )


def driver_roster(
    container: st.delta_generator.DeltaGenerator, drivers: list[Driver], color_map: dict[int, str]
) -> None:
    """Renderiza uma tira horizontal com o grid de pilotos da sessão.

    Pensado para páginas que listam muitos pilotos (até ~20), onde cards
    grandes com foto de cada um poluiriam a tela.

    Args:
        container: container Streamlit onde a tira será desenhada.
        drivers: pilotos a exibir.
        color_map: mapa `driver_number -> cor` (ver `driver_color_map`).
    """
    container.markdown(_roster_html(drivers, color_map), unsafe_allow_html=True)


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
