import requests
import re
import base64
import time

# --- НАСТРОЙКИ ---
TOTAL_GB = 508
USED_GB = 14
TG_NAME = "serojka"

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
    # 1. Заголовки для Happ (Полоска 12/500 ГБ)
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = USED_GB * 1024 * 1024 * 1024
    expire = int(time.time() + (86400 * 30))
    
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-title: My-Bypass-Sub\n"
    header += f"profile-description: Свежие конфиги для обхода блокировок @{TG_NAME} 🔝\n\n"

    # 2. Сбор всех ссылок из твоих источников
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            raw_content += r.text + "\n"
        except: continue

    # Ищем протоколы: vless, vmess, ss, trojan
    found = re.findall(r'(vless|vmess|ss|trojan)://[^\s"<>#]+', raw_content)
    nodes = list(set(found)) # Убираем дубликаты
    
    # 3. Формируем список ссылок (с именами)
    final_list = []
    for i, node in enumerate(nodes[:150]): # Оставляем топ-150
        clean = node.split('#')[0]
        # Сохраняем формат ссылки, который ты просил
        final_list.append(f"{clean}#⚡️ Сервер {i+1}")

    # 4. СОХРАНЯЕМ В ДВА ФАЙЛА
    
    # Файл №1: configs.txt (ОТКРЫТЫЕ ССЫЛКИ ДЛЯ ТЕБЯ)
    raw_text_output = "\n".join(final_list)
    with open("configs.txt", "w", encoding='utf-8') as f:
        f.write(raw_text_output)
    
    # Файл №2: sub.txt (ЗАШИФРОВАННЫЙ ДЛЯ HAPP С ПОЛОСКОЙ ГБ)
    payload = header + raw_text_output
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    with open("sub.txt", "w", encoding='utf-8') as f:
        f.write(encoded)

    print(f"Готово! В configs.txt и sub.txt сохранено {len(final_list)} конфигов.")

if __name__ == "__main__":
    main()
