import os
import time
import requests

from homeip.dns_providers import LeasewebDNSProvider


CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
DNS_PROVIDER = os.getenv("DNS_PROVIDER", "leaseweb").lower()
DOMAIN = os.getenv("DNS_DOMAIN")
RECORD_NAME = os.getenv("DNS_RECORD", "@").strip()


def get_public_ip() -> str:
    response = requests.get("https://api.ipify.org")
    response.raise_for_status()
    return response.text.strip()


def main():
    if not DOMAIN:
        raise ValueError("DNS_DOMAIN environment variable is required")

    if DNS_PROVIDER != "leaseweb":
        raise ValueError(f"Unsupported DNS provider: {DNS_PROVIDER}")

    provider = LeasewebDNSProvider()

    last_ip = None
    while True:
        try:
            current_ip = get_public_ip()
            if current_ip != last_ip:
                provider.update_record(DOMAIN, RECORD_NAME, current_ip)
                last_ip = current_ip
        except Exception as exc:
            print(f"Error updating DNS: {exc}")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
