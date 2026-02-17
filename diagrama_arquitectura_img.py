from PIL import Image, ImageDraw, ImageFont


def crear_diagrama(ruta_salida: str = "diagrama_arquitectura.png") -> None:
    # Crear lienzo
    ancho, alto = 1100, 700
    img = Image.new("RGB", (ancho, alto), color=(15, 23, 42))  # Fondo oscuro
    draw = ImageDraw.Draw(img)

    # Tipografías
    font_title = ImageFont.load_default()
    font_box = ImageFont.load_default()
    font_small = ImageFont.load_default()

    # Colores
    color_box = (30, 64, 175)
    color_box_border = (191, 219, 254)
    color_text = (248, 250, 252)
    color_arrow = (248, 250, 252)
    color_label = (148, 163, 184)

    def get_text_size(text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def draw_centered_box(x, y, w, h, text):
        left = x - w // 2
        top = y - h // 2
        right = x + w // 2
        bottom = y + h // 2
        draw.rounded_rectangle(
            (left, top, right, bottom),
            radius=15,
            fill=color_box,
            outline=color_box_border,
            width=2,
        )
        tw, th = get_text_size(text, font_box)
        draw.text(
            (x - tw / 2, y - th / 2),
            text,
            font=font_box,
            fill=color_text,
        )
        return (x, top, bottom)

    def draw_down_arrow(x, y_start, y_end, label=None):
        draw.line((x, y_start, x, y_end), fill=color_arrow, width=3)
        # Flecha
        head_size = 7
        draw.polygon(
            [
                (x - head_size, y_end - head_size),
                (x + head_size, y_end - head_size),
                (x, y_end + head_size),
            ],
            fill=color_arrow,
        )
        if label:
            tw, th = get_text_size(label, font_small)
            draw.text(
                (x - tw / 2, (y_start + y_end) / 2 - th / 2),
                label,
                font=font_small,
                fill=color_label,
            )

    def draw_horizontal_double(x1, x2, y, label=None):
        draw.line((x1, y, x2, y), fill=color_arrow, width=3)
        # Flechas en ambos extremos
        head = 7
        draw.polygon(
            [(x1 - head, y - head), (x1 - head, y + head), (x1 + head, y)],
            fill=color_arrow,
        )
        draw.polygon(
            [(x2 + head, y - head), (x2 + head, y + head), (x2 - head, y)],
            fill=color_arrow,
        )
        if label:
            tw, th = get_text_size(label, font_small)
            draw.text(
                ((x1 + x2) / 2 - tw / 2, y - th - 4),
                label,
                font=font_small,
                fill=color_label,
            )

    def draw_horizontal_single(x1, x2, y, label=None):
        draw.line((x1, y, x2, y), fill=color_arrow, width=3)
        head = 7
        draw.polygon(
            [(x2 + head, y - head), (x2 + head, y + head), (x2 - head, y)],
            fill=color_arrow,
        )
        if label:
            tw, th = get_text_size(label, font_small)
            draw.text(
                ((x1 + x2) / 2 - tw / 2, y - th - 4),
                label,
                font=font_small,
                fill=color_label,
            )

    # Título
    titulo = "Arquitectura General del Sistema AutoMarketing"
    tw, th = get_text_size(titulo, font_title)
    draw.text(
        ((ancho - tw) / 2, 30),
        titulo,
        font=font_title,
        fill=(248, 250, 252),
    )

    # Coordenadas base
    x_centro = ancho // 2
    y_inicio = 110
    separacion_y = 110

    # 1. Interfaz de Usuario (Frontend)
    _, top_front, bottom_front = draw_centered_box(
        x_centro,
        y_inicio,
        430,
        60,
        "INTERFAZ DE USUARIO (Frontend)",
    )

    # Flecha hacia Backend (HTTP/WebSocket)
    y_backend = y_inicio + separacion_y
    draw_down_arrow(
        x_centro,
        bottom_front + 10,
        y_backend - 40,
        label="HTTP / WebSocket",
    )

    # 2. Servidor de Aplicación (Backend - Flask)
    backend_x = x_centro - 160
    backend_y = y_backend
    draw_centered_box(
        backend_x,
        backend_y,
        430,
        60,
        "SERVIDOR DE APLICACIÓN (Backend - Flask)",
    )

    # 3. Almacenamiento (JSON)
    storage_x = x_centro + 260
    storage_y = backend_y
    draw_centered_box(
        storage_x,
        storage_y,
        280,
        60,
        "ALMACENAMIENTO (JSON)",
    )

    # Flecha doble Backend <-> JSON
    draw_horizontal_double(
        backend_x + 215,
        storage_x - 140,
        backend_y,
        label="Lectura / Escritura de Configuración",
    )

    # Flecha hacia Motor de Automatización (Control de Ejecución)
    y_motor = backend_y + separacion_y
    draw_down_arrow(
        backend_x,
        backend_y + 40,
        y_motor - 40,
        label="Control de Ejecución",
    )

    # 4. Motor de Automatización (Selenium WebDriver)
    _, top_motor, bottom_motor = draw_centered_box(
        backend_x,
        y_motor,
        430,
        60,
        "MOTOR DE AUTOMATIZACIÓN (Selenium WebDriver)",
    )

    # Flecha hacia Navegador (Interacción Web)
    y_navegador = y_motor + separacion_y
    draw_down_arrow(
        backend_x,
        bottom_motor + 10,
        y_navegador - 40,
        label="Interacción Web",
    )

    # 5. Navegador Web (Chrome)
    navegador_x = backend_x
    navegador_y = y_navegador
    draw_centered_box(
        navegador_x,
        navegador_y,
        430,
        60,
        "NAVEGADOR WEB (Google Chrome)",
    )

    # 6. Facebook (destino final)
    facebook_x = navegador_x + 360
    facebook_y = navegador_y
    draw_centered_box(
        facebook_x,
        facebook_y,
        260,
        60,
        "FACEBOOK",
    )

    # Flecha navegador -> Facebook
    draw_horizontal_single(
        navegador_x + 215,
        facebook_x - 130,
        navegador_y,
        label=None,
    )

    img.save(ruta_salida)
    print(f"Diagrama guardado en: {ruta_salida}")


if __name__ == "__main__":
    crear_diagrama()
