import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os

st.set_page_config(page_title="ID Card Generator", layout="centered")

st.title("🪪 ID Card Generator")
st.markdown("Upload your **template** and **photo**, and get a personalized ID card.")

# Upload files
template_file = st.file_uploader("📁 Upload your ID card template (PNG)", type=["png"])
photo_file = st.file_uploader("📸 Upload your photo (JPG or PNG)", type=["jpg", "jpeg", "png"])

# Text inputs
name = st.text_input("Enter Name:", "MALYA")
id_number = st.text_input("Enter ID:", "05024302022")
department = st.text_input("Enter Department:", "BCA")

# Button
if st.button("Generate ID Card"):
    if template_file and photo_file:
        # Load images
        template = Image.open(template_file).convert("RGBA")
        photo = Image.open(photo_file).convert("RGBA").resize((120, 120))

        # Create circular mask
        mask = Image.new("L", photo.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, photo.size[0], photo.size[1]), fill=255)

        # White background for photo
        photo_bg = Image.new("RGBA", photo.size, (255, 255, 255, 255))
        photo_bg.paste(photo, (0, 0), mask)

        # Paste circular photo onto template
        template.paste(photo_bg, (60, 160), mask)

        # Load font
        try:
            font_large = ImageFont.truetype("assets/Roboto-Bold.ttf", 28)
            font_small = ImageFont.truetype("assets/Roboto-Bold.ttf", 22)
        except:
            font_large = font_small = ImageFont.load_default()

        # Draw text
        draw = ImageDraw.Draw(template)
        draw.text((220, 200), f"Name: {name}", fill="black", font=font_large)
        draw.text((220, 240), f"ID: {id_number}", fill="black", font=font_small)
        draw.text((220, 280), f"Dept: {department}", fill="black", font=font_small)

        # Save output
        output = io.BytesIO()
        template.save(output, format='PNG')
        output.seek(0)

        # Display and download
        st.image(template, caption="🖼 Final ID Card", use_container_width=True)
        st.download_button("📥 Download ID Card", data=output, file_name="ID_Card.png", mime="image/png")
    else:
        st.error("❌ Please upload both the template and the photo.")



