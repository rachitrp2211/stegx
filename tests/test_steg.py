from stegx import image_lsb

# Path to your test image
input_img = "examples/test.png"     # your original image
stego_img = "examples/stego.png"    # output after hiding

# Step 1: Hide a message
secret_message = b"MySecret123"
image_lsb.embed_png(input_img, stego_img, secret_message)
print(f"Message embedded into {stego_img}")

# Step 2: Extract the message back
extracted = image_lsb.extract_png(stego_img)
print("Extracted message:", extracted)

