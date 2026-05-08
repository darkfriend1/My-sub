import requests
import re
import base64
import socket
import urllib.parse

SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def is_alive(node):
    try:
        # Извлекаем адрес и порт из ссылки
        parsed = urllib.parse.urlparse(node)
        netloc = parsed.netloc
        if "@" in netloc: netloc = netloc.split("@")[1]
        
        host = netloc.split(":")[0]
        port = int(netloc.split(":")[1].split("?")[0])
        
        # Проверка TCP порта
        with socket.create_connection((host, port), timeout=2):
            return True
    except:
        return False

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = list(set(re.findall(pattern, raw_content)))
    
    print(f"Найдено {len(found)} кандидатов. Начинаю проверку...")
    
    final_list = []
    count = 1
    for node in found:
        if is_alive(node):
            base_link = node.split('#')[0].strip()
            n_up = node.upper()
            
            # Флаги
            if "RU" in n_up or "RUSSIA" in n_up: flag, c = "🇷🇺", "Russia"
            elif "DE" in n_up or "GERMANY" in n_up: flag, c = "🇩🇪", "Germany"
            elif "TR" in n_up or "TURKEY" in n_up: flag, c = "🇹🇷", "Turkey"
            else: flag, c = "🌐", "Bypass"

            final_list.append(f"{base_link}#LTE | {flag} {c} | {count}")
            count += 1
            if count > 50: break # Ограничим до 50 лучших для скорости

    output_text = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    encoded = base64.b64encode(output_text.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Успех! В подписку попало {len(final_list)} живых серверов.")

if __name__ == "__main__":
    main()
