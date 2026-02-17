from PIL import Image, ImageDraw, ImageFont
import os

def create_er_diagram():
    # Canvas setup
    width = 1000
    height = 800
    background_color = (255, 255, 255)
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)

    # Colors
    header_color = (44, 62, 80) # Dark Blue
    text_color = (0, 0, 0)
    line_color = (0, 0, 0)
    box_border = (0, 0, 0)
    
    try:
        # Try to load a font, otherwise default
        font_header = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 16)
        font_title = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_title = ImageFont.load_default()

    # Title
    draw.text((300, 30), "Modelo de Datos Lógico - AutoMarketing", fill=text_color, font=font_title)

    # Helper function to draw entity tables
    def draw_entity(x, y, title, attributes):
        box_width = 250
        header_height = 40
        row_height = 30
        box_height = header_height + (len(attributes) * row_height)
        
        # Draw Header
        draw.rectangle([x, y, x + box_width, y + header_height], fill=header_color, outline=box_border)
        draw.text((x + 10, y + 8), title, fill=(255, 255, 255), font=font_header)
        
        # Draw Body
        draw.rectangle([x, y + header_height, x + box_width, y + box_height], outline=box_border)
        
        for i, attr in enumerate(attributes):
            curr_y = y + header_height + (i * row_height)
            draw.text((x + 10, curr_y + 5), attr, fill=text_color, font=font_text)
            # Draw separator line
            if i < len(attributes) - 1:
                draw.line([x, curr_y + row_height, x + box_width, curr_y + row_height], fill=(200, 200, 200))
        
        return ((x + box_width // 2, y), (x + box_width // 2, y + box_height)) # Return top and bottom center points

    # Define Entities
    # 1. USUARIO
    user_attrs = ["PK  email : VARCHAR", "    password : VARCHAR"]
    u_top, u_bottom = draw_entity(100, 150, "USUARIO", user_attrs)

    # 2. CAMPAÑA
    campaign_attrs = ["PK  id : INT", "FK  usuario_email : VARCHAR", "    mensaje : TEXT", "    link_promocion : VARCHAR"]
    c_top, c_bottom = draw_entity(100, 450, "CAMPAÑA", campaign_attrs)

    # 3. GRUPO_FACEBOOK
    group_attrs = ["PK  url : VARCHAR", "    nombre : VARCHAR"]
    g_top, g_bottom = draw_entity(600, 150, "GRUPO_FACEBOOK", group_attrs)

    # 4. PUBLICACION (LOG)
    log_attrs = ["PK  id : INT", "FK  campaña_id : INT", "FK  grupo_url : VARCHAR", "    fecha_hora : DATETIME", "    estado : VARCHAR"]
    l_top, l_bottom = draw_entity(600, 450, "PUBLICACION (LOG)", log_attrs)

    # Draw Relationships (Lines)
    
    # Usuario -> Campaña (One to Many)
    # Line from bottom of User to top of Campaign
    draw.line([u_bottom[0], u_bottom[1], c_top[0], c_top[1]], fill=line_color, width=2)
    # Crow's foot notation (simplified)
    draw.text((c_top[0] + 5, c_top[1] - 25), "1:N", fill=text_color, font=font_text)

    # Campaña -> Publicacion (One to Many)
    # Line from right of Campaign to Left of Publicacion
    # Coordinates calculation
    c_right_x = 100 + 250
    c_mid_y = 450 + (40 + 4*30)//2
    l_left_x = 600
    l_mid_y = 450 + (40 + 5*30)//2
    
    draw.line([c_right_x, c_mid_y, l_left_x, l_mid_y], fill=line_color, width=2)
    draw.text(((c_right_x + l_left_x)//2 - 10, c_mid_y - 20), "1:N", fill=text_color, font=font_text)

    # Grupo -> Publicacion (One to Many)
    # Line from bottom of Group to top of Publicacion
    draw.line([g_bottom[0], g_bottom[1], l_top[0], l_top[1]], fill=line_color, width=2)
    draw.text((l_top[0] + 5, l_top[1] - 25), "1:N", fill=text_color, font=font_text)

    # Save
    img.save('modelo_datos_er.png')
    print("Diagrama generado: modelo_datos_er.png")

if __name__ == "__main__":
    create_er_diagram()
