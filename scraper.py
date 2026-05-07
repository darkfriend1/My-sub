import requests
import re
import base64
import socket
import time
from datetime import datetime, timedelta

# --- НАСТРОЙКИ ПОД ТЕБЯ ---
LIMIT = 100            # Макс. количество рабочих нод
TOTAL_GB = 500         # Лимит на фото
USED_GB = 12           # Расход как на фото
EXPIRE_DAYS = 24       # Срок действия
TG_LINK = "https://t.me/+dGgfc2EX3uoxN2Fi" # Твой канал для кнопки
INF_LINK = "https://t.me/your_info"  # Твоя ссылка для инфо

# ТВОИ ИСТОЧНИКИ (Объединенные)
SOURCES = [
    "https://t.me/s/ConfigsHUB2",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://cvedcsub.vercel.app/configs/configs.txt"
]

def check_port(host, port):
    try:
        s = socket.create_connection((host, int(port)), timeout=1.5)
        s.close()
        return True
    except:
        return False

def generate_header():
    total = TOTAL_GB * 1024 * 1024 * 1024
    used = USED_GB * 1024 * 1024 * 1024
    expire = int(time.time() + (86400 * EXPIRE_DAYS))
    return f"upload=0; download={used}; total={total}; expire={expire}"

def main():
    print("[*] PHANTOM: Starting global sync...")
    raw_content = ""
    
    # 1. Сбор данных
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            raw_content += r.text + "\n"
            print(f"[+] Synced: {url[:30]}...")
        except: continue

    # 2. Поиск ссылок
    found = re.findall(r'(vless|vmess|ss|trojan)://[^\s"<>#]+', raw_content)
    unique_nodes = list(set(found))
    valid_nodes = []

    # 3. Формирование ПАНЕЛИ ИНФОРМАЦИИ (как на фото)
    exp_date = (datetime.now() + timedelta(days=EXPIRE_DAYS)).strftime("%d.%m.%Y")
    info_remarks = f"📊 [{USED_GB}GB/{TOTAL_GB}GB] | Exp: {exp_date}"
    # Техническая нода для кнопок TG и Info
    info_node = f"vless://info@127.0.0.1:443?encryption=none&security=none#{info_remarks}"
    valid_nodes.append(info_node)

    print(f"[*] Found {len(unique_nodes)} nodes. Validating...")

    # 4. Проверка и Очистка мусора
    for node in unique_nodes:
        if len(valid_nodes) >= LIMIT: break
        try:
            parts = re.search(r'@?([^:]+):([0-9]+)', node)
            if parts:
                host, port = parts.group(1), parts.group(2)
                if check_port(host, port):
                    clean_link = node.split('#')[0]
                    # Присвоение имени и флага (Happ распознает флаг по названию страны)
                    name = f"⚡️ VPN | SERVER-{len(valid_nodes)}"
                    valid_nodes.append(f"{clean_link}# {name}")
        except: continue

    # 5. Сборка финального файла с мета-данными
    # Эти заголовки Happ превратит в кнопки и полоску ГБ
    header_info = f"profile-title: PHANTOM_FREE\n"
    header_info += f"subscription-userinfo: {generate_header()}\n"
    header_info += f"support-url: {TG_LINK}\n"
    header_info += f"profile-web-page-url: {INF_LINK}\n\n"

    final_content = header_info + "\n".join(valid_nodes)
    
    # Кодирование в Base64 (Зашифрованная подписка)
    encoded = base64.b64encode(final_content.encode()).decode()

    with open("sub.txt", "w") as f:
        f.write(encoded)
    
    print(f"[!] COMPLETE: {len(valid_nodes)} nodes saved to sub.txt")

if __name__ == "__main__":
    main()
