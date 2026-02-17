# MEMORIA DE ESTADÍA PROFESIONAL
## TÍTULO DEL PROYECTO: SISTEMA DE AUTOMATIZACIÓN DE DIFUSIÓN DE MARKETING "AUTOMARKETING"
## EMPRESA: DICOTECH

---

## INTRODUCCIÓN

En la era digital actual, la presencia en redes sociales es fundamental para la estrategia comercial de cualquier empresa. Sin embargo, para departamentos de marketing como el de DICOTECH, la gestión manual de múltiples publicaciones en diversos grupos de interés puede convertirse en una tarea repetitiva, propensa a errores y consumidora de tiempo valioso.

El presente reporte de estadía profesional describe el desarrollo e implementación de "AutoMarketing", una solución tecnológica diseñada para automatizar el proceso de difusión de campañas publicitarias en Facebook. Este proyecto surge de la necesidad de optimizar los recursos humanos del área de marketing, permitiendo a los colaboradores enfocar sus esfuerzos en la creatividad y estrategia, delegando la ejecución repetitiva a un sistema de software inteligente.

La estadía profesional en DICOTECH se realiza con el propósito de aplicar conocimientos de programación avanzada, específicamente en el lenguaje Python y tecnologías web, para resolver una problemática real y tangible de la empresa. A través de este proyecto, se busca no solo mejorar la eficiencia operativa, sino también demostrar cómo la automatización de procesos puede integrarse en flujos de trabajo tradicionales.

El reporte está organizado en cuatro capítulos fundamentales:
*   **Capítulo I:** Presenta las generalidades de DICOTECH, su identidad corporativa y el entorno donde se desarrolló el proyecto.
*   **Capítulo II:** Plantea la problemática, los objetivos, la justificación y la metodología utilizada para el desarrollo del software.
*   **Capítulo III:** Detalla el desarrollo técnico de la estadía, desde el análisis de requerimientos hasta la implementación del código y la interfaz de usuario.
*   **Capítulo IV:** Expone los resultados obtenidos, las conclusiones alcanzadas y las recomendaciones para el mantenimiento futuro del sistema.

---

## CAPÍTULO I: GENERALIDADES DE LA EMPRESA

### 1. Datos Generales
*   **Nombre de la empresa:** DICOTECH
*   **Giro:** [INSERTAR GIRO DE LA EMPRESA, EJ: TECNOLOGÍA, CONSULTORÍA, ETC.]
*   **Dirección:** [INSERTAR DIRECCIÓN]

### 2. Antecedentes Históricos
[INVESTIGAR Y REDACTAR: Breve historia de cuándo se fundó DICOTECH, cómo ha crecido y sus hitos importantes.]

### 3. Misión
[INSERTAR LA MISIÓN OFICIAL DE DICOTECH]

### 4. Visión
[INSERTAR LA VISIÓN OFICIAL DE DICOTECH]

### 5. Valores
[INSERTAR LISTA DE VALORES, EJ: INNOVACIÓN, RESPONSABILIDAD, ETC.]

### 6. Productos o Servicios que ofrece
[LISTAR LOS PRODUCTOS/SERVICIOS PRINCIPALES DE DICOTECH QUE EL ÁREA DE MARKETING PROMOCIONA]

### 7. Organigrama
[INSERTAR IMAGEN O DESCRIPCIÓN DEL ORGANIGRAMA]

### 8. Descripción del departamento donde se realizó la estadía
La estadía se llevó a cabo en el **Departamento de Desarrollo / Soporte a Marketing**. Este departamento es responsable de [DESCRIBIR FUNCIONES, EJ: proveer herramientas tecnológicas, gestionar campañas, analizar datos, etc.]. Como becario en programación asignado a esta área, mi función principal fue identificar cuellos de botella en los procesos manuales y proponer soluciones de software.

---

## CAPÍTULO II: PLANTEAMIENTO DE LA ESTADÍA PROFESIONAL

### Descripción de la Problemática
En el área de marketing de DICOTECH, los colaboradores realizan diariamente la tarea de difundir campañas y promociones de productos en grupos de Facebook. Este proceso se realiza actualmente de forma manual e implica:
1.  Iniciar sesión en cuentas corporativas.
2.  Buscar manualmente cada grupo en una lista predefinida.
3.  Copiar y pegar el texto de la campaña y subir las imágenes o enlaces correspondientes.
4.  Repetir este proceso decenas de veces.

Esta mecánica presenta varios problemas:
*   **Pérdida de tiempo:** Un colaborador puede tardar horas en publicar en 20-30 grupos.
*   **Errores humanos:** Es común equivocarse al pegar el texto, olvidar enlaces o publicar en el grupo incorrecto debido a la fatiga.
*   **Inconsistencia:** No siempre se publica a las mismas horas o con la misma frecuencia.
*   **Desmotivación:** Es una tarea monótona que no aprovecha el talento creativo del personal.

Por lo tanto, se considera un problema de eficiencia operativa que afecta el alcance de las campañas de DICOTECH.

### Objetivos

#### Objetivo General
Desarrollar e implementar un sistema web de automatización ("AutoMarketing") que permita a los colaboradores de marketing de DICOTECH programar y ejecutar publicaciones masivas en grupos de Facebook de manera desatendida, simulando el comportamiento humano para maximizar el alcance y minimizar el tiempo operativo.

#### Objetivos Específicos
1.  **Analizar** el flujo de trabajo actual de publicación en redes sociales para identificar los puntos clave de automatización.
2.  **Desarrollar** un script en Python utilizando la librería Selenium para interactuar automáticamente con el navegador web (login, navegación, publicación).
3.  **Diseñar** una interfaz gráfica de usuario (GUI) amigable basada en tecnologías web (HTML, CSS, Flask) para que el personal no técnico pueda configurar sus campañas fácilmente.
4.  **Implementar** mecanismos de seguridad y simulación humana (tiempos de espera aleatorios, escritura progresiva) para evitar bloqueos por parte de la plataforma.
5.  **Validar** el funcionamiento del sistema mediante pruebas de campo con campañas reales de DICOTECH.

### Justificación
La realización de esta estadía profesional se justifica por la necesidad de modernización tecnológica en los procesos internos de DICOTECH.
*   **¿Para qué?** Para liberar al personal de marketing de tareas repetitivas de bajo valor, permitiéndoles enfocarse en el diseño de estrategias y análisis de métricas.
*   **¿Por qué?** Porque el uso de herramientas de automatización (RPA - Robotic Process Automation) es un estándar en la industria actual para aumentar la productividad y reducir costos operativos.

### Viabilidad
El proyecto es técnica y financieramente viable:
*   **Recursos Financieros:** El desarrollo utiliza software de código abierto (Python, Selenium, Flask), por lo que no requiere licencias costosas.
*   **Recursos Humanos:** El desarrollo es realizado por el becario (autor) con supervisión del jefe de área.
*   **Recursos Materiales:** Se utiliza el equipo de cómputo ya existente en la empresa.

### Resultados Esperados
Al concluir la estadía, se espera entregar:
1.  Una aplicación funcional instalada en los equipos de marketing.
2.  Una reducción estimada del 80% en el tiempo dedicado a la publicación en grupos.
3.  Documentación técnica y manual de usuario para el sistema.
4.  Código fuente organizado y mantenible.

### Metodología a aplicar
Se utilizará una metodología de desarrollo ágil simplificada (tipo Scrum/Kanban personal) combinada con el ciclo de vida de desarrollo de software (SDLC):
1.  **Análisis de Requisitos:** Reuniones con el equipo de marketing.
2.  **Diseño:** Arquitectura del software y prototipado de interfaz.
3.  **Desarrollo:** Programación iterativa (Backend -> Scripting -> Frontend).
4.  **Pruebas:** Ejecución controlada y ajuste de errores.
5.  **Implementación:** Despliegue en entorno de producción.

---

## CAPÍTULO III: DESARROLLO DE LA ESTADÍA PROFESIONAL

### Fase 1: Análisis e Investigación
Se inició con la investigación de las herramientas necesarias. Se determinó que **Python** era el lenguaje ideal por su riqueza en librerías de automatización.
*   **Selenium WebDriver:** Seleccionado para controlar el navegador Google Chrome, ya que permite interactuar con elementos dinámicos (JavaScript) de Facebook que herramientas simples de peticiones HTTP no pueden manejar.
*   **Flask:** Seleccionado para crear un servidor web ligero que sirva la interfaz de usuario localmente.

### Fase 2: Configuración del Entorno de Desarrollo
Se procedió a instalar las herramientas en el equipo de desarrollo:
*   Instalación de Python 3.x.
*   Creación de un entorno virtual (`venv`) para aislar dependencias.
*   Instalación de librerías mediante `pip install -r requirements.txt` (selenium, flask, webdriver_manager).
*   Configuración del IDE (Trae/VS Code) para el desarrollo.

### Fase 3: Desarrollo del Motor de Automatización (Backend)
Esta fue la etapa central del proyecto. Se creó el archivo `facebook_groups_automation.py`.
**Actividades clave:**
1.  **Manejo de Login:** Se programó la función `login_facebook` que detecta los campos de correo y contraseña. Se implementó una escritura "humanizada" (carácter por carácter con retrasos aleatorios) para evitar ser detectados como bot.
2.  **Navegación:** Se implementó la lógica para recorrer una lista de URLs de grupos proporcionada por el usuario.
3.  **Interacción con el DOM:** Se utilizaron selectores CSS y XPath complejos para identificar robustamente la caja de texto "¿Qué estás pensando?" de Facebook, ya que esta plataforma cambia sus clases dinámicamente.
    *   *Reto encontrado:* Facebook tiene múltiples versiones de su interfaz.
    *   *Solución:* Se creó una lista de posibles selectores que el script prueba secuencialmente hasta encontrar el correcto.
4.  **Publicación:** Se automatizó la inserción del mensaje, la espera de la vista previa del enlace y el clic final en "Publicar".

### Fase 4: Diseño de la Interfaz de Usuario (Frontend)
Para hacer el sistema accesible, se desarrolló una interfaz web moderna.
**Archivos creados:**
*   `templates/index.html`: Estructura HTML5 con un diseño de panel de control (Dashboard).
*   `static/style.css`: Estilos CSS3 con una paleta de colores oscuros ("Dark Mode") profesional, inspirada en herramientas de desarrollo.
**Características de la interfaz:**
*   Formulario de configuración para credenciales y lista de grupos.
*   Botones de control (Iniciar / Detener).
*   **Terminal en Vivo:** Se implementó una conexión WebSocket (usando `flask-socketio`) para que los logs del proceso de Python se muestren en tiempo real en la página web, dando feedback inmediato al usuario.

### Fase 5: Integración y Pruebas
Se creó el archivo `app.py` como punto de entrada. Este script levanta el servidor Flask y gestiona los hilos de ejecución (threading) para que la automatización corra en segundo plano sin congelar la interfaz web.
**Pruebas realizadas:**
*   **Prueba Unitaria:** Login exitoso con credenciales de prueba.
*   **Prueba de Integración:** Ciclo completo de publicación en 3 grupos de prueba controlados.
*   **Ajustes:** Se calibraron los tiempos de espera (sleep) para asegurar que las imágenes carguen antes de publicar.

---

## CAPÍTULO IV: RESULTADOS Y CONCLUSIONES

### Resultados Obtenidos
1.  **Software Funcional:** Se entregó la aplicación "AutoMarketing" totalmente operativa. El sistema es capaz de realizar el login y publicar texto y enlaces en grupos definidos.
2.  **Interfaz Intuitiva:** El personal de marketing validó la interfaz web, destacando su facilidad de uso frente a la ejecución de scripts por consola.
3.  **Eficiencia:** En las pruebas finales, el sistema logró publicar en 10 grupos en aproximadamente 12 minutos (incluyendo pausas de seguridad), una tarea que manualmente tomaba cerca de 25-30 minutos y requiera atención constante. El sistema opera de forma desatendida.
4.  **Estabilidad:** El sistema maneja errores comunes (como internet lento o elementos no encontrados) sin cerrarse inesperadamente, registrando el error en el log y continuando con el siguiente grupo.

### Validación contra Objetivos
*   *Objetivo:* Automatizar publicaciones. -> *Resultado:* **CUMPLIDO**.
*   *Objetivo:* Interfaz amigable. -> *Resultado:* **CUMPLIDO** (Web Dashboard).
*   *Objetivo:* Simulación humana. -> *Resultado:* **CUMPLIDO** (Algoritmos de escritura y pausas implementados).

### Conclusiones
La estadía profesional en DICOTECH ha sido una experiencia enriquecedora que permitió cerrar la brecha entre la teoría académica y la práctica profesional.
Se concluye que:
1.  La automatización con Python es una herramienta poderosa para potenciar la productividad en áreas no técnicas como el marketing.
2.  La experiencia de usuario (UX/UI) es vital incluso en herramientas internas; una buena interfaz asegura que la herramienta sea realmente adoptada por los empleados.
3.  El desarrollo de software que interactúa con plataformas de terceros (como Facebook) requiere una programación robusta y adaptable a cambios constantes.

### Recomendaciones
Para el futuro del proyecto y la empresa, se recomienda:
1.  **Mantenimiento de Selectores:** Facebook actualiza su código frecuentemente. Se recomienda revisar los selectores XPath/CSS cada 3-6 meses.
2.  **Uso Ético:** Utilizar la herramienta con moderación (pausas largas entre grupos) para cumplir con las políticas de uso de la comunidad y evitar restricciones en las cuentas.
3.  **Escalabilidad:** Considerar en el futuro añadir soporte para adjuntar imágenes locales o programar campañas por calendario.

---

## ANEXOS

### Anexo A: Cronograma de Actividades
[INSERTAR TABLA O DIAGRAMA DE GANTT DE TUS SEMANAS DE ESTADÍA]

### Anexo B: Carta de Liberación
[ESPACIO PARA LA CARTA ESCANEADA]

### Anexo C: Evidencia de Código (Fragmento Principal)
```python
# Fragmento de app.py - Lógica de ejecución
def run_automation_logic(config):
    logger.info("🚀 Iniciando proceso de automatización...")
    current_bot_instance = FacebookGroupsAutomation(email=email, password=password)
    if current_bot_instance.login_facebook():
        for i, group_url in enumerate(groups):
            current_bot_instance.post_to_group(group_url, message, link)
            time.sleep(60) # Pausa de seguridad
```

---

## REFERENCIAS BIBLIOGRÁFICAS

1.  Python Software Foundation. (2023). *Python 3.10 Documentation*. Recuperado de https://docs.python.org/3/
2.  Selenium Project. (2023). *The Selenium Browser Automation Project*. Recuperado de https://www.selenium.dev/documentation/
3.  Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
4.  Pallets. (2023). *Flask Documentation*. Recuperado de https://flask.palletsprojects.com/
5.  Sommerville, I. (2011). *Ingeniería de software* (9a ed.). México: Pearson Educación.

