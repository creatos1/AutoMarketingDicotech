def mostrar_diagrama():
    diagrama = r"""
    [ INTERFAZ DE USUARIO (Frontend) ]
            |
            |  (HTTP / WebSocket)
            v
    [ SERVIDOR DE APLICACIÓN (Backend - Flask) ] <---> [ ALMACENAMIENTO (JSON) ]
            |
            |  (Control de Ejecución)
            v
    [ MOTOR DE AUTOMATIZACIÓN (Selenium WebDriver) ]
            |
            |  (Interacción Web)
            v
    [ NAVEGADOR WEB (Google Chrome) ] ---> [ FACEBOOK ]
    """
    print(diagrama)


if __name__ == "__main__":
    mostrar_diagrama()