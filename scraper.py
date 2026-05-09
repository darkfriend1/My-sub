import requests
import re
import base64
import socket
import urllib.parse
import concurrent.futures
import os

# =========================================
# ⚙️ SETTINGS
# =========================================

MAX_SERVERS = 50
TIMEOUT = 3.0
THREADS = 30

# =========================================
# 🔗 SOURCES
# =========================================

SOURCES = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/whoahaow/rjsxrd/refs/heads/main/githubmirror/bypass-unsecure/bypass-unsecure-all.txt",
    "https://raw.githubusercontent.com/Temnuk/naabuzil/refs/heads/main/whitelist_full",
    "https://cvedcsub.vercel.app/configs/configs.txt",
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt"
]

# =========================================
# 📂 CREATE FOLDERS
# =========================================

os.makedirs("output", exist_ok=True)

# =========================================
# 📥 DOWNLOAD SOURCES
# =========================================

def fetch_sources():
    raw = ""

    for url in SOURCES:
        try:
            print(f"📡 Loading: {url}")

            r = requests.get(url, timeout=15)

            if r.status_code == 200:
                raw += r.text + "\n"
                print("✅ OK")

            else:
                print(f"❌ Status: {r.status_code}")

        except Exception as e:
            print(f"❌ ERROR: {e}")

    return raw

# =========================================
# 🔍 EXTRACT LINKS
# =========================================

def extract_nodes(raw):
    pattern = r'(?:vless|vmess|trojan|ss)://[^\s]+'

    found = re.findall(pattern, raw)

    # remove duplicates
    found = list(set(found))

    cleaned = []

    for node in found:
        if len(node) > 20:
            cleaned.append(node.strip())

    return cleaned

# =========================================
# ⚡ CHECK LIVE SERVERS
# =========================================

def deep_ping(node):
    try:
        parsed = urllib.parse.urlparse(node)

        netloc = parsed.netloc

        if "@" in netloc:
            netloc = netloc.split("@")[1]

        host = netloc.split(":")[0]

        port_raw = netloc.split(":")[1].split("?")[0]
        port = int(re.sub(r"\D", "", port_raw))

        # DNS check
        ip = socket.gethostbyname(host)

        # TCP connect
        sock = socket.create_connection(
            (ip, port),
            timeout=TIMEOUT
        )

        sock.settimeout(TIMEOUT)

        try:
            sock.send(b"\n")
        except:
            sock.close()
            return None

        sock.close()

        return node

    except:
        return None

# =========================================
# 🌍 COUNTRY / FLAGS
# =========================================

def get_tag(node):
    up = node.upper()

    if "RU" in up or "RUSSIA" in up:
        return "🇷🇺 Russia"

    elif "DE" in up or "GERMANY" in up:
        return "🇩🇪 Germany"

    elif "NL" in up or "NETHERLANDS" in up:
        return "🇳🇱 Netherlands"

    elif "US" in up or "USA" in up:
        return "🇺🇸 USA"

    elif "TR" in up or "TURKEY" in up:
        return "🇹🇷 Turkey"

    elif "FR" in up:
        return "🇫🇷 France"

    elif "GB" in up or "UK" in up:
        return "🇬🇧 United Kingdom"

    else:
        return "🌐 Global"

# =========================================
# 🔐 BUILD ENCRYPTED SUB
# =========================================

def build_subscription(configs):
    content = "\n".join(configs)

    # raw configs
    with open(
        "output/configs.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)

    # encrypted/base64 subscription
    encoded = base64.b64encode(
        content.encode("utf-8")
    )

    with open(
        "output/sub.txt",
        "wb"
    ) as f:

        f.write(encoded)

# =========================================
# 🔗 GENERATE DEEP LINK
# =========================================

def build_deeplink():
    github_sub = (
        "https://raw.githubusercontent.com/"
        "USER/REPO/main/output/sub.txt"
    )

    encoded_url = urllib.parse.quote(
        github_sub,
        safe=""
    )

    deeplink = (
        f"happ://install-sub?url={encoded_url}"
    )

    with open(
        "output/deeplink.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(deeplink)

# =========================================
# 🚀 MAIN
# =========================================

def main():

    print("================================")
    print("🚀 VPN PARSER STARTED")
    print("================================")

    # =====================================
    # DOWNLOAD
    # =====================================

    raw_data = fetch_sources()

    # =====================================
    # EXTRACT
    # =====================================

    all_nodes = extract_nodes(raw_data)

    print(f"\n🔎 Total found: {len(all_nodes)}")

    if not all_nodes:
        print("❌ No nodes found")
        return

    # =====================================
    # CHECK SERVERS
    # =====================================

    print("\n⚡ Checking live servers...")

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=THREADS
    ) as executor:

        checked_nodes = list(
            executor.map(deep_ping, all_nodes)
        )

    alive_nodes = [
        n for n in checked_nodes
        if n is not None
    ]

    print(f"✅ Alive servers: {len(alive_nodes)}")

    # =====================================
    # FORMAT
    # =====================================

    final_configs = []

    for i, node in enumerate(
        alive_nodes[:MAX_SERVERS]
    ):

        base = node.split('#')[0].strip()

        tag = get_tag(base)

        final_configs.append(
            f"{base}#Happ | {tag} | {i+1}"
        )

    # =====================================
    # SAVE FILES
    # =====================================

    build_subscription(final_configs)

    build_deeplink()

    # =====================================
    # INFO FILE
    # =====================================

    with open(
        "output/info.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"Alive servers: "
            f"{len(final_configs)}\n"
        )

    # =====================================
    # DONE
    # =====================================

    print("\n================================")
    print("✅ DONE")
    print(f"📄 configs.txt: {len(final_configs)}")
    print("🔐 sub.txt created")
    print("🔗 deeplink.txt created")
    print("================================")

# =========================================

if __name__ == "__main__":
    main()
