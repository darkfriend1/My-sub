import requests
import re
import base64

# ТВОИ ПРОВЕРЕННЫЕ ИСТОЧНИКИ
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt"
]

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200: raw_content += r.text + "\n"
        except: continue

    # Ищем только полноценные конфиги (длиннее 60 символов)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{60,}'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set(found))
    
    final_configs = []
    for i, node in enumerate(unique_nodes[:150]):
        base_link = node.split('#')[0]
        n_up = node.upper()
        
        # Подбор флага как в твоих примерах
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, c = "🇳🇱", "Netherlands"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        elif any(x in n_up for x in ["US", "USA"]): flag, c = "🇺🇸", "USA"
        else: flag, c = "🌐", "Bypass"

        # Формат имени: LTE | Флаг Страна | Номер
        name = f"LTE | {flag} {c} | {i+1}"
        final_configs.append(f"{base_link}#{name}")

    # Сохраняем чистый список для отладки
    output_text = "\n".join(final_configs)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    # Кодируем ВЕСЬ список в Base64 без лишних заголовков (как в твоем старом sub_base64.txt)
    encoded = base64.b64encode(output_text.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"[+] Собрано {len(final_configs)} конфигов.")

if __name__ == "__main__":
    main()
