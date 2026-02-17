
import logging
import time
import os
import random
from typing import List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

logger = logging.getLogger(__name__)

class FacebookGroupsAutomation:
    """Automatiza las publicaciones en grupos de Facebook usando Selenium"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        logger.info("FacebookGroupsAutomation: Inicializando automatización de grupos")
        self.driver = None
        self.wait = None
        self.email = email
        self.password = password
        
    def setup_driver(self):
        """Configura el driver de Chrome"""
        logger.info("FacebookGroupsAutomation: Configurando Chrome WebDriver")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        chrome_options.add_argument("--incognito")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            try:
                self.driver.delete_all_cookies()
            except Exception:
                pass
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"})
            self.wait = WebDriverWait(self.driver, 60)
            
            logger.info("FacebookGroupsAutomation: Driver configurado exitosamente")
        except Exception as e:
            logger.error(f"FacebookGroupsAutomation: Error configurando driver: {e}")
            raise Exception(f"No se pudo configurar Chrome WebDriver: {e}")
        
    def login_facebook(self, email: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Inicia sesión en Facebook"""
        logger.info("FacebookGroupsAutomation: Iniciando sesión en Facebook")

        email_to_use = email or self.email
        password_to_use = password or self.password
        
        try:
            # Ir a la página de login (sesión fresca en modo incógnito)
            self.driver.get("https://www.facebook.com/login")
            time.sleep(3)
            try:
                self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            except:
                pass
            try:
                for xpath in [
                    "//button[contains(., 'Aceptar')]",
                    "//button[contains(., 'Permitir todas')]",
                    "//button[contains(., 'Allow all')]",
                    "//div[@role='button'][contains(., 'Continuar')]",
                ]:
                    try:
                        btn = self.driver.find_element(By.XPATH, xpath)
                        if btn.is_displayed():
                            try:
                                btn.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", btn)
                            time.sleep(1)
                    except:
                        continue
            except:
                pass
            
            selectors_email: List[Tuple[str, str]] = [
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input#email"),
                (By.CSS_SELECTOR, "input[name='email']"),
                (By.CSS_SELECTOR, "input#m_login_email"),
            ]
            selectors_pass: List[Tuple[str, str]] = [
                (By.ID, "pass"),
                (By.NAME, "pass"),
                (By.CSS_SELECTOR, "input#pass"),
                (By.CSS_SELECTOR, "input[name='pass']"),
                (By.CSS_SELECTOR, "input#m_login_password"),
            ]
            email_field = None
            password_field = None
            # Intentar localizar campos en desktop
            for loc in selectors_email:
                try:
                    email_field = self.wait.until(EC.presence_of_element_located(loc))
                    break
                except:
                    continue
            for loc in selectors_pass:
                try:
                    password_field = self.driver.find_element(*loc)
                    break
                except:
                    continue
            # Fallback a m.facebook si no se encuentran campos
            if not email_field or not password_field:
                try:
                    self.driver.get("https://m.facebook.com/login")
                    time.sleep(2)
                    for loc in selectors_email:
                        try:
                            email_field = self.wait.until(EC.presence_of_element_located(loc))
                            break
                        except:
                            continue
                    for loc in selectors_pass:
                        try:
                            password_field = self.driver.find_element(*loc)
                            break
                        except:
                            continue
                except:
                    pass
            # Si aún no hay campos, no hay sesión y no se encuentra el formulario
            # se mantendrá el flujo con Fallback a m.facebook y error si no aparecen
            
            if email_to_use and password_to_use and email_field and password_field:
                try:
                    try:
                        ActionChains(self.driver).move_to_element(email_field).pause(random.uniform(0.2, 0.6)).click().perform()
                    except Exception:
                        email_field.click()
                    try:
                        email_field.clear()
                    except:
                        pass
                    self._human_type(email_field, email_to_use, 0.06)
                    try:
                        ActionChains(self.driver).move_to_element(password_field).pause(random.uniform(0.2, 0.6)).click().perform()
                    except Exception:
                        password_field.click()
                    try:
                        password_field.clear()
                    except:
                        pass
                    self._human_type(password_field, password_to_use, 0.06)
                    login_button = None
                    try:
                        login_button = self.driver.find_element(By.NAME, "login")
                    except:
                        try:
                            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                        except:
                            pass
                    if not login_button:
                        try:
                            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[name='login']")
                        except:
                            pass
                    if login_button:
                        try:
                            ActionChains(self.driver).move_to_element(login_button).pause(random.uniform(0.2, 0.5)).click().perform()
                        except Exception:
                            login_button.click()
                    
                    if self._wait_for_login(timeout_seconds=90):
                        logger.info("FacebookGroupsAutomation: Login automático exitoso")
                    else:
                        logger.info("FacebookGroupsAutomation: Login automático no confirmado, esperando verificación manual")
                        if self._wait_for_login(timeout_seconds=300):
                            logger.info("FacebookGroupsAutomation: Login detectado tras verificación manual")
                        else:
                            self._capture_debug("login_timeout")
                            logger.error("FacebookGroupsAutomation: Timeout esperando login")
                            return False
                except Exception:
                    try:
                        self._capture_debug("login_auto_error")
                    except Exception:
                        pass
                    logger.exception("FacebookGroupsAutomation: Error en login")
                    return False
            else:
                logger.info("FacebookGroupsAutomation: Esperando login manual del usuario")
                print("Por favor, inicia sesión manualmente en la ventana del navegador...")
                try:
                    if not self._wait_for_login(timeout_seconds=300):
                        raise TimeoutException("Timeout esperando login manual")
                    logger.info("FacebookGroupsAutomation: Login manual detectado")
                except Exception:
                    try:
                        self._capture_debug("login_error")
                    except Exception:
                        pass
                    logger.exception("FacebookGroupsAutomation: Error en login")
                    return False
                
            return True
            
        except Exception:
            try:
                self._capture_debug("login_exception")
            except Exception:
                pass
            logger.exception("FacebookGroupsAutomation: Error en login")
            return False

    def _is_logged_in(self) -> bool:
        try:
            url = ""
            try:
                url = (self.driver.current_url or "").lower()
            except Exception:
                url = ""
            if any(x in url for x in ["/login", "checkpoint", "recover", "two_factor", "device-based"]):
                return False
            try:
                cookies = self.driver.get_cookies()
                if any(c.get("name") == "c_user" and c.get("value") for c in cookies):
                    return True
            except Exception:
                pass
            for sel in [
                "[data-testid='search']",
                "[aria-label='Inicio']",
                "[aria-label='Home']",
                "[data-testid='facebar_root']",
                "a[href*='/groups/']",
                "#MComposer",
            ]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if el.is_displayed():
                        return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    def _wait_for_login(self, timeout_seconds: int) -> bool:
        start = time.time()
        last_url = None
        while time.time() - start < timeout_seconds:
            try:
                current_url = None
                try:
                    current_url = self.driver.current_url
                except Exception:
                    current_url = None
                if current_url and current_url != last_url:
                    last_url = current_url
                if self._is_logged_in():
                    return True
                if last_url and any(x in last_url.lower() for x in ["checkpoint", "two_factor", "device-based"]):
                    time.sleep(2)
                else:
                    time.sleep(1.5)
            except WebDriverException:
                time.sleep(1.5)
            except Exception:
                time.sleep(1.5)
        return False
    
    def post_to_group(self, group_url: str, message: str, link: Optional[str] = None) -> Tuple[bool, str]:
        """Publica en un grupo específico de Facebook"""
        logger.info(f"FacebookGroupsAutomation: Publicando en grupo: {group_url}")
        
        try:
            url = group_url.strip().strip('`"\'')
            if not url.startswith("http"):
                url = "https://" + url
            if not self._navigate_to_group(url):
                return False, "No se pudo cargar el grupo"
            # Si por alguna razón se redirige a login, intentar login y volver al grupo
            try:
                current = self.driver.current_url
                if "login" in current or "signin" in current:
                    if self.email and self.password:
                        if self.login_facebook(self.email, self.password):
                            self.driver.get(url)
                            time.sleep(3)
            except:
                pass
            self._close_overlays()
            
            # Abrir compositor del grupo en desktop
            opened = self._click_xpath([
                '//div[@role="button"][contains(., "Crear publicación")]',
                '//span[contains(., "Crear publicación")]/ancestor::div[@role="button"]',
                '//div[@role="button"][contains(., "¿Qué estás pensando")]',
                '//span[contains(., "¿Qué estás pensando")]/ancestor::div[@role="button"]',
                '//div[@role="button"][contains(., "Escribe algo")]',
                '//span[contains(., "Escribe algo")]/ancestor::div[@role="button"]',
                '//div[@role="button"][contains(., "Create post")]',
                '//span[contains(., "Create post")]/ancestor::div[@role="button"]',
                '//div[@role="button"][contains(., "What\'s on your mind")]',
                '//span[contains(., "What\'s on your mind")]/ancestor::div[@role="button"]',
            ])
            if not opened:
                try:
                    self.driver.execute_script("window.scrollTo(0, 500);")
                    time.sleep(1)
                    opened = self._click_xpath([
                        "//div[@role='button'][contains(., 'Crear publicación')]",
                        "//div[@role='button'][contains(., 'Create post')]",
                    ])
                except:
                    pass

            # Buscar área de texto dentro del modal del compositor
            post_box_selectors: List[str] = [
                "div[role='dialog'] div[role='textbox'][contenteditable='true']",
                "div[role='dialog'] div[contenteditable='true']",
                "div[role='textbox'][data-testid]",
                "div[contenteditable='true']",
                "[data-testid='status-attachment-mentions-input']",
                "div[aria-label='Crear publicación'] div[contenteditable='true']",
                "div[aria-label*='¿Qué estás pensando']",
                "div[aria-label*='What\'s on your mind']",
            ]
            
            post_box = None
            for selector in post_box_selectors:
                try:
                    post_box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if not post_box:
                # Fallback: intentar vista móvil del grupo para abrir compositor más simple
                try:
                    if "/groups/" in url:
                        group_id = url.split("/groups/")[-1].split("?")[0].split("/")[0]
                        m_url = f"https://m.facebook.com/groups/{group_id}"
                        self.driver.get(m_url)
                        time.sleep(3)
                        for sel in [
                            "div[role='textbox'][contenteditable='true']",
                            "textarea",
                        ]:
                            try:
                                post_box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                                break
                            except:
                                continue
                except:
                    pass
                if not post_box:
                    try:
                        out_dir = os.path.join(os.getcwd(), 'instance', 'automation_logs')
                        os.makedirs(out_dir, exist_ok=True)
                        ts = int(time.time())
                        self.driver.save_screenshot(os.path.join(out_dir, f'no_composer_{ts}.png'))
                        with open(os.path.join(out_dir, f'no_composer_{ts}.html'), 'w', encoding='utf-8') as f:
                            f.write(self.driver.page_source)
                    except Exception:
                        pass
                    raise Exception("No se pudo encontrar el área de publicación")
            
            # Hacer clic en el área de publicación
            post_box.click()
            time.sleep(2)

            post_text = message or ""
            if link:
                post_text = f"{post_text}\n\n{link}" if post_text else link

            self._human_paste(post_box, post_text)
            time.sleep(2)

            if post_text:
                try:
                    current_text = ""
                    try:
                        current_text = (post_box.get_attribute("innerText") or post_box.get_attribute("textContent") or "")
                    except Exception:
                        current_text = ""
                    if not current_text.strip():
                        self._capture_debug("paste_empty_post")
                except Exception:
                    pass

            if link:
                self._wait_for_preview()
            
            # Buscar y hacer clic en el botón de publicar
            publish_selectors: List[str] = [
                "div[role='dialog'] [data-testid='react-composer-post-button']",
                "div[role='dialog'] div[aria-label='Publicar']",
                "div[role='dialog'] button[type='submit']",
                "div[role='dialog'] [data-testid='composer-post-button']",
                "[data-testid='react-composer-post-button']",
                "div[aria-label='Publicar']",
                "button[type='submit']",
            ]
            
            publish_button = None
            for selector in publish_selectors:
                try:
                    publish_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if publish_button.is_enabled():
                        break
                except:
                    continue
            if not publish_button:
                for xp in [
                    "//div[@role='dialog']//span[contains(., 'Publicar')]/ancestor::*[@role='button']",
                    "//div[@role='dialog']//span[contains(., 'Post')]/ancestor::*[@role='button']",
                ]:
                    try:
                        publish_button = self.driver.find_element(By.XPATH, xp)
                        break
                    except:
                        continue
            if not publish_button:
                for xp in [
                    "//div[@role='dialog']//span[contains(., 'Publicar')]/ancestor::*[@role='button']",
                    "//div[@role='dialog']//span[contains(., 'Post')]/ancestor::*[@role='button']",
                    "//div[@role='dialog']//div[@role='button'][.//span[contains(., 'Publicar')]]",
                ]:
                    try:
                        publish_button = self.driver.find_element(By.XPATH, xp)
                        break
                    except:
                        continue
            
            if publish_button:
                try:
                    publish_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", publish_button)
                try:
                    for _ in range(30):
                        try:
                            self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
                            time.sleep(1)
                            continue
                        except:
                            break
                except:
                    pass
                logger.info("FacebookGroupsAutomation: Publicación enviada exitosamente")
                return True, "Publicación enviada exitosamente"
            else:
                try:
                    out_dir = os.path.join(os.getcwd(), 'instance', 'automation_logs')
                    os.makedirs(out_dir, exist_ok=True)
                    ts = int(time.time())
                    self.driver.save_screenshot(os.path.join(out_dir, f'no_publish_button_{ts}.png'))
                    with open(os.path.join(out_dir, f'no_publish_button_{ts}.html'), 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                except Exception:
                    pass
                logger.error("FacebookGroupsAutomation: No se encontró botón de publicar")
                return False, "No se pudo encontrar el botón de publicar"
                
        except Exception as e:
            logger.error(f"FacebookGroupsAutomation: Error publicando en grupo: {e}")
            return False, f"Error publicando: {str(e)}"

    def _navigate_to_group(self, url: str) -> bool:
        try:
            for attempt in range(3):
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                    self.driver.execute_script("window.scrollTo(0, 0);")
                except Exception:
                    time.sleep(2)
                self._close_overlays()
                try:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='main']")))
                    return True
                except Exception:
                    time.sleep(2)
                    continue
            return False
        except Exception:
            return False

    def _close_overlays(self):
        try:
            for xp in [
                "//button[contains(., 'Aceptar')]",
                "//button[contains(., 'Permitir todas')]",
                "//button[contains(., 'Accept all')]",
                "//div[@role='button'][contains(., 'Continuar')]",
                "//span[contains(., 'Continuar')]/ancestor::div[@role='button']",
            ]:
                try:
                    el = self.driver.find_element(By.XPATH, xp)
                    if el.is_displayed():
                        try:
                            el.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", el)
                        time.sleep(1)
                except Exception:
                    continue
        except Exception:
            pass

    def _click_xpath(self, xpaths: List[str]) -> bool:
        for xp in xpaths:
            try:
                el = self.driver.find_element(By.XPATH, xp)
                if el.is_displayed():
                    try:
                        el.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(2)
                    return True
            except Exception:
                continue
        return False
    
    def post_video_to_groups(self, video, group_urls: List[str]):
        """Publica un video en múltiples grupos"""
        logger.info(f"FacebookGroupsAutomation: Publicando video en {len(group_urls)} grupos")
        
        # Crear mensaje formateado
        message = f"🎥 Nuevo video: {video.title}\n\n"
        
        if video.description:
            description = video.description[:300] + "..." if len(video.description) > 300 else video.description
            message += f"{description}\n\n"
        
        message += f"👁️ {video.view_count:,} visualizaciones\n"
        message += f"👍 {video.like_count:,} likes\n\n"
        message += f"¡Míralo aquí! 👇"
        
        results = []
        
        for group_url in group_urls:
            logger.info(f"FacebookGroupsAutomation: Publicando en: {group_url}")
            success, msg = self.post_to_group(group_url, message, video.youtube_url)
            results.append({
                'group_url': group_url,
                'success': success,
                'message': msg
            })
            
            # Pausa entre publicaciones para evitar ser detectado como spam
            time.sleep(10)
        
        return results

    def post_local_video_to_group(self, group_url: str, file_path: str, message: Optional[str] = None) -> Tuple[bool, str]:
        logger.info(f"FacebookGroupsAutomation: Publicando video local en: {group_url}")
        try:
            if not file_path or not os.path.exists(file_path):
                return False, "Archivo no encontrado"
            url = group_url.strip().strip('`"\'')
            if not url.startswith("http"):
                url = "https://" + url
            self.driver.get(url)
            time.sleep(5)
            try:
                self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            except:
                pass
            # Abrir compositor del grupo (desktop) para asegurar que aparezca el input de adjuntos
            try:
                for xpath in [
                    "//div[@role='button'][contains(., 'Crear publicación')]",
                    "//span[contains(., 'Crear publicación')]/ancestor::div[@role='button']",
                    "//div[@role='button'][contains(., '¿Qué estás pensando')]",
                    "//span[contains(., '¿Qué estás pensando')]/ancestor::div[@role='button']",
                    "//div[@role='button'][contains(., 'Escribe algo')]",
                    "//span[contains(., 'Escribe algo')]/ancestor::div[@role='button']",
                ]:
                    try:
                        btn = self.driver.find_element(By.XPATH, xpath)
                        if btn.is_displayed():
                            try:
                                btn.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", btn)
                            time.sleep(2)
                            break
                    except:
                        continue
            except:
                pass

            # Intentar abrir acción Foto/Video dentro del modal
            try:
                for xp in [
                    "//div[@role='dialog']//div[@role='button'][contains(., 'Foto') or contains(., 'Video')]",
                    "//div[@role='dialog']//span[contains(., 'Foto') or contains(., 'Video')]/ancestor::div[@role='button']",
                ]:
                    try:
                        b = self.driver.find_element(By.XPATH, xp)
                        try:
                            b.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", b)
                        time.sleep(2)
                        break
                    except:
                        continue
            except:
                pass

            upload_input = None
            # Priorizar input dentro del modal
            for sel in [
                "div[role='dialog'] input[type='file']",
                "input[type='file']",
            ]:
                try:
                    upload_input = self.driver.find_element(By.CSS_SELECTOR, sel)
                    break
                except:
                    continue
            if not upload_input:
                try:
                    out_dir = os.path.join(os.getcwd(), 'instance', 'automation_logs')
                    os.makedirs(out_dir, exist_ok=True)
                    ts = int(time.time())
                    self.driver.save_screenshot(os.path.join(out_dir, f'no_upload_input_{ts}.png'))
                    with open(os.path.join(out_dir, f'no_upload_input_{ts}.html'), 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                except Exception:
                    pass
                return False, "No se encontró el selector de carga"
            upload_input.send_keys(file_path)
            time.sleep(7)
            if message:
                try:
                    box = None
                    for sel in [
                        "div[role='dialog'] div[role='textbox'][contenteditable='true']",
                        "div[role='dialog'] div[contenteditable='true']",
                    ]:
                        try:
                            box = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, sel)))
                            break
                        except:
                            continue
                    if box:
                        box.click()
                        time.sleep(1)
                        self._human_paste(box, message)
                except:
                    pass
            publish_button = None
            for selector in [
                "div[role='dialog'] [data-testid='react-composer-post-button']",
                "div[role='dialog'] div[aria-label='Publicar']",
                "div[role='dialog'] button[type='submit']",
                "div[role='dialog'] [data-testid='composer-post-button']",
                "[data-testid='react-composer-post-button']",
                "div[aria-label='Publicar']",
                "button[type='submit']",
            ]:
                try:
                    publish_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if publish_button.is_enabled():
                        break
                except:
                    continue
            if not publish_button:
                return False, "No se pudo encontrar el botón de publicar"
            try:
                publish_button.click()
            except:
                self.driver.execute_script("arguments[0].click();", publish_button)
            # Esperar a que se cierre el modal (indicador de envío)
            try:
                for _ in range(20):
                    try:
                        self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
                        time.sleep(1)
                        continue
                    except:
                        break
            except:
                pass
            return True, "Video local publicado"
        except Exception as e:
            logger.error(f"FacebookGroupsAutomation: Error publicando video local: {e}")
            return False, f"Error publicando video local: {str(e)}"

    def post_local_image_to_group(self, group_url: str, file_path: str, message: Optional[str] = None) -> Tuple[bool, str]:
        logger.info(f"FacebookGroupsAutomation: Publicando imagen en: {group_url}")
        ok, msg = self.post_local_video_to_group(group_url, file_path, message)
        if ok:
            return True, "Imagen publicada"
        return False, msg

    def post_local_video_to_groups(self, file_path: str, message: Optional[str], group_urls: List[str]):
        results = []
        for group_url in group_urls:
            success, msg = self.post_local_video_to_group(group_url, file_path, message)
            results.append({
                'group_url': group_url,
                'success': success,
                'message': msg
            })
            time.sleep(12)
        return results
    
    def close_driver(self):
        """Cierra el navegador"""
        if self.driver:
            logger.info("FacebookGroupsAutomation: Cerrando navegador")
            self.driver.quit()
            self.driver = None

    def _human_type(self, element, text: Optional[str], delay: float):
        if not text:
            return
        try:
            element.click()
        except:
            pass
        for ch in text:
            element.send_keys(ch)
            time.sleep(random.uniform(delay * 0.6, delay * 1.4))

    def _human_paste(self, element, text: Optional[str]):
        if text is None:
            return
        try:
            import tkinter as tk

            def _focus_element():
                try:
                    ActionChains(self.driver).move_to_element(element).pause(random.uniform(0.1, 0.25)).click().perform()
                    return
                except Exception:
                    pass
                try:
                    element.click()
                    return
                except Exception:
                    pass
                try:
                    self.driver.execute_script("arguments[0].focus();", element)
                except Exception:
                    pass

            def _read_current_value() -> str:
                try:
                    val = element.get_attribute("value")
                    if isinstance(val, str) and val.strip():
                        return val
                except Exception:
                    pass
                try:
                    inner = element.get_attribute("innerText")
                    if isinstance(inner, str) and inner.strip():
                        return inner
                except Exception:
                    pass
                try:
                    tc = element.get_attribute("textContent")
                    if isinstance(tc, str) and tc.strip():
                        return tc
                except Exception:
                    pass
                return ""

            def _ctrl_v_paste():
                _focus_element()
                time.sleep(random.uniform(0.15, 0.4))
                try:
                    ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                    time.sleep(random.uniform(0.1, 0.25))
                except Exception:
                    try:
                        element.send_keys(Keys.CONTROL, 'a')
                    except Exception:
                        pass
                try:
                    ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                except Exception:
                    element.send_keys(Keys.CONTROL, 'v')
                time.sleep(random.uniform(0.25, 0.6))

            def _human_multiline_paste():
                root = tk.Tk()
                root.withdraw()

                _focus_element()
                time.sleep(random.uniform(0.15, 0.35))
                try:
                    ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                    time.sleep(random.uniform(0.1, 0.25))
                except Exception:
                    try:
                        element.send_keys(Keys.CONTROL, 'a')
                    except Exception:
                        pass

                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if line:
                        try:
                            root.clipboard_clear()
                            root.clipboard_append(line)
                            root.update()
                        except Exception:
                            pass
                        try:
                            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                        except Exception:
                            try:
                                element.send_keys(Keys.CONTROL, 'v')
                            except Exception:
                                element.send_keys(line)
                        time.sleep(random.uniform(0.12, 0.25))

                    if i < len(lines) - 1:
                        try:
                            ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                        except Exception:
                            try:
                                element.send_keys(Keys.SHIFT, Keys.ENTER)
                            except Exception:
                                element.send_keys(Keys.ENTER)
                        time.sleep(random.uniform(0.08, 0.18))

                try:
                    root.destroy()
                except Exception:
                    pass

            def _js_insert_text():
                try:
                    self.driver.execute_script(
                        "arguments[0].focus();"
                        "try { document.execCommand('selectAll', false, null); } catch(e) {}"
                        "try { document.execCommand('insertText', false, arguments[1]); } catch(e) { arguments[0].innerText = arguments[1]; }",
                        element,
                        text,
                    )
                    time.sleep(random.uniform(0.2, 0.45))
                except Exception:
                    pass

            if '\n' in text:
                _human_multiline_paste()
                if _read_current_value().strip():
                    return

            root = tk.Tk()
            root.withdraw()
            try:
                root.clipboard_clear()
                root.clipboard_append(text)
                root.update()
            except Exception:
                pass
            try:
                root.destroy()
            except Exception:
                pass

            _ctrl_v_paste()
            if not _read_current_value():
                _ctrl_v_paste()
            if not _read_current_value():
                _js_insert_text()
            if not _read_current_value():
                try:
                    element.send_keys(text)
                except Exception:
                    pass
        except Exception:
            try:
                element.send_keys(text)
            except Exception:
                pass

    def _wait_for_preview(self):
        try:
            preview_selectors: List[str] = [
                "img[src*='ytimg.com']",
                "a[href*='youtube.com/watch']",
                "[data-testid*='attachment']",
                "div[aria-label*='enlace']",
            ]
            for sel in preview_selectors:
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
                    return
                except:
                    continue
            time.sleep(3)
        except:
            pass

    def _capture_debug(self, tag: str):
        try:
            out_dir = os.path.join(os.getcwd(), 'instance', 'automation_logs')
            os.makedirs(out_dir, exist_ok=True)
            ts = int(time.time())
            png = os.path.join(out_dir, f'{tag}_{ts}.png')
            html = os.path.join(out_dir, f'{tag}_{ts}.html')
            meta = os.path.join(out_dir, f'{tag}_{ts}.txt')
            try:
                self.driver.save_screenshot(png)
            except Exception:
                pass
            try:
                with open(html, 'w', encoding='utf-8') as f:
                    f.write(self.driver.page_source)
            except Exception:
                pass
            try:
                url = None
                title = None
                try:
                    url = self.driver.current_url
                except Exception:
                    url = None
                try:
                    title = self.driver.title
                except Exception:
                    title = None
                cookie_names = []
                try:
                    cookie_names = sorted({c.get('name') for c in self.driver.get_cookies() if c.get('name')})
                except Exception:
                    cookie_names = []
                with open(meta, 'w', encoding='utf-8') as f:
                    f.write(f"url={url}\n")
                    f.write(f"title={title}\n")
                    f.write(f"cookies={','.join(cookie_names)}\n")
            except Exception:
                pass
        except Exception:
            pass
