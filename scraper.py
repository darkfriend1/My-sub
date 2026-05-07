import requests
import re
import base64

# САМЫЕ ЖИВЫЕ ИСТОЧНИКИ (ТВОИ + ПРОВЕРЕННЫЕ МИРОВЫЕ)
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://gitverse.ru/api/repos/flaafix/AetrisVPN/raw/branch/master/AetrisVPN.txt",
    "https://raw.githubusercontent.com/mueat/V2ray-Configs/main/All_Configs_Sub.txt" # Доп. источник
]

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # Если файл уже в base64 (как некоторые подписки), пробуем его расшифровать
                text = r.text
                if len(text) > 100 and "://" not in text[:50]:
                    try: text = base64.b64decode(text).decode('utf-8')
                    except: pass
                raw_content += text + "\n"
        except: continue

    # Ищем только ВАЛИДНЫЕ ссылки (vless/vmess/ss/trojan)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{50,}'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set(found))
    
    final_configs = []
    for i, node in enumerate(unique_nodes[:100]):
        # Очистка ссылки от мусора в конце (бывает лишний текст)
        clean_node = node.split('\n')[0].split('\r')[0].strip()
        base_link = clean_node.split('#')[0]
        n_up = clean_node.upper()
        
        # Определяем страну для флага
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, c = "🇳🇱", "Netherlands"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        elif any(x in n_up for x in ["US", "USA"]): flag, c = "🇺🇸", "USA"
        else: flag, c = "🌐", "Bypass"

        # Формат как в MadVPN / Fastcon
        name = f"LTE | {flag} {c} | {i+1}"
        final_configs.append(f"{base_link}#{name}")

    # Сохраняем результат
    output_text = "\n".join(final_configs)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    # Кодируем в чистый Base64 для Happ
    encoded = base64.b64encode(output_text.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"[+] Собрано {len(final_configs)} очищенных конфигов.")

if __name__ == "__main__":
    main()
