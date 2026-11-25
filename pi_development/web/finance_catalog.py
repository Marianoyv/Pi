"""Public Pi Finance route inventory shared by sitemaps and release checks."""


FINANCE_PAGE_PATHS = (
    "",
    "ipc",
    "icl",
    "cuotas-o-contado",
    "cancelar-deudas",
    "sueldo-real",
    "comparador-plazos-fijos",
    "credito-uva",
    "monotributo",
    "interes-simple",
    "interes-compuesto",
    "plazo-fijo",
    "prestamo-sistema-frances",
    "tna-tea",
    "porcentaje-aumento",
    "porcentaje-descuento",
    "variacion-porcentual",
    "iva",
    "rentabilidad-inversion",
    "metodologia",
    "fuentes",
    "aviso-legal",
)


def get_finance_routes():
    return ["/finance/" if not path else f"/finance/{path}/" for path in FINANCE_PAGE_PATHS]
