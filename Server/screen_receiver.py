import socket
import struct
import pickle
import cv2

class ScreenReceiver:
    def __init__(self, app):
        self.app = app

    def receive_and_display_screen(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.listen(5)

            conn, addr = sock.accept()

            while self.app.server.server_running:
                try:
                    data_len = struct.unpack("L", conn.recv(4))[0]
                    data = b''
                    while len(data) < data_len:
                        chunk = conn.recv(4096)
                        if not chunk:
                            return
                        data += chunk
                    frame = pickle.loads(data)
                    cv2.imshow('Laptop Screen', frame)
                    if cv2.waitKey(1) == ord('q'):
                        break
                except Exception as e:
                    print(f"[ERROR] Exception: {e}")
                    break

            conn.close()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"[ERROR] Exception: {e}")
