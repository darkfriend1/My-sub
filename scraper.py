import requests
import re
import base64

# Источники, которые ты предоставил + твои старые
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN"
]

def main():
    # 1. Заголовок (Без лимитов, как ты просил)
    header = "profile-title: WWYOUVPN\n"
    header += "profile-update-interval: 1\n"
    header += "support-url: https://t.me/NOOOO\n\n"

    # 2. Сбор сырых данных
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                raw_content += r.text + "\n"
        except: continue

    # 3. Улучшенный поиск (фильтруем мусор, берем только полные ссылки)
    # Ищем ссылки vless/vmess/ss/trojan длиной не менее 60 символов
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set(found))
    
    # 4. Форматирование под Fastcon: LTE | Country | Number
    final_list = []
    for i, node in enumerate(unique_nodes[:100]):
        base_link = node.split('#')[0]
        n_up = node.upper()
        
        # Логика определения страны для флага
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, country = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, country = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["US", "USA"]): flag, country = "🇺🇸", "USA"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, country = "🇳🇱", "Netherlands"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, country = "🇹🇷", "Turkey"
        else: flag, country = "🌐", "Bypass"

        # Создаем имя как на фото 1000009207
        name = f"LTE | {country} | {i+1}"
        final_list.append(f"{base_link}#{name}")

    # 5. Запись файлов
    # configs.txt для тебя (открытый вид)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(final_list))
    
    # sub.txt для Happ (Base64)
    payload = header + "\n".join(final_list)
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"[+] Сгенерировано {len(final_list)} чистых конфигов.")

if __name__ == "__main__":
    main()
