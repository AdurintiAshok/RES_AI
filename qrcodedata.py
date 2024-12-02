import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Title of the application
st.title("QR Code Generator")

# Provide an option to choose between text or URL input, passing a unique key
input_option = st.radio("Choose Input Type", ('Text', 'URL'), key="input_type")

# Based on the selection, prompt the user to input text or URL
if input_option == 'Text':
    user_input = st.text_area("Enter the Text", "Hello, QR Code!", key="text_input")
elif input_option == 'URL':
    user_input = st.text_input("Enter the URL", "https://example.com", key="url_input")

# Button to generate QR code
if st.button("Generate QR Code"):
    if user_input:
        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )
        qr.add_data(user_input)
        qr.make(fit=True)
        
        # Create an image from the QR code
        img = qr.make_image(fill='black', back_color='white')

        # Convert the PIL image to a byte stream
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Display the QR code image
        st.image(img_byte_arr, caption="Generated QR Code", use_column_width=True)
    else:
        st.warning("Please enter text or URL to generate a QR code.")
