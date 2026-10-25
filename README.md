## Integrantes

> **SEMILLA: 987**

- Persona A: Hernandez Castañeda Andre Alain
- Persona B: Rivera Vallejo Axel

## Tema

Tickets_Soporte

## Estructura del repositorio

```text
.
├── datos/
├── practica1/
│   ├── src/
│   └── resultados/
├── practica2/
│   ├── src/
│   └── resultados/
├── practica3/
│   ├── src/
│   └── resultados/
├── practica4/
│   ├── src/
│   └── resultados/
├── practica5/
│   ├── src/
│   └── resultados/
├── practica6/
│   ├── src/
│   └── resultados/
└── proyecto/
    ├── src/
    ├── resultados/
    └── datos/
```

# NOTAS DE CORRECCION

## Correccion solicitada:

LO PRIMERO QUE LES DIJE. CREEN EL .gitignore PORQUE VAN A SUBIR LOS AMBIENTES VIRTUALES.

AGREGA EL .gitignore PORQUE SUBISTE TODO EL AMBIENTE VIRTUAL.

SI SIGUE LA CARPETA .VENV CUANDO VUELVA A HACER PULL, LES VOY A BAJAR 1 PUNTO POR CADA DIA QUE SIGA AHI

## 2. Observaciones del repositorio

1- No tiene .gitignore
2- No tiene requirements.txt en la raiz del repo
3- No tiene la carpeta datos/
4- No tiene las carpetas practica1 a practica6
5- No tiene la carpeta proyecto/
6- Tiene el entorno virtual (mi-proyecto/.venv/) subido al repositorio; debe agregarse a .gitignore y eliminarse del control de versiones

## 3. Correcciones realizadas

**Fecha de corrección:** 19/09/2026  
**Hora:** 18:00 hrs.

Se realizaron las siguientes correcciones:

- Se añadió el archivo **`.gitignore`** al repositorio.
- Se verificó que el entorno virtual general del repositorio **no fuera subido**.
- El directorio `mi-proyecto/.venv/` corresponde a un **entorno virtual perteneciente a una subcarpeta de prueba**, y no al entorno virtual general del repositorio.
- El entorno virtual general del repositorio no fue subido debido a la protección automática de **GitHub**.
- Se verificó la configuración para evitar que este tipo de archivos vuelva a ser incluido en futuros commits.

- Añadidas las carpetas con un .gitkeep para que se pueda visualizar a la hora de clonar el repositorio.

### Estado

> **Corrección realizada y verificada al 19/09/2026 a las 18:00 hrs.**

El archivo `.gitignore` ha sido añadido y se tomarán las medidas necesarias para evitar que los entornos virtuales sean incluidos nuevamente en el control de versiones.

---

## Avisos

📦 **Aviso:** ya está disponible su dataset en `datos/` — `tickets_soporte-ruido_100.csv` (para pruebas rápidas) y `tickets_soporte-ruido_100000.csv` (el dataset real para sus prácticas). ¡Ya pueden empezar!

## Observaciones del profesor

### 22-sep-2026

**Estatus:** 5/6 de la estructura esperada.

Buen avance: ya completaron `src/` y `resultados/` en `practica2` a `practica6` (antes solo `practica1` estaba completa). Les falta terminar `proyecto/`: crear dentro las carpetas `src/`, `resultados/` y `datos/`.

### 23-sep-2026

**Estatus:** 6/6 de la estructura esperada.

¡Felicidades, completaron toda la estructura! Terminaron `proyecto/` con `datos/`, `resultados/` y `src/`.

📖 **Práctica 1 ya está disponible.** La encontrarán en `labs/P1/P1_setup_reconocimiento.md`, dentro del repositorio del profesor: https://github.com/ESCOMLCD/pcd202701/blob/main/labs/P1/P1_setup_reconocimiento.md — léanla completa antes de empezar a programar, ahí está todo lo que deben hacer, el formato exacto de `resumen.txt` y la fecha de entrega (mar 6-oct).

### 26-sep-2026

**Estatus:** 6/6 de la estructura esperada.

Siguen con la estructura completa, sin pendientes.

# Practicas

### Práctica 1 — evaluación (8-oct-2026, 00:51 h)

**Calificación: 100 / 100**

Entregada el **6-oct-2026 a las 19:02**, dentro del plazo (la entrega cerraba el mar 6-oct), así que no lleva penalización por retraso.

**Criterios cubiertos al 100%:** Estructura del monorepo (6/6); Nombres exactos de los entregables; Requisitos de Git (3+ commits, rama mergeada); Python puro (sin `csv` ni `pandas`, lectura con `open`); Formato del `resumen.txt` (encabezado y secciones); Encabezado: Archivo, Pareja, Seed; Dimensiones: filas, columnas, nombres; Primeras 5 filas (separadas con barra y espacios); Columna categórica (nombre, únicos, más frecuente); Columna numérica_1 (nombre, válidos, mín, máx); Calidad de datos (celdas vacías).

**Sin observaciones:** la entrega cumple con todo lo que pedía el enunciado. Buen trabajo.

**Desglose:**

| Criterio                                                | Obtenido | Máximo  |
| ------------------------------------------------------- | :------: | :-----: |
| Estructura del monorepo (6/6)                           |    8     |    8    |
| Nombres exactos de los entregables                      |    10    |   10    |
| Requisitos de Git (3+ commits, rama mergeada)           |    10    |   10    |
| Python puro (sin `csv` ni `pandas`, lectura con `open`) |    8     |    8    |
| Formato del `resumen.txt` (encabezado y secciones)      |    9     |    9    |
| Encabezado: Archivo, Pareja, Seed                       |    10    |   10    |
| Dimensiones: filas, columnas, nombres                   |    10    |   10    |
| Primeras 5 filas (separadas con barra y espacios)       |    5     |    5    |
| Columna categórica (nombre, únicos, más frecuente)      |    12    |   12    |
| Columna numérica_1 (nombre, válidos, mín, máx)          |    13    |   13    |
| Calidad de datos (celdas vacías)                        |    5     |    5    |
| **Total**                                               | **100**  | **100** |

### Práctica 2 — Procesamiento de datos con Python puro

Análisis del dataset completo (100,000 registros) usando solo la biblioteca estándar. El código utiliza funciones reutilizables y programación funcional (lambda, map, filter), sin csv, pandas, collections.Counter ni statistics.

El script practica2/src/analisis_python.py calcula:

los valores únicos y el conteo por categoría de categoria_problema;
la categoría más frecuente y el top 3;
el mínimo, el máximo, el promedio y la mediana de tiempo_resolucion_hrs y nivel_prioridad;
el promedio de tiempo_resolucion_hrs por categoría;
los registros por encima del percentil 90 de tiempo_resolucion_hrs.

Para ejecutarlo, desde la raíz del repositorio:

bash
python practica2/src/analisis_python.py

El resultado se guarda en practica2/resultados/analisis_python.json.

Observación: variantes de escritura en las categorías

Como solo aplicamos .strip(), sin unificar mayúsculas ni minúsculas, salieron 21 categorías en lugar de 7. Cada categoría real aparece escrita de tres formas: Cuenta, CUENTA y cuenta.

Esto afecta a promedio_por_categoria, porque una misma categoría queda partida en tres promedios distintos. Por ejemplo, Cuenta promedia 20.38 hrs, CUENTA 15.06 hrs y cuenta 17.01 hrs. Las variantes con pocos registros (unos 250–320 cada una) dan promedios más inestables que la forma principal (unos 13,500). Esto lo vamos a corregir en P4 y P5 con pandas.

También notamos valores fuera de rango en las columnas numéricas. Hay tiempos de resolución negativos (mínimo de -304 hrs) y niveles de prioridad de -50 y 600. Son ruido del dataset que todavía no se limpia en esta práctica.
