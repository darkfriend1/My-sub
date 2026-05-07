import requests
import re
import base64
import time

# --- ТОЛЬКО НУЖНЫЕ НАСТРОЙКИ ---
TOTAL_GB = 504
USED_GB = 13
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
    # 1. Формируем заголовки для полоски и текста (как на фото)
    total_b = TOTAL_GB * 1024 * 1024 * 1024
    used_b = USED_GB * 1024 * 1024 * 1024
    expire = int(time.time() + (86400 * 30))
    
    header = f"subscription-userinfo: upload=0; download={used_b}; total={total_b}; expire={expire}\n"
    header += f"support-url: https://t.me/{TG_NAME}\n"
    header += f"profile-title: Private Sub\n"
    header += f"profile-description: Переходите в телеграм канал @{TG_NAME} чтобы следить за обновлениями 🔝\n\n"

    # 2. Собираем конфиги
    raw_content = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=10)
            raw_content += r.text + "\n"
        except: continue

    found = re.findall(r'(vless|vmess|ss|trojan)://[^\s"<>#]+', raw_content)
    nodes = list(set(found))
    
    # 3. Переименовываем
    final_list = []
    for i, node in enumerate(nodes[:100]): # Лимит 100 штук
        clean = node.split('#')[0]
        final_list.append(f"{clean}#⚡️ Сервер {i+1}")

    # 4. Финальная сборка
    payload = header + "\n".join(final_list)
    encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')

    with open("sub.txt", "w") as f:
        f.write(encoded)
    print(f"Done! Created {len(final_list)} nodes.")

if __name__ == "__main__":
    main()
