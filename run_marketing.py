import json
import logging
import os
import time
import sys
from facebook_groups_automation import FacebookGroupsAutomation
from licensing import verify_license

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('marketing_bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path='marketing_config.json'):
    """Carga la configuración desde el archivo JSON"""
    if not os.path.exists(config_path):
        logger.error(f"No se encontró el archivo de configuración: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"Error al leer la configuración: {e}")
        return None

def main():
    logger.info("Iniciando Bot de Marketing para Facebook...")
    
    # 1. Cargar configuración
    config = load_config()
    if not config:
        print("Error: No se pudo cargar la configuración. Revisa 'marketing_bot.log'.")
        return

    email = config.get('email')
    password = config.get('password')
    groups = config.get('groups', [])
    message = config.get('message')
    facebook_description = config.get('facebook_description')
    link = config.get('link_to_promote')
    image_path = config.get('image_path')
    license_server_url = config.get('license_server_url')
    license_key = config.get('license_key')

    # Validar configuración
    if not email or "ejemplo.com" in email:
        logger.error("Configuración incompleta: Por favor edita 'marketing_config.json' con tu correo real.")
        print("Error: Configura tu correo y contraseña en 'marketing_config.json'.")
        return

    if not groups:
        logger.warning("No hay grupos configurados para publicar.")
        print("Aviso: Agrega enlaces de grupos en 'marketing_config.json'.")
        return

    # 2. Inicializar automatización
    bot = FacebookGroupsAutomation(email=email, password=password)
    
    try:
        ok, msg, _ = verify_license(license_server_url, license_key)
        if not ok:
            logger.error(f"🔒 {msg}")
            return

        # 3. Configurar navegador
        bot.setup_driver()
        
        # 4. Iniciar sesión
        logger.info(f"Intentando iniciar sesión con: {email}")
        if not bot.login_facebook(email=email, password=password):
            logger.error("No se pudo iniciar sesión. Verifica tus credenciales o si hay bloqueos.")
            return
        
        logger.info("Inicio de sesión exitoso. Esperando 10 segundos antes de comenzar...")
        time.sleep(10)

        # 5. Publicar en grupos
        logger.info(f"Comenzando publicación en {len(groups)} grupos.")
        
        success_count = 0
        fail_count = 0
        
        for i, group_url in enumerate(groups):
            logger.info(f"Procesando grupo {i+1}/{len(groups)}: {group_url}")
            
            # Verificar si la URL es válida (básico)
            if "facebook.com" not in group_url:
                logger.warning(f"URL de grupo inválida, saltando: {group_url}")
                continue

            try:
                post_text = facebook_description or message
                if post_text and link:
                    post_text = f"{post_text}\n\n{link}"
                if image_path:
                    abs_image = image_path
                    if not os.path.isabs(abs_image):
                        abs_image = os.path.abspath(abs_image)
                    success, status_msg = bot.post_local_image_to_group(group_url, abs_image, post_text)
                else:
                    success, status_msg = bot.post_to_group(group_url, post_text or "", link)
                
                if success:
                    success_count += 1
                    logger.info(f"✅ Publicado exitosamente en: {group_url}")
                else:
                    fail_count += 1
                    logger.error(f"❌ Falló publicación en {group_url}: {status_msg}")
            except Exception as e:
                fail_count += 1
                logger.error(f"❌ Error crítico en grupo {group_url}: {e}")

            # Pausa entre publicaciones para evitar bloqueos (Importante)
            if i < len(groups) - 1:
                wait_time = 60  # 60 segundos entre grupos (ajustable)
                logger.info(f"Esperando {wait_time} segundos antes del siguiente grupo...")
                time.sleep(wait_time)
        
        # Resumen final
        logger.info("="*50)
        logger.info(f"PROCESO TERMINADO")
        logger.info(f"Exitosos: {success_count}")
        logger.info(f"Fallidos: {fail_count}")
        logger.info("="*50)

    except Exception as e:
        logger.error(f"Error general en la ejecución: {e}")
    finally:
        # Cerrar navegador al finalizar
        # Comentar la siguiente línea si quieres dejar el navegador abierto para inspeccionar
        # bot.close_driver()
        logger.info("Navegador finalizado (o mantenido abierto según configuración).")
        print("Proceso finalizado. Revisa el log para más detalles.")

if __name__ == "__main__":
    main()
