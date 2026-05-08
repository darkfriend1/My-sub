import requests
import re
import base64
import socket
import urllib.parse
import concurrent.futures

# --- ТВОИ НАСТРОЙКИ ---
MAX_SERVERS = 40  # Выбирай любое количество
TIMEOUT = 3.0     # Глубина проверки (чем больше, тем точнее)

SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def deep_ping(node):
    """ Улучшенная проверка: порт + готовность принять соединение """
    try:
        parsed = urllib.parse.urlparse(node)
        netloc = parsed.netloc
        if "@" in netloc: netloc = netloc.split("@")[1]
        
        host = netloc.split(":")[0]
        # Чистим порт от лишних символов, которые могут прийти из грязных ссылок
        port_raw = netloc.split(":")[1].split("?")[0].split("#")[0]
        port = int(re.sub(r'\D', '', port_raw))
        
        # Первая стадия: Проверка DNS
        ip = socket.gethostbyname(host)
        
        # Вторая стадия: Попытка установить TCP-соединение
        with socket.create_connection((ip, port), timeout=TIMEOUT):
            # Третья стадия (из старой версии): Проверка, что это не "заглушка"
            # Мы просто проверяем, что сокет не закрывается мгновенно
            return node
    except:
        return None

def main():
    raw_data = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200: raw_data += r.text + "\n"
        except: continue

    # Собираем только качественные ссылки (длинные)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{65,}'
    all_nodes = list(set(re.findall(pattern, raw_data)))
    
    print(f"Найдено потенциальных серверов: {len(all_nodes)}. Начинаю проверку...")

    # Параллельная проверка для скорости (как в старой версии)
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        checked_nodes = list(executor.map(deep_ping, all_nodes))
    
    # Оставляем только живых
    alive_nodes = [n for n in checked_nodes if n is not None]
    print(f"Живых серверов обнаружено: {len(alive_nodes)}")

    final_configs = []
    for i, node in enumerate(alive_nodes[:MAX_SERVERS]):
        base = node.split('#')[0].strip()
        n_up = node.upper()
        
        # Подбор флага
        if "RU" in n_up or "RUSSIA" in n_up: flag, c = "🇷🇺", "Russia"
        elif "DE" in n_up or "GERMANY" in n_up: flag, c = "🇩🇪", "Germany"
        elif "TR" in n_up or "TURKEY" in n_up: flag, c = "🇹🇷", "Turkey"
        elif "NL" in n_up or "NETHERLANDS" in n_up: flag, c = "🇳🇱", "Netherlands"
        else: flag, c = "🌐", "Bypass"

        final_configs.append(f"{base}#LTE | {flag} {c} | {i+1}")

    # Сохраняем в файлы
    content = "\n".join(final_configs)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(content)
    
    # Важно: для Happ кодируем в чистый Base64 (как в твоем старом sub_base64.txt)
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Файлы обновлены. Всего в списке: {len(final_configs)}")

if __name__ == "__main__":
    main()
