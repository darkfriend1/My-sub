import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
MAX_SERVERS = 50 
# Новые, супер-свежие источники
SOURCES = [
    "https://raw.githubusercontent.com/yror382-netizen/Vpnchim/refs/heads/main/Sjsh",
    "https://raw.githubusercontent.com/bikun-bikun/vless-daily/main/vless.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/master/sub/shadowsocks",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/master/sub/vless",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/master/sub/vmess",
    "https://raw.githubusercontent.com/vfarid/v2ray-worker-sub/master/sub/trojan"
]

def main():
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                content = r.text
                # Если источник в base64 — расшифровываем
                if "://" not in content[:50]:
                    try: content = base64.b64decode(content).decode('utf-8')
                    except: pass
                raw_content += content + "\n"
        except: continue

    # Собираем ссылки (фильтруем только по длине, не пингуем — Happ сам проверит)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]{50,}'
    found = list(set(re.findall(pattern, raw_content)))
    
    final_configs = []
    for i, node in enumerate(found[:MAX_SERVERS]):
        base_link = node.split('#')[0].strip()
        n_up = node.upper()
        
        # Определение флага
        if any(x in n_up for x in ["RU", "RUSSIA"]): flag, c = "🇷🇺", "Russia"
        elif any(x in n_up for x in ["DE", "GERMANY"]): flag, c = "🇩🇪", "Germany"
        elif any(x in n_up for x in ["TR", "TURKEY"]): flag, c = "🇹🇷", "Turkey"
        elif any(x in n_up for x in ["NL", "NETHERLANDS"]): flag, c = "🇳🇱", "Netherlands"
        else: flag, c = "🌐", "Bypass"

        name = f"LTE | {flag} {c} | {i+1}"
        final_configs.append(f"{base_link}#{name}")

    output_text = "\n".join(final_configs)
    
    # Сохраняем configs.txt
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(output_text)
    
    # Кодируем в чистый Base64 для Happ (как в старом проекте)
    encoded = base64.b64encode(output_text.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! Собрано {len(final_configs)} свежих конфигов.")

if __name__ == "__main__":
    main()
