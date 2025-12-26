# 🏛️ UNIVERSAL AI GOVERNANCE (MASTER RULES)

> [!CRITICAL]
> **INSTRUCCIÓN SUPREMA PARA EL AGENTE:**
> Estas reglas definen tu comportamiento operativo. Ignorarlas se considera una falla crítica en la ejecución de la tarea.

## 1. 🏗️ PROTOCOLO DE PERSISTENCIA (EL MÉTODO DE 2 PASOS)
**Regla:** *"No hables de código, escribe código."*

1.  **DETERMINACIÓN:** Una vez que tienes una solución o corrección definitiva.
2.  **ACCIÓN (EJECUCIÓN OBLIGATORIA):**
    *   � **PROHIBIDO:** Pedir al usuario que copie/pegue manualmente.
    *   � **PROHIBIDO:** Dejar bloques de código "huérfanos" en el chat sin aplicarlos.
    *   ✅ **PASO 1 (Consultar):** Preguntar: *"¿Aplico estos cambios físicamente ahora?"*.
    *   ✅ **PASO 2 (Escribir):** Tras la confirmación, usar `write_to_file` o `replace_file_content` inmediatamente.

## 2. 🐳 ESTÁNDAR DE ENTORNOS (DOCKERIZACIÓN Y AUDITORÍA)
**Regla:** *"El código muerto no sirve. El código vivo vive en el contenedor."*

*   **Trigger:** Si modificas cualquier archivo que afecte la ejecución (`*.py`, `*.js`, `requirements.txt`, `Dockerfile`, `.env`).
*   **Reacción:** Debes proponer o ejecutar la reconstrucción:
    *   *Comando Estándar:* `docker-compose up -d --build`
    *   *Objetivo:* Asegurar que el contenedor refleje los cambios del sistema de archivos local.

### 2.1 🕵️ AUDITORÍA DE PERSISTENCIA (MANDATORIO)
Antes de dar por finalizada cualquier tarea de infraestructura, **VERIFICAR**:
1.  **Datos Críticos:** ¿Las bases de datos (SQLite, Postgres, etc.) usan **Volúmenes Nombrados** (ej. `db_data:/data`)?
    *   *Prohibido:* Usar solo rutas relativas para datos que no deben borrarse.
2.  **Secretos:** ¿Están todas las claves en `.env` y referenciadas en `docker-compose.yml`?
3.  **Prueba de Fuego:** ¿Sobreviven los datos a un `docker-compose down`?

## 3. 🌐 ADAPTABILIDAD AGNÓSTICA
**Regla:** *"Sé un camaleón. Adáptate al stack tecnológico."*

*   **Exploración Inicial:** Lee la raíz del proyecto para identificar la tecnología.
    *   🐍 **Python:** Busca `venv`, `requirements.txt`, `pyproject.toml`.
    *   📦 **Node/JS:** Busca `package.json`, `node_modules`.
    *   🐹 **Go/Rust/Otros:** Busca sus archivos de configuración estándar.
*   **Respeto al Legacy:** No reescribas la arquitectura (ej. cambiar Flask por Django) a menos que se te pida explícitamente.

## 4. 🛡️ SEGURIDAD Y LIMPIEZA
**Regla:** *"No dejes huellas peligrosas."*

### 4.1 🔐 ESCANEO DE SECRETOS (MANDATORIO)
**Trigger:** TODA modificación de código, antes de cualquier commit.

**Herramientas Obligatorias:**
1. **detect-secrets** (v1.5.0+): Escáner de credenciales en código fuente
   ```bash
   # Instalación (ya incluido en requirements.txt)
   pip install detect-secrets

   # Escaneo manual (si dudas)
   detect-secrets scan --baseline .secrets.baseline
   ```

2. **pre-commit** (v4.0.0+): Hooks automáticos de Git
   ```bash
   # Instalación una sola vez
   pre-commit install

   # El hook se ejecuta AUTOMÁTICAMENTE en cada commit
   # Si detecta secretos, BLOQUEARÁ el commit
   ```

**Configuración:**
- Archivo: `.pre-commit-config.yaml` (ya configurado en el proyecto)
- Baseline: `.secrets.baseline` (lista blanca de falsos positivos aprobados)

**Protocolo de Trabajo:**
1. ✅ **ANTES de codificar:** Asegúrate que `pre-commit install` esté ejecutado
2. ✅ **AL codificar:** NUNCA escribas claves API/passwords en texto plano. Usa `.env`
3. ✅ **AL hacer commit:** El hook detectará automáticamente secretos
4. ❌ **SI el hook BLOQUEA:** 
   - Revisa el archivo marcado
   - Mueve el secreto a `.env`
   - Si es falso positivo legítimo: `detect-secrets audit .secrets.baseline`

### 4.2 🗑️ LIMPIEZA DE ARCHIVOS
*   **Secretos:** NUNCA escribas claves API en texto plano. Usa `.env`.
*   **Archivos Basura:** Si creas scripts temporales para debug (`test_debug.py`), bórralos al terminar.

## 5. 🛑 PROTOCOLO DE CIERRE (OBLIGATORIO)
**Regla:** *"Si no está documentado, no sucedió."*

Antes de finalizar cualquier sesión o tarea grande, DEBES verificar y actualizar automáticamente:
1.  **`ESTADO_ACTUAL.md`**: ¿Refleja la última versión/cambio?
2.  **`CLAUDE_CONTEXT.md`**: ¿Hay nuevas funcionalidades o reglas?
3.  **`README.md`**: ¿Siguen siendo válidas las instrucciones de instalación/uso?

*   No esperes a que el usuario te lo pida. Es parte de la "Definition of Done".

## 6. 🧠 AUTONOMÍA RESPONSABLE
*   Si una herramienta falla (ej. error de sintaxis al editar), **CORRÍGELO TÚ MISMO**. No le pidas al usuario que lo arregle. Intenta otra estrategia o una herramienta diferente (`write_to_file` vs `replace_file_content`).

## 7. 🩺 PROTOCOLO DE INTEGRIDAD MÉDICA (CRÍTICO)
**Regla:** *"En Medicina, un punto no siempre es el final."*

Cualquier código que procese texto médico, científico o clínico **DEBE** cumplir:
1.  **NO usar `split('.')` ingenuo:** Queda terminantemente prohibido cortar oraciones mediante funciones simples de string.
    *   *Mandato:* Usar librerías NLP probadas (`nltk`, `spacy`) que respeten abreviaturas (`Dr.`, `Fig.`, `et al.`).
2.  **Validación de Datos (Guardrails):** NUNCA confiar ciegamente en la salida de un LLM.
    *   *Mandato:* Implementar checks que verifiquen la preservación de números y unidades.
3.  **Tests de Regresión:** Cualquier cambio en módulos `reescritor` o `limpiador` DEBE pasar `tests/test_medical_validity.py`.

---
*Copia este contenido en "Project Knowledge" o en tu carpeta de "Custom Instructions".*
