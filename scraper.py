import requests
import re
import base64
import socket
import urllib.parse
import concurrent.futures

# --- ТВОИ НАСТРОЙКИ ---
MAX_SERVERS = 30  # ТУТ МЕНЯЙ КОЛИЧЕСТВО
TIMEOUT = 2.5     # Скорость проверки

SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def check_node(node):
    """ Глубокая проверка порта из твоего старого метода """
    try:
        p = urllib.parse.urlparse(node)
        host = p.netloc.split('@')[-1].split(':')[0]
        port = int(re.sub(r'\D', '', p.netloc.split(':')[-1].split('?')[0]))
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return node
    except: return None

def main():
    raw = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw += r.text + "\n"
        except: continue

    found = list(set(re.findall(r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}', raw)))
    
    # Многопоточный чек (как в старой версии)
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as ex:
        valid = [n for n in ex.map(check_node, found) if n]

    final = []
    for i, node in enumerate(valid[:MAX_SERVERS]):
        base = node.split('#')[0].strip()
        n_up = node.upper()
        # Логика флагов
        if "RU" in n_up: f, c = "🇷🇺", "Russia"
        elif "DE" in n_up: f, c = "🇩🇪", "Germany"
        elif "US" in n_up: f, c = "🇺🇸", "USA"
        else: f, c = "🌐", "Bypass"
        
        final.append(f"{base}#LTE | {f} {c} | {i+1}")

    out = "\n".join(final)
    with open("configs.txt", "w", encoding='utf-8') as f: f.write(out)
    with open("sub.txt", "w", encoding='utf-8') as f: 
        f.write(base64.b64encode(out.encode()).decode())

if __name__ == "__main__":
    main()
