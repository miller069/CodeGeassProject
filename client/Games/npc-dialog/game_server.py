"""
game_server.py - Python multiplayer server for the NPC dialog game

Run this once on ONE machine. Everyone else connects to that machine's IP.

Usage:
    python game_server.py
    python game_server.py --port 8080

How to find your IP so teammates can connect:
    Linux/Mac:  hostname -I
    Windows:    ipconfig
"""

import socket
import threading
import argparse
import time

# How often (seconds) the server broadcasts everyone's position to all clients
BROADCAST_INTERVAL = 0.05   # 20 updates per second


class GameServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port

        # player_id -> {'conn', 'addr', 'name', 'x', 'y', 'character_type', 'status'}
        self.players = {}
        self.next_id = 1
        self.lock = threading.Lock()

        self.running = False

    # ------------------------------------------------------------------
    # Start / stop
    # ------------------------------------------------------------------

    def start(self):
        self.running = True
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(32)

        print(f"Server started on port {self.port}")
        print(f"Share YOUR IP address with teammates so they can connect")
        print(f"  Linux/Mac:  run 'hostname -I' in another terminal")
        print(f"  Windows:    run 'ipconfig' in another terminal")
        print(f"Waiting for players...")

        # Broadcast loop runs in background
        broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        broadcast_thread.start()

        # Accept new connections in the main thread
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

    # ------------------------------------------------------------------
    # Client handler - runs in its own thread per connected player
    # ------------------------------------------------------------------

    def _handle_client(self, conn, addr):
        # Assign a unique ID to this player
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

        # Tell the client what their ID is
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

        except Exception as e:
            pass  # client disconnected or network error
        finally:
            with self.lock:
                if player_id in self.players:
                    del self.players[player_id]
            conn.close()
            print(f"Player {player_id} disconnected  ({len(self.players)} remaining)")

    # ------------------------------------------------------------------
    # Message processing
    # ------------------------------------------------------------------

    def _process_message(self, player_id, msg):
        # Format: UPDATE|<id>|<x>|<y>|<name>|<character_type>|<status>
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

    # ------------------------------------------------------------------
    # Broadcast - send all player positions to everyone at 20hz
    # ------------------------------------------------------------------

    def _broadcast_loop(self):
        while self.running:
            time.sleep(BROADCAST_INTERVAL)
            self._broadcast_state()

    def _broadcast_state(self):
        with self.lock:
            if not self.players:
                return

            # Build STATE message in TEXT format:
            # STATE||id|name|x|y|socket_num|character_type|status||id|name|...
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

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _send(self, conn, msg):
        conn.send((msg + '\n').encode('utf-8'))


# ------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='NPC Dialog Game Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on (default: 8080)')
    args = parser.parse_args()

    server = GameServer(port=args.port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.stop()
