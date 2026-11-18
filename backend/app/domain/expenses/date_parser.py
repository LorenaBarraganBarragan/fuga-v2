"""
date_parser.py — Extracción determinista de fechas para FUGA+

Reglas (RN-INT-04 / D-04):
  - Formas aceptadas: "hoy", "ayer", "YYYY-MM-DD", "DD/MM", "DD/MM/YYYY",
    "DD de <mes>"
  - Zona horaria funcional: America/Bogota
  - Fecha mínima: 2020-01-01
  - Sin fechas futuras (la validación de "no futuro" se hace en FastAPI
    con la fecha del servidor; aquí se devuelve la fecha extraída más un aviso)
  - Sin coincidencia → fecha local actual con aviso de baja confianza
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from zoneinfo import ZoneInfo

ZONA = ZoneInfo("America/Bogota")
FECHA_MINIMA = date(2020, 1, 1)

MESES_ES: dict[str, int] = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
    "ene": 1,
    "feb": 2,
    "mar": 3,
    "abr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dic": 12,
}


@dataclass(frozen=True)
class FechaResultado:
    fecha: date
    confianza: str  # "alta" | "media" | "baja"
    avisos: list[str]


def _hoy_bogota() -> date:
    """Retorna la fecha actual en la zona America/Bogota."""
    from datetime import datetime

    return datetime.now(tz=ZONA).date()


def _es_fecha_valida(d: date) -> tuple[bool, list[str]]:
    """Valida que la fecha esté en [2020-01-01, hoy]."""
    avisos = []
    hoy = _hoy_bogota()
    if d < FECHA_MINIMA:
        avisos.append(f"La fecha {d} es anterior al mínimo permitido (2020-01-01).")
        return False, avisos
    if d > hoy:
        # Solo aviso; la validación de error se hace en FastAPI (no en el parser)
        avisos.append(
            f"La fecha {d} parece futura. Se usará la fecha proporcionada "
            "pero será rechazada por el servidor si es posterior a hoy."
        )
        return True, avisos  # Se devuelve con aviso, rechazo en API
    return True, avisos


def extraer_fecha(texto: str) -> FechaResultado:
    """
    Extrae la fecha de gasto del texto libre.

    >>> from datetime import date
    >>> # "hoy" retorna la fecha actual
    >>> r = extraer_fecha("Hoy gasté 8000 en taxi")
    >>> r.confianza
    'alta'
    >>> r.avisos
    []
    """
    hoy = _hoy_bogota()
    texto_low = texto.lower().strip()

    # 1. "hoy" / "el día de hoy"
    if re.search(r"\bhoy\b", texto_low):
        return FechaResultado(fecha=hoy, confianza="alta", avisos=[])

    # 2. "ayer"
    if re.search(r"\bayer\b", texto_low):
        ayer = hoy - timedelta(days=1)
        valida, avisos = _es_fecha_valida(ayer)
        return FechaResultado(fecha=ayer, confianza="alta", avisos=avisos)

    # 3. "mañana" → ignorar, usar hoy con aviso
    if re.search(r"\bma[ñn]ana\b", texto_low):
        return FechaResultado(
            fecha=hoy,
            confianza="media",
            avisos=["Fecha futura detectada en el texto ('mañana'). Se usó la fecha de hoy."],
        )

    # 4. YYYY-MM-DD
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", texto_low)
    if m:
        try:
            d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            valida, avisos = _es_fecha_valida(d)
            confianza = "alta" if valida and not avisos else "media"
            return FechaResultado(fecha=d, confianza=confianza, avisos=avisos)
        except ValueError:
            pass  # Fecha inválida (ej: mes 13); seguir buscando

    # 5. DD/MM/YYYY o DD/MM (año actual si se omite)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", texto_low)
    if m:
        try:
            dia = int(m.group(1))
            mes = int(m.group(2))
            year_raw = m.group(3)
            if year_raw is not None:
                anio = int(year_raw) if len(year_raw) == 4 else 2000 + int(year_raw)
            else:
                # Año actual; si resulta futuro, probar año anterior
                anio = hoy.year
            d = date(anio, mes, dia)
            if d > hoy and year_raw is None:
                d = date(anio - 1, mes, dia)
            valida, avisos = _es_fecha_valida(d)
            confianza = "alta" if valida and not avisos else "media"
            return FechaResultado(fecha=d, confianza=confianza, avisos=avisos)
        except ValueError:
            pass

    # 6. "DD de <mes>" / "el DD de <mes>"
    patron_mes = "|".join(MESES_ES.keys())
    m = re.search(rf"\b(\d{{1,2}})\s+de\s+({patron_mes})\b", texto_low)
    if m:
        try:
            dia = int(m.group(1))
            mes = MESES_ES[m.group(2)]
            # Año actual; si es futuro, probar año anterior
            anio = hoy.year
            d = date(anio, mes, dia)
            if d > hoy:
                d = date(anio - 1, mes, dia)
            valida, avisos = _es_fecha_valida(d)
            confianza = "alta" if valida and not avisos else "media"
            return FechaResultado(fecha=d, confianza=confianza, avisos=avisos)
        except ValueError:
            pass

    # 7. Sin coincidencia → hoy con aviso de baja confianza
    return FechaResultado(
        fecha=hoy,
        confianza="baja",
        avisos=["No se detectó una fecha en el texto. Se usó la fecha de hoy por defecto."],
    )
