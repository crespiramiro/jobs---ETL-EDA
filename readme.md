# 🌍 Jobs – ETL Pipeline & Analysis

A complete ETL pipeline to extract, clean, and analyze remote job listings for IT & non IT roles across regions.

1. Introduction
This project implements an ETL pipeline to collect, clean, and analyze remote job listings from two public APIs (Jobicy and Remotive). It targets data science and engineering roles and focuses on geographical diversity.
2. Objectives
- Create a modular ETL system.
- Enrich data by combining multiple sources.
- Apply data cleaning and imputation techniques.
- Store structured data in PostgreSQL.
- Enable analysis and visualization in R and Tableau.
1. ETL Pipeline Description
- **Extraction**: Job data is retrieved using `requests` from the two APIs and saved as CSV files.
- **Transformation**:
    - Columns were cleaned and standardized.
    - Missing salary values were imputed using PMM (Predictive Mean Matching), implemented via `IterativeImputer` and `RandomForestRegressor` from `sklearn`. This method was chosen for its ability to preserve realistic value distributions.
    - I made sure that the imputation did not distort the original data distribution by using **boxplots and histograms** to compare salary distributions **before and after imputation**.
    - Data was grouped and labeled by region, seniority, and title.
    - Duplicate handling ensured unique jobs per company and title.
- **Loading**: The cleaned dataset is loaded into a PostgreSQL database under the schema `jobs.all_jobs`.
1. Analysis and Visualization Tools
- **R** was used for exploratory data analysis and potential modeling.
1. Key Decisions and Rationale
- Combining Jobicy and Remotive ensures broader coverage of global job markets.
- Imputing salaries instead of deleting rows prevents bias and loss of information.
- Splitting data by region, title, and seniority allows finer granularity in analysis.

---

[ESPAÑOL]

1. Introducción
Este proyecto implementa un pipeline ETL para recopilar, limpiar y analizar ofertas de empleo remoto desde dos APIs públicas (Jobicy y Remotive). Está orientado a roles en ciencia y análisis de datos, con énfasis en diversidad geográfica.
2. Objetivos
- Crear un sistema ETL modular.
- Enriquecer datos combinando múltiples fuentes.
- Aplicar técnicas de limpieza e imputación.
- Almacenar datos estructurados en PostgreSQL.
- Habilitar el análisis y visualización en R y Tableau.
1. Descripción del Pipeline
- **Extracción**: Los datos se obtienen mediante `requests` desde ambas APIs y se guardan en CSV.
- **Transformación**:
    - Se limpian y estandarizan las columnas.
    - Se imputan salarios faltantes usando PMM (Predictive Mean Matching), con `IterativeImputer` y `RandomForestRegressor`. Este método preserva la distribución realista de los valores.
    - Me aseguré de que la imputación no distorsionara la distribución original de los datos mediante **gráficos de boxplot e histogramas** que comparan los salarios **antes y después de la imputación**.
    - Se agrupan datos por región, seniority y título.
    - Se controlan duplicados por empresa y título.
- **Carga**: El dataset limpio se carga a una base de datos PostgreSQL bajo el esquema `jobs.all_jobs`.
1. Herramientas de Análisis y Visualización
- **R** para análisis estadístico exploratorio y modelado.
1. Decisiones Clave
- Usar dos fuentes garantiza cobertura más amplia.
- Imputar en lugar de eliminar evita sesgos.
- Separar por región, título y seniority mejora la granularidad del análisis.