import requests
import re
import base64
import socket
import urllib.parse
import concurrent.futures

# =========================
# ⚙️ НАСТРОЙКИ
# =========================

MAX_SERVERS = 49
TIMEOUT = 3.0

SOURCES = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://cvedcsub.vercel.app/configs/configs.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt"
]

# =========================
# 📥 ЗАГРУЗКА
# =========================

def fetch_sources():
    raw = ""
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                raw += r.text + "\n"
        except:
            pass
    return raw

# =========================
# 🔍 ПАРСЕР
# =========================

def extract_nodes(raw):
    pattern = r'(?:vless|vmess|ss|trojan)://[^\s]{20,}'
    nodes = list(set(re.findall(pattern, raw)))
    return nodes

# =========================
# ⚡ ПРОВЕРКА ЖИВЫХ
# =========================

def deep_ping(node):
    try:
        parsed = urllib.parse.urlparse(node)
        netloc = parsed.netloc

        if "@" in netloc:
            netloc = netloc.split("@")[1]

        host = netloc.split(":")[0]
        port = int(netloc.split(":")[1].split("?")[0])

        ip = socket.gethostbyname(host)

        with socket.create_connection((ip, port), timeout=TIMEOUT):
            return node
    except:
        return None

# =========================
# 🌍 ОПРЕДЕЛЕНИЕ СТРАНЫ
# =========================

def get_tag(node):
    up = node.upper()

    if "RU" in up:
        return "🇷🇺 Russia"
    elif "DE" in up:
        return "🇩🇪 Germany"
    elif "NL" in up:
        return "🇳🇱 Netherlands"
    elif "US" in up:
        return "🇺🇸 USA"
    elif "TR" in up:
        return "🇹🇷 Turkey"
    else:
        return "🌐 Global"

# =========================
# 🚀 MAIN
# =========================

def main():
    print("📡 Loading sources...")

    raw = fetch_sources()
    nodes = extract_nodes(raw)

    print(f"🔎 Found: {len(nodes)} nodes")

    print("⚡ Checking live servers...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
        checked = list(ex.map(deep_ping, nodes))

    alive = [x for x in checked if x]

    print(f"✅ Alive: {len(alive)}")

    # =========================
    # 🧹 CLEAN + FORMAT
    # =========================

    final = []

    for i, node in enumerate(alive[:MAX_SERVERS]):
        base = node.split("#")[0].strip()

        tag = get_tag(base)

        final.append(f"{base}#VPN | {tag} | #{i+1}")

    # =========================
    # 💾 SAVE NORMAL
    # =========================

    text = "\n".join(final)

    import os
    os.makedirs("output", exist_ok=True)

    with open("output/configs.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # =========================
    # 🔐 PREMIUM SUB (BASE64)
    # =========================

    encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")

    with open("output/sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print("📦 DONE")
    print(f"📄 configs: {len(final)} servers")

if __name__ == "__main__":
    main()
