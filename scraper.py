import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
TOTAL_GB = 234
USED_GB = 5.6 # Можешь менять это число для теста шкалы
TG_NAME = "14789"

SOURCES = [
    "https://t.me/s/ConfigsHUB2",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN",
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def main():
    # 1. Формируем заголовок для ШКАЛЫ И КНОПОК
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = int(USED_GB * 1024 * 1024 * 1024)
    expire = int(time.time() + (86400 * 3)) # Истекает через 3 дня
    
    # Сборка по стандарту Vpnchim
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"profile-title: My-Bypass-Sub\n"
    header += f"profile-update-interval: 1\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-description: 🚀 Свежие конфиги от PHANTOM. Обновление каждый час. 🔝\n\n"

    # 2. Сбор контента
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                raw_content += r.text + "\n"
        except: continue

    # Поиск ссылок
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]+'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set([n for n in found if len(n) > 30]))
    
    # 3. Добавляем ФЛАГИ И НАЗВАНИЯ (Авто-определение стран)
    final_list = []
    for i, node in enumerate(unique_nodes[:100]):
        base_link = node.split('#')[0]
        
        # Автоматика флагов по ключевым словам в исходной ссылке
        if "RU" in node.upper() or "RUSSIA" in node.upper():
            flag, country = "🇷🇺", "Russia"
        elif "DE" in node.upper() or "GERMANY" in node.upper():
            flag, country = "🇩🇪", "Germany"
        elif "US" in node.upper() or "USA" in node.upper():
            flag, country = "🇺🇸", "USA"
        elif "NL" in node.upper() or "NETHERLANDS" in node.upper():
            flag, country = "🇳🇱", "Netherlands"
        else:
            flag, country = "🌐", "Auto"

        name = f"{flag} LTE | {country} | Server-{i+1}"
        final_list.append(f"{base_link}#{name}")

    # 4. Сохранение
    raw_output = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(raw_output)
    
    # Упаковка для sub.txt (ОБЯЗАТЕЛЬНО Base64 без лишних символов)
    full_payload = header + raw_output
    encoded = base64.b64encode(full_payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"DONE! Создано {len(final_list)} конфигов с флагами.")

if __name__ == "__main__":
    main()
