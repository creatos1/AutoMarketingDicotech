# AutoMarketing (Facebook Groups)

Este repositorio incluye:
- Un panel web (`app.py`) para configurar campaña y ejecutar el bot.
- Un runner por consola (`run_marketing.py`).
- Automatización con Selenium (`facebook_groups_automation.py`).

## Importante sobre Vercel (plan gratis)

Este proyecto **no puede ejecutarse correctamente en Vercel** como “bot” porque:
- Vercel es serverless con límites de tiempo; Selenium requiere un navegador real y procesos largos.
- `flask-socketio` (WebSocket) no encaja bien con serverless clásico.
- El login manual/2FA necesita una sesión de navegador interactiva.

Vercel sí sirve para hospedar una UI estática, pero **la automatización debe correr en una PC/VPS**.

## Cobrar por periodos + modo mantenimiento (licencias)

La forma práctica de “cobrar cada X tiempo” y poder parar el sistema para mantenimiento es usar un **servidor de licencias**:

- El cliente (tu `.exe` o el `app.py`) guarda:
  - `license_key`
  - `license_server_url`
- Cada vez que se presiona **Iniciar Bot** (o al correr `run_marketing.py`) el programa llama a `license_server_url`.
- Si el servidor responde:
  - `{"status":"ok"}` → deja ejecutar.
  - `{"maintenance":true}` → bloquea con mensaje “mantenimiento”.
  - `expires_at` en el pasado → bloquea por “licencia vencida”.

En este repo ya está integrado el chequeo:
- Módulo: `licensing.py`
- En dashboard: `license_key` y `license_server_url` en el formulario

### Cómo cobrar (Stripe) en plan gratis

Patrón típico:
- Stripe Subscription (mensual/anual).
- Webhook de Stripe (cuando paga / falla / cancela) → tu backend actualiza `expires_at` o `status` de esa `license_key`.
- El bot verifica en cada ejecución.

Puedes alojar el **servidor de licencias** en:
- Vercel (API serverless) o cualquier hosting simple.
- Base de datos: Supabase / Postgres / SQLite (si es muy pequeño).

### Limitación importante

Si el bot puede funcionar sin internet, cualquier control por tiempo puede ser burlado. Para control real:
- Requiere verificación online o al menos “renovación” periódica.

## Subir a GitHub sin filtrar credenciales

- `marketing_config.json` está en `.gitignore`.
- Usa `marketing_config.example.json` como plantilla y crea tu propio `marketing_config.json` local.

Si ya subiste credenciales a GitHub alguna vez, cambia la contraseña y revisa historial.

## Ejecutar en otra PC (sin instalar Python)

Opción recomendada: generar un `.exe` (Windows) con GitHub Actions y descargarlo desde Releases.

### 1) Crear Release en GitHub

- Sube el repo a GitHub.
- En Actions, ejecuta el workflow “Build Windows executables”.
- Descarga los artefactos (`AutoMarketing-Dashboard.exe` y `AutoMarketing-CLI.exe`).

### 2) Usar el dashboard

- Ejecuta `AutoMarketing-Dashboard.exe`.
- Abre `http://127.0.0.1:5000/`.

Requisitos en la PC:
- Google Chrome instalado.

## Ejecutar con Python (alternativa)

```bash
pip install -r requirements.txt
python app.py
```

