# stegx/cli.py
import argparse
from pathlib import Path
from stegx import image_lsb, crypto_utils

def main():
    parser = argparse.ArgumentParser(description="stegx - LSB steganography (message/file) with password")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # hide: supports --file or --message
    p_hide = sub.add_parser("hide", help="Hide a message or a file inside an image")
    p_hide.add_argument("input", help="Input cover PNG image")
    p_hide.add_argument("output", help="Output stego PNG image")
    grp = p_hide.add_mutually_exclusive_group(required=True)
    grp.add_argument("--file", "-f", help="Path to file to hide (binary)")
    grp.add_argument("--message", "-m", help="Text message to hide")
    p_hide.add_argument("--password", "-p", required=True, help="Password to encrypt hidden data")

    # reveal
    p_reveal = sub.add_parser("reveal", help="Reveal hidden data from a stego image")
    p_reveal.add_argument("input", help="Input stego PNG image")
    p_reveal.add_argument("--password", "-p", required=True, help="Password to decrypt")
    p_reveal.add_argument("--out", "-o", help="If provided and data is a file, write output to this path")

    args = parser.parse_args()

    if args.cmd == "hide":
        # build plaintext: [2-byte filename length][filename bytes][payload bytes]
        if args.file:
            fpath = Path(args.file)
            if not fpath.exists():
                raise SystemExit(f"File not found: {args.file}")
            payload = fpath.read_bytes()
            filename = fpath.name.encode("utf-8")
        else:
            payload = args.message.encode("utf-8")
            filename = b""

        fname_len = len(filename).to_bytes(2, "big")
        plaintext = fname_len + filename + payload

        # encrypt
        encrypted = crypto_utils.encrypt_bytes(plaintext, args.password)

        # embed into image
        image_lsb.hide_message(args.input, args.output, encrypted)
        print(f"[+] Hidden {'file' if args.file else 'message'} into {args.output}")

    elif args.cmd == "reveal":
        # extract encrypted bytes
        encrypted = image_lsb.reveal_message(args.input)

        # decrypt
        try:
            plaintext = crypto_utils.decrypt_bytes(encrypted, args.password)
        except Exception as e:
            raise SystemExit(f"Decryption failed: {e}")

        # parse filename and payload
        if len(plaintext) < 2:
            raise SystemExit("Corrupt data (no filename length)")

        fname_len = int.from_bytes(plaintext[:2], "big")
        offset = 2
        filename = plaintext[offset: offset + fname_len].decode("utf-8") if fname_len > 0 else ""
        offset += fname_len
        data = plaintext[offset:]

        if filename:
            out_path = Path(args.out) if args.out else Path(filename)
            out_path.write_bytes(data)
            print(f"[+] Recovered file written to: {out_path}")
        else:
            # treat as text and print (safe decode)
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                # fallback: print raw bytes repr
                print("[!] Decrypted payload is not UTF-8 text. Use --out to save it as a file.")
                print(repr(data))
                return
            print("[+] Recovered message:")
            print(text)

if __name__ == "__main__":
    main()
