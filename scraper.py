import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
TOTAL_GB = 506
USED_GB = 17
TG_NAME = "565666"

SOURCES = [
    "https://t.me/s/ConfigsHUB2",
    "https://t.me/s/halyava_vpnx",
    "https://t.me/s/Farah_VPN",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://cvedcsub.vercel.app/configs/configs.txt"
]

def main():
    # 1. Заголовки для Happ
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = USED_GB * 1024 * 1024 * 1024
    expire = int(time.time() + (86400 * 30))
    
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-title: My-Bypass-Sub\n"
    header += f"profile-description: Свежие конфиги для обхода блокировок @{TG_NAME} 🔝\n\n"

    # 2. Сбор контента
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            raw_content += r.text + "\n"
        except: continue

    # ИСПРАВЛЕННОЕ РЕГУЛЯРНОЕ ВЫРАЖЕНИЕ (берет ссылку целиком)
    pattern = r'(?:vless|vmess|ss|trojan)://[a-zA-Z0-9\-\.\?@&\+=\|/%#:_]+'
    found = re.findall(pattern, raw_content)
    
    # Очистка от дублей и мусора
    nodes = []
    for n in found:
        # Убираем лишние символы в конце, если прилипли
        clean = n.split('<')[0].split('"')[1] if '"' in n else n.split('<')[0]
        if len(clean) > 20: # Ссылка не может быть короче 20 символов
            nodes.append(clean)
    
    unique_nodes = list(set(nodes))
    
    # 3. Формируем список
    final_list = []
    for i, node in enumerate(unique_nodes[:150]):
        # Отрезаем старое имя, если оно было в ссылке
        base_link = node.split('#')[0]
        final_list.append(f"{base_link}#⚡️ Сервер {i+1}")

    # 4. Сохранение
    raw_text_output = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(raw_text_output)
    
    payload = header + raw_text_output
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"DONE! Найдено полноценных конфигов: {len(final_list)}")

if __name__ == "__main__":
    main()
