import requests
import re
import base64
import time

# ИСТОЧНИКИ (ТВОИ ЛЮБИМЫЕ)
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def main():
    # 1. Заголовок для шкалы (как на фото MadVPN)
    expire = int(time.time() + 86400 * 30) # +30 дней
    header = f"subscription-userinfo: upload=0; download=0; total=0; expire={expire}\n"
    header += "profile-title: MY BYPASS\n"
    header += "support-url: https://t.me/halyava_vpnx\n\n"

    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    # 2. Поиск ссылок (минимум 60 символов, чтобы отсечь мусор)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set(found))
    
    final_list = []
    for i, node in enumerate(unique_nodes[:100]):
        # Очищаем саму ссылку от лишних знаков в конце
        base_link = node.split('#')[0].strip()
        n_up = node.upper()
        
        # Логика флагов
        if "RU" in n_up or "RUSSIA" in n_up: flag, c = "🇷🇺", "Russia"
        elif "DE" in n_up or "GERMANY" in n_up: flag, c = "🇩🇪", "Germany"
        elif "NL" in n_up or "NETHERLANDS" in n_up: flag, c = "🇳🇱", "Netherlands"
        elif "TR" in n_up or "TURKEY" in n_up: flag, c = "🇹🇷", "Turkey"
        elif "US" in n_up or "USA" in n_up: flag, c = "🇺🇸", "USA"
        else: flag, c = "🌐", "Bypass"

        # Создаем имя: LTE | Страна | Номер (как на твоем фото)
        name = f"LTE | {flag} {c} | {i+1}"
        final_list.append(f"{base_link}#{name}")

    # 3. Сохранение
    output_text = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    # Полный пакет (заголовок + ссылки) в Base64
    full_payload = header + output_text
    encoded = base64.b64encode(full_payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"DONE! Собрано {len(final_list)} конфигов.")

if __name__ == "__main__":
    main()
