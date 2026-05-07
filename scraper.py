import requests
import re
import base64

# ТВОИ СТАРЫЕ ПРОВЕРЕННЫЕ ИСТОЧНИКИ (Без ТГ)
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def main():
    # 1. Заголовок (Без лимитов, как на последних фото)
    header = "profile-title: MY BYPASS\n"
    header += "support-url: https://t.me/vbvbfdry\n\n"

    # 2. Сбор данных
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    # 3. Фильтр: только длинные рабочие ссылки (от 60 символов)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set(found))
    
    # 4. Флаги и формат имен (LTE | Флаг Страна | №)
    final_list = []
    for i, node in enumerate(unique_nodes[:100]):
        base_link = node.split('#')[0]
        n_up = node.upper()
        
        # Определение страны
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, c = "🇳🇱", "Netherlands"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        elif any(x in n_up for x in ["US", "USA"]): flag, c = "🇺🇸", "USA"
        else: flag, c = "🌐", "Bypass"

        # Формат как на твоих фото-примерах
        name = f"LTE | {flag} {c} | {i+1}"
        final_list.append(f"{base_link}#{name}")

    # 5. Сохранение
    content = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(content)
    
    payload = header + content
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! Собрано {len(final_list)} конфигов.")

if __name__ == "__main__":
    main()
