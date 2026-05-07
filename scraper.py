import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
TOTAL_GB = 67
USED_GB = 42.0  # Будет отображаться 12,0GB / 500,0GB
TG_NAME = "676767"

SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt",
    "https://t.me/s/ConfigsHUB2",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full"
]

def main():
    # 1. ЗАГОЛОВОК ДЛЯ ШКАЛЫ (Формат как у Vpnchim/Aetris)
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = int(USED_GB * 1024 * 1024 * 1024)
    expire = int(time.time() + (86400 * 30)) # +30 дней
    
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"profile-title: PHANTOM BYPASS\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-description: Переходите в телеграм канал @{TG_NAME} за обновлениями 🔝\n\n"

    # 2. СБОР КОНФИГОВ
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    # Мощная регулярка для захвата всей ссылки
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]+'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set([n for n in found if len(n) > 40]))
    
    # 3. АВТО-ОПРЕДЕЛЕНИЕ СТРАН И ФЛАГОВ
    final_list = []
    for i, node in enumerate(unique_nodes[:150]):
        base_link = node.split('#')[0]
        n_up = node.upper()
        
        # Логика флагов
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["US", "USA"]): flag, c = "🇺🇸", "USA"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, c = "🇳🇱", "Netherlands"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        else: flag, c = "🌐", "Bypass"

        name = f"{flag} LTE | {c} | {i+1}"
        final_list.append(f"{base_link}#{name}")

    # 4. СОХРАНЕНИЕ
    content = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(content)
    
    # Base64 для Happ
    payload = header + content
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! Собрано {len(final_list)} конфигов.")

if __name__ == "__main__":
    main()
