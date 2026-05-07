import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
TOTAL_GB = 54
USED_GB = 16
TG_NAME = "5656565666"

SOURCES = [
    "https://t.me/s/ConfigsHUB2",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt"
]

def main():
    # 1. Заголовки (Лимиты)
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = USED_GB * 1024 * 1024 * 1024
    expire = int(time.time() + (86400 * 30))
    
    # Формируем четкий заголовок
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-title: PHANTOM-BYPASS\n"
    header += f"profile-description: @{TG_NAME} | Обход блокировок 🔝\n\n"

    # 2. Сбор свежих данных
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                raw_content += r.text + "\n"
        except: continue

    # Улучшенный поиск ссылок
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]+'
    found = re.findall(pattern, raw_content)
    unique_nodes = list(set([n for n in found if len(n) > 30]))
    
    # 3. Добавляем ФЛАГИ и ИМЕНА
    # Happ ставит флаг, если в имени есть [RU], [US] и т.д.
    final_list = []
    for i, node in enumerate(unique_nodes[:100]):
        base_link = node.split('#')[0]
        # Добавляем [RU] для флага России и молнию
        name = f" [RU] PHANTOM SERVER №{i+1}"
        final_list.append(f"{base_link}#{name}")

    # 4. Сохранение
    raw_output = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(raw_output)
    
    # Полная сборка для sub.txt
    full_payload = header + raw_output
    encoded = base64.b64encode(full_payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! Найдено {len(final_list)} конфигов.")

if __name__ == "__main__":
    main()
