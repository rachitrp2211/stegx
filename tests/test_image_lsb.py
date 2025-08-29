import os
from stegx import image_lsb

def test_hide_and_reveal_message(tmp_path):
    # Use a small image for testing
    in_img = "examples/test.png"   # make sure you keep a test image
    out_img = tmp_path / "out.png"
    message = b"hello steganography"

    # Hide
    image_lsb.hide_message(in_img, str(out_img), message)

    # Reveal
    revealed = image_lsb.reveal_message(str(out_img))

    assert revealed == message
