import qrcode

# Define the data for the QR code (e.g., URL of your API endpoint)
data = "http://127.0.0.1:8000/api/success/image"

# Create QR code instance
qr = qrcode.QRCode(
    version=1,  # Controls size of the QR code (1 is smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in pixels
    border=4,  # Width of the border (minimum is 4)
)

# Add data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR code
img = qr.make_image(fill="black", back_color="white")

# Save the image to a file
img.save("success_image_qr.png")

print("QR code generated and saved as 'success_image_qr.png'")
