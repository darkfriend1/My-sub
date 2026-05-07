import requests
import json
import base64
import time
from datetime import datetime, timedelta

# --- ГИБКИЕ НАСТРОЙКИ ---
LIMIT_NODES = 30
TOTAL_GB = 50
EXPIRE_DAYS = 30
TG_CHANNEL = "https://t.me/+dGgfc2EX3uoxN2Fi" # Своя ТГ-ссылка
INF_PAGE = "https://your_info_site.com"  # Страница информации
# ------------------------

def generate_billing_config():
    """Эмуляция биллинга и ссылок для инфо-панели (Пункт 3)"""
    total_bytes = TOTAL_GB * 1024 * 1024 * 1024
    used_bytes = int(total_bytes * 0.05) # Имитация 5% расхода
    expire_date = (datetime.now() + timedelta(days=EXPIRE_DAYS)).strftime("%d.%m.%Y")
    
    # Создаем технический конфиг, который Happ интерпретирует как панель биллинга
    # Для этого в备注 (remarks) пишем специальный формат, поддерживаемый клиентом
    billing_remarks = f"📊 [{TOTAL_GB}GB/{EXPIRE_DAYS} Days] | Expires: {expire_date} | TG: {TG_CHANNEL}"
    
    # Пример для Sing-box/Hiddify формата, который может отображаться как панель
    info_config = {
        "tag": "BILLING_INFO",
        "type": "selector",
        "outbounds": ["direct"],
        "remarks": billing_remarks, # Вот здесь магия имен и флагов
        "custom_data": { # Специфично для некоторых JSON-клиентов
            "total_gb": TOTAL_GB,
            "used_gb": TOTAL_GB * 0.05,
            "expire_at": expire_date,
            "tg": TG_CHANNEL
        }
    }
    return json.dumps(info_config)

def update_sub():
    valid_configs = []
    # 1. Добавляем конфиг с информацией (Пункт 3)
    valid_configs.append(generate_billing_config())
    
    # 2. Получаем сырые ссылки (здесь твой JSON не нужен, т.к. мы парсим ссылки)
    # sources = [...] (как в прошлом скрипте)
    # nodes = parse_and_clean_nodes(sources)
    
    # --- Эмуляция рабочих нод ---
    mock_nodes = [
        {"ip": "1.1.1.1", "port": 443, "type": "vless"},
        {"ip": "2.2.2.2", "port": 80, "type": "vmess"},
        # ...
    ]
    # ----------------------------

    for node in mock_nodes:
        # 3. Добавление флагов и имен (Пункт 1)
        # Мы используем API геоип (локальное) или просто привязываемся к IP.
        # Например, 1.1.1.1 -> Flag: 🇺🇸, Name: US-Main
        country_code = "DE" # Упрощенно, нужно geoip
        flag = "🇩🇪" if country_code == "DE" else "🇺🇸"
        server_name = f"VPN | Германия | Авто" if country_code == "DE" else "VPN | США | μTorrent"
        
        # Реконструируем ссылку с кастомным Remark
        # remarks = "🇩🇪 VPN | Германия | Авто"
        link = f"vless://uuid@{node['ip']}:{node['port']}?encryption=none&security=reality&type=tcp#{flag} {server_name}"
        valid_configs.append(link)

    # 4. Принудительное шифрование (Base64) (Пункт 2)
    # Отдаем файл в Base64. Клиент обязан декодировать его.
    content = "\n".join(valid_configs)
    final_sub = base64.b64encode(content.encode()).decode()
    
    with open("sub.txt", "w") as f:
        f.write(final_sub)
    print("[+] Подписка обновлена. JSON для флагов применен. Base64 зашифровано.")

if __name__ == "__main__":
    update_sub()
