# game_server.py
# Ibrahim Chatila
# run this on one machine and share your IP with teammates so they can join
# find your IP: hostname -I on linux, ipconfig on windows
# usage: python game_server.py
# game serverrrr

import socket
import threading
import argparse
import time

# how often the server sends everyone's position to all players (seconds)
BROADCAST_INTERVAL = 0.05


class GameServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port

        # stores each connected player by their id
        self.players = {}
        self.next_id = 1
        self.lock = threading.Lock()

        self.running = False

    def start(self):
        self.running = True
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(32)

        print(f"Server started on port {self.port}")
        print(f"Share your IP with teammates so they can connect")
        print(f"  Linux/Mac: hostname -I")
        print(f"  Windows: ipconfig")
        print(f"Waiting for players...")

        broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        broadcast_thread.start()

        while self.running:
            try:
                conn, addr = self.server_sock.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                client_thread.start()
            except OSError:
                break

    def stop(self):
        self.running = False
        self.server_sock.close()
        print("Server stopped.")

    def _handle_client(self, conn, addr):
        with self.lock:
            player_id = self.next_id
            self.next_id += 1
            self.players[player_id] = {
                'conn': conn,
                'addr': addr,
                'name': f'Player{player_id}',
                'x': 128.0,
                'y': 128.0,
                'character_type': '',
                'status': 'down',
            }

        self._send(conn, f"CONNECTED|{player_id}")
        print(f"Player {player_id} connected from {addr}")

        buffer = ""
        try:
            while self.running:
                data = conn.recv(4096).decode('utf-8', errors='ignore')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self._process_message(player_id, line.strip())
        except Exception:
            pass
        finally:
            with self.lock:
                if player_id in self.players:
                    del self.players[player_id]
            conn.close()
            print(f"Player {player_id} disconnected ({len(self.players)} remaining)")

    def _process_message(self, player_id, msg):
        # messages from clients come in as UPDATE|id|x|y|name|character_type|status
        if not msg.startswith("UPDATE|"):
            return

        parts = msg.split('|')
        if len(parts) < 5:
            return

        try:
            x = float(parts[2])
            y = float(parts[3])
            name = parts[4] if len(parts) > 4 else f'Player{player_id}'
            character_type = parts[5] if len(parts) > 5 else ''
            status = parts[6] if len(parts) > 6 else 'down'

            with self.lock:
                if player_id in self.players:
                    self.players[player_id].update({
                        'name': name,
                        'x': x,
                        'y': y,
                        'character_type': character_type,
                        'status': status,
                    })
        except (ValueError, IndexError):
            pass

    def _broadcast_loop(self):
        while self.running:
            time.sleep(BROADCAST_INTERVAL)
            self._broadcast_state()

    def _broadcast_state(self):
        with self.lock:
            if not self.players:
                return

            # build the state message and send it to every connected player
            parts = ["STATE"]
            for pid, p in self.players.items():
                entry = f"{pid}|{p['name']}|{p['x']}|{p['y']}|{pid}|{p['character_type']}|{p['status']}"
                parts.append(entry)

            state_msg = "||".join(parts)

            dead = []
            for pid, p in self.players.items():
                try:
                    self._send(p['conn'], state_msg)
                except Exception:
                    dead.append(pid)

            for pid in dead:
                del self.players[pid]

    def _send(self, conn, msg):
        conn.send((msg + '\n').encode('utf-8'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()

    server = GameServer(port=args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop()
