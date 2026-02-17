from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import logging
import json
import os
import threading
import time
from werkzeug.utils import secure_filename
from facebook_groups_automation import FacebookGroupsAutomation
from licensing import verify_license

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_marketing_bot'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# --- Logging Handler to WebSocket ---
class SocketHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            socketio.emit('log_message', {'data': msg, 'level': record.levelname})
        except Exception:
            self.handleError(record)

# Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Clear existing handlers to avoid duplicates
for h in logger.handlers[:]:
    logger.removeHandler(h)

socket_handler = SocketHandler()
socket_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(socket_handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# Global bot state
bot_thread = None
stop_event = threading.Event()
current_bot_instance = None

CONFIG_FILE = 'marketing_config.json'

UPLOAD_DIR = os.path.join('instance', 'uploads')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_automation_logic(config):
    global current_bot_instance
    
    email = config.get('email')
    password = config.get('password')
    groups = config.get('groups', [])
    message = config.get('message')
    facebook_description = config.get('facebook_description')
    link = config.get('link_to_promote')
    image_path = config.get('image_path')
    license_server_url = config.get('license_server_url')
    license_key = config.get('license_key')
    
    if isinstance(groups, str):
        groups = [g.strip() for g in groups.split('\n') if g.strip()]

    logger.info("🚀 Iniciando proceso de automatización...")
    
    current_bot_instance = FacebookGroupsAutomation(email=email, password=password)
    
    try:
        ok, msg, _ = verify_license(license_server_url, license_key)
        if not ok:
            logger.error(f"🔒 {msg}")
            socketio.emit('status_update', {'status': 'error'})
            return

        current_bot_instance.setup_driver()
        
        logger.info(f"🔑 Intentando iniciar sesión como: {email}")
        if not current_bot_instance.login_facebook(email=email, password=password):
            logger.error("❌ Falló el inicio de sesión. Revisa la ventana del navegador (2FA/checkpoint) o credenciales.")
            return

        logger.info("✅ Login exitoso. Esperando 5s...")
        time.sleep(5)
        
        success_count = 0
        fail_count = 0
        
        total_groups = len(groups)
        
        post_text = facebook_description or message
        if post_text and link:
            post_text = f"{post_text}\n\n{link}"

        for i, group_url in enumerate(groups):
            if stop_event.is_set():
                logger.warning("🛑 Proceso detenido por el usuario.")
                break
                
            logger.info(f"📢 [{i+1}/{total_groups}] Procesando grupo: {group_url}")
            
            try:
                if image_path:
                    abs_image = image_path
                    if not os.path.isabs(abs_image):
                        abs_image = os.path.abspath(abs_image)
                    success, status_msg = current_bot_instance.post_local_image_to_group(group_url, abs_image, post_text)
                else:
                    success, status_msg = current_bot_instance.post_to_group(group_url, post_text or "", link)
                if success:
                    success_count += 1
                    logger.info(f"✅ Publicado: {group_url}")
                else:
                    fail_count += 1
                    logger.error(f"❌ Error: {status_msg}")
            except Exception as e:
                fail_count += 1
                logger.error(f"❌ Excepción: {str(e)}")
            
            # Progress update
            progress = int(((i + 1) / total_groups) * 100)
            socketio.emit('progress_update', {'progress': progress, 'current': i+1, 'total': total_groups})

            if i < total_groups - 1 and not stop_event.is_set():
                wait_time = 60
                logger.info(f"⏳ Esperando {wait_time}s para el siguiente grupo...")
                for _ in range(wait_time):
                    if stop_event.is_set(): break
                    time.sleep(1)
        
        logger.info(f"🏁 Finalizado. Exitosos: {success_count}, Fallidos: {fail_count}")
        socketio.emit('status_update', {'status': 'completed'})
        
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        socketio.emit('status_update', {'status': 'error'})
    finally:
        if current_bot_instance:
            current_bot_instance.close_driver()
            current_bot_instance = None

@app.route('/')
def index():
    config = load_config()
    # Convert list back to string for textarea
    if isinstance(config.get('groups'), list):
        config['groups'] = '\n'.join(config['groups'])
    return render_template('index.html', config=config)

@app.route('/save_config', methods=['POST'])
def save_configuration():
    data = request.json
    # Convert groups string to list for saving
    groups_str = data.get('groups', '')
    data['groups'] = [g.strip() for g in groups_str.split('\n') if g.strip()]
    
    save_config(data)
    return jsonify({'status': 'success', 'message': 'Configuración guardada'})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        file = request.files.get('image')
        if not file or not file.filename:
            return jsonify({'status': 'error', 'message': 'No se recibió archivo'}), 400

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        safe_name = secure_filename(file.filename)
        base, ext = os.path.splitext(safe_name)
        ts = int(time.time())
        final_name = f"{base}_{ts}{ext}" if ext else f"{base}_{ts}"
        rel_path = os.path.join(UPLOAD_DIR, final_name)
        abs_path = os.path.abspath(rel_path)
        file.save(abs_path)

        return jsonify({'status': 'success', 'image_path': rel_path.replace('\\', '/')})
    except Exception as e:
        logger.error(f"Error subiendo imagen: {e}")
        return jsonify({'status': 'error', 'message': 'Error subiendo imagen'}), 500

@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot_thread, stop_event
    
    if bot_thread and bot_thread.is_alive():
        return jsonify({'status': 'error', 'message': 'El bot ya está en ejecución'})
    
    config = load_config()

    ok, msg, _ = verify_license(config.get('license_server_url'), config.get('license_key'))
    if not ok:
        return jsonify({'status': 'error', 'message': f'🔒 {msg}'}), 403
    stop_event.clear()
    
    bot_thread = threading.Thread(target=run_automation_logic, args=(config,))
    bot_thread.start()
    
    return jsonify({'status': 'success', 'message': 'Bot iniciado'})

@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global stop_event
    stop_event.set()
    logger.info("🛑 Solicitando detención del bot...")
    return jsonify({'status': 'success', 'message': 'Deteniendo bot...'})

if __name__ == '__main__':
    host = os.environ.get('AUTOMARKETING_HOST', '127.0.0.1')
    port = int(os.environ.get('AUTOMARKETING_PORT', '5000'))
    debug = os.environ.get('AUTOMARKETING_DEBUG', '0') == '1'
    socketio.run(app, debug=debug, host=host, port=port, use_reloader=False)
