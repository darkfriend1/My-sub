import requests
import re
import base64
import socket
import urllib.parse
import concurrent.futures

# --- НАСТРОЙКИ ---
MAX_SERVERS = 80  # Измени это число (сколько рабочих серверов хочешь получить)
CHECK_TIMEOUT = 2.5 # Секунды на проверку одного сервера

SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def check_server(node):
    """ Проверка доступности порта сервера """
    try:
        parsed = urllib.parse.urlparse(node)
        netloc = parsed.netloc
        if "@" in netloc: netloc = netloc.split("@")[1]
        
        host = netloc.split(":")[0]
        port_part = netloc.split(":")[1].split("?")[0].split("#")[0]
        port = int(port_part)
        
        with socket.create_connection((host, port), timeout=CHECK_TIMEOUT):
            return node
    except:
        return None

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    # Собираем все уникальные ссылки
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = list(set(re.findall(pattern, raw_content)))
    
    print(f"Найдено {len(found)} серверов. Запускаю глубокую проверку...")

    active_configs = []
    # Используем многопоточность для ускорения пинговки
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_server, found))
        
    valid_nodes = [r for r in results if r is not None]

    for i, node in enumerate(valid_nodes[:MAX_SERVERS]):
        base_link = node.split('#')[0].strip()
        n_up = node.upper()
        
        # Определяем флаг
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        elif any(x in n_up for x in ["US", "USA"]): flag, c = "🇺🇸", "USA"
        else: flag, c = "🌐", "Bypass"

        final_name = f"LTE | {flag} {c} | {i+1}"
        active_configs.append(f"{base_link}#{final_name}")

    # Сохранение результатов
    output_text = "\n".join(active_configs)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    encoded = base64.b64encode(output_text.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! В подписку попало {len(active_configs)} реально живых серверов.")

if __name__ == "__main__":
    main()
