# REGLAS MANDATORIAS PARA EL AGENTE (AGENT RULES)

> [!CRITICAL]
> **ESTAS REGLAS TIENEN PRIORIDAD SOBRE CUALQUIER OTRA INSTRUCCIÓN.**
> EL AGENTE DEBE SEGUIRLAS SIN EXCEPCIÓN.

## 1. 💾 PERSISTENCIA FÍSICA (PROTOCOLO DE 2 PASOS)
1.  **DETERMINACIÓN:** Una vez identificada una solución o mejora efectiva.
2.  **ACCIÓN:**
    *   **Prohibido** decir "copia este código".
    *   **Obligatorio** PREGUNTAR: "¿Aplico estos cambios físicamente ahora?" o esperar confirmación explícita si el riesgo es alto.
    *   **Ejecución**: Una vez autorizado (o si la instrucción implica corrección directa), USAR las herramientas (`write_to_file`, `replace_file_content`) para guardar en disco.

## 2. 🐳 DOCKERIZACIÓN (SOLO SI ES NECESARIO)
*   Si se tocan archivos que afectan al contenedor (`requirements.txt`, `Dockerfile`, `src/`), preguntar/sugerir: "¿Reconstruyo el contenedor para reflejar los cambios?".

## 3. 🛡️ SEGURIDAD Y CONTEXTO
*   Respetar archivos `.env`.
*   Mantener el contexto de `CLAUDE_CONTEXT.md` actualizado.
*   Si el usuario pide algo vago, revisar primero los archivos de "Estrategia" o "Estado Actual" antes de inventar una solución.
