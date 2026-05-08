import requests
import base64
import json
import socket
import urllib.parse
import concurrent.futures
from pathlib import Path

# =========================
# SETTINGS
# =========================

CONFIG = {
    "MAX_CONFIGS": 50,
    "TIMEOUT": 3,
    "MAX_WORKERS": 20,

    # Разрешенные протоколы
    "ALLOW_PROTOCOLS": [
        "vmess",
        "vless",
        "trojan",
        "ss"
    ],

    # Проверять DNS
    "CHECK_DNS": True,

    # Проверять порт
    "CHECK_PORT": True,

    # Удалять дубли
    "REMOVE_DUPLICATES": True,

    # Сохранять base64 подписку
    "EXPORT_BASE64": True,

    # Источники
    "SOURCES": [
        "https://example.com/configs.txt"
    ]
}

# =========================
# HELPERS
# =========================

def safe_request(url):
    try:
        r = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if r.status_code != 200:
            return ""

        text = r.text.strip()

        # защита от html мусора
        if "<html" in text.lower():
            return ""

        return text

    except:
        return ""

# =========================
# VMESS PARSER
# =========================

def parse_vmess(link):
    try:
        encoded = link.replace("vmess://", "").strip()

        encoded += "=" * (-len(encoded) % 4)

        decoded = base64.b64decode(encoded).decode("utf-8")

        data = json.loads(decoded)

        host = data.get("add")
        port = int(data.get("port"))

        return host, port

    except:
        return None, None

# =========================
# NORMAL PARSER
# =========================

def parse_uri(link):
    try:
        p = urllib.parse.urlparse(link)

        return p.hostname, p.port

    except:
        return None, None

# =========================
# VALIDATION
# =========================

def validate_node(link):

    try:

        proto = link.split("://")[0]

        if proto not in CONFIG["ALLOW_PROTOCOLS"]:
            return None

        # vmess
        if proto == "vmess":
            host, port = parse_vmess(link)

        else:
            host, port = parse_uri(link)

        if not host or not port:
            return None

        # DNS
        if CONFIG["CHECK_DNS"]:
            socket.gethostbyname(host)

        # PORT
        if CONFIG["CHECK_PORT"]:
            with socket.create_connection(
                (host, port),
                timeout=CONFIG["TIMEOUT"]
            ):
                pass

        return link

    except:
        return None

# =========================
# LOAD SOURCES
# =========================

def load_sources():

    raw = ""

    for url in CONFIG["SOURCES"]:

        print(f"[+] Loading: {url}")

        raw += safe_request(url)
        raw += "\n"

    return raw

# =========================
# EXTRACT LINKS
# =========================

def extract_links(raw):

    result = []

    for line in raw.splitlines():

        line = line.strip()

        if not line:
            continue

        for proto in CONFIG["ALLOW_PROTOCOLS"]:

            if line.startswith(f"{proto}://"):
                result.append(line)

    # remove duplicates
    if CONFIG["REMOVE_DUPLICATES"]:
        result = list(dict.fromkeys(result))

    return result

# =========================
# SAVE FILES
# =========================

def save_output(configs):

    output = "\n".join(configs)

    Path("configs.txt").write_text(
        output,
        encoding="utf-8"
    )

    print(f"[+] Saved configs.txt")

    if CONFIG["EXPORT_BASE64"]:

        encoded = base64.b64encode(
            output.encode()
        ).decode()

        Path("sub.txt").write_text(
            encoded,
            encoding="utf-8"
        )

        print(f"[+] Saved sub.txt")

# =========================
# MAIN
# =========================

def main():

    raw = load_sources()

    links = extract_links(raw)

    print(f"[+] Found: {len(links)}")

    valid = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CONFIG["MAX_WORKERS"]
    ) as executor:

        for result in executor.map(validate_node, links):

            if result:
                valid.append(result)

    valid = valid[:CONFIG["MAX_CONFIGS"]]

    print(f"[+] Valid: {len(valid)}")

    save_output(valid)

if __name__ == "__main__":
    main()
