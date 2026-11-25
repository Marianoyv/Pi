# Pi Finance

Producto financiero integrado en Pi Development bajo `/finance/`, con HTML, CSS y JavaScript estáticos y 18 calculadoras:

- `IPC` (mensual) — inflación (INDEC).
- `ICL` (diario) — índice para contratos de locación (BCRA).
- Cuotas o contado, cancelación de deudas y sueldo real.
- Comparador de plazos fijos, crédito UVA y monotributo.
- Intereses, préstamos, tasas, porcentajes, IVA y rentabilidad.

## Estructura

- Home: `index.html`, `home.js`
- IPC: `ipc/`
- ICL: `icl/`
- Estilos y componentes compartidos: `shared/`

## Datos oficiales

Las calculadoras leen archivos JSON estáticos publicados junto con el sitio:

- `ipc/data/ipc.json`
- `icl/data/icl.json`
- `credito-uva/data/uva.json`
- `comparador-plazos-fijos/data/plazos-fijos.json`
- `monotributo/data/categorias.json`

Desde la raíz del repositorio se pueden actualizar manualmente con:

```sh
node pi_finance/scripts/update-data.mjs
```

El sincronizador consulta BCRA y ARCA, valida las respuestas y no sobrescribe los archivos si una fuente parece incompleta.

## Integración

`export_static` copia esta fuente saneada a `dist/finance/`. Pi Development conserva su catálogo de productos, páginas y diseño; Pi Finance funciona como un producto vertical con navegación propia y una salida de regreso a la marca principal.

Las pruebas se ejecutan con:

```sh
node pi_finance/scripts/test-calculators.mjs
```
