# SADIT v1.2 - Documentación de Arquitectura Modular (MVP)

## 1. Validación de Modelo MVP (Producto Mínimo Viable)
La arquitectura actual ha sido diseñada específicamente para soportar un **MVP Clínico Escalable**. Cumple con los requisitos críticos sin sobre-ingeniería:

*   **Core de Valor:** El motor de inferencia (Bayesiano + ALICIA) está centralizado y desacoplado, permitiendo iteraciones rápidas en la lógica médica sin romper la API.
*   **Compliance desde el Día 0:** Al implementar *Schema Isolation* (Multi-Tenant) desde el inicio, se evita una refactorización dolorosa y costosa cuando se requiera certificación HIPAA/GDPR.
*   **Cost-Effective:** Utiliza contenedores ligeros (Python Slim + Alpine Postgres) que pueden correr en un servidor de $5/mes o escalar a Kubernetes.

## 2. Estrategia de Modularidad
El sistema es **Modular por Diseño** en todos los niveles:

### A. Backend (micro-kernel pattern)
*   **API Routers:** `src/api/` contiene módulos aislados (`auth.py`, `inference.py`). Agregar un módulo de `billing.py` o `patients.py` es tan simple como crear el archivo y registrarlo en `main.py`.
*   **Business Logic:** La lógica médica (`src/sadit/`) es independiente del framework web. Puede ser extraída a una CLI o una función Lambda sin cambios.
*   **Database:** El uso de SQLAlchemy permite cambiar de PostgreSQL a SQLite (dev) o Aurora (prod) solo cambiando la URL de conexión.

### B. Frontend (Component-Based)
*   **React + Vite:** La UI está construida con componentes atómicos. El `Dashboard` es un contenedor que orquesta sub-componentes (`ClinicalForm`, `ResultsPanel`).
*   **Atomic Design:** Se pueden agregar "Widgets" médicos nuevos (ej. Visor DICOM) sin afectar el resto de la aplicación.

### C. Infraestructura (Docker Services)
*   **Desacoplamiento:** La base de datos y el núcleo de aplicación son servicios separados.
*   **Evolución a Microservicios:** Si el módulo de Visión por Computadora crece mucho, puede moverse a su propio contenedor con GPU, comunicándose vía HTTP con el núcleo, sin reescribir todo el sistema.

## 3. Hoja de Ruta Tecnológica (Roadmap to v2.0)
Esta arquitectura soporta las siguientes expansiones sin deuda técnica significativa:

1.  **Fase SaaS (v1.3):** Integrar Stripe/PayPal para gestión de suscripciones (nuevo Router + Tabla Public).
2.  **Fase Hospitalaria (v1.5):** Integrar PACS/DICOM (nuevo Servicio Docker).
3.  **Fase Mobile (v2.0):** Crear App React Native consumiendo la **misma API** actual (Reutilización 100% del Backend).

## 4. Conclusión
**Sí, la arquitectura es compatible y robusta.** Está diseñada para crecer horizontalmente (más clientes) y verticalmente (más funcionalidades médicas) manteniendo la seguridad y el orden.
