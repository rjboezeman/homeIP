import os
import time
import importlib
import logging
import requests
from .utils import resolve_fqdn

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))
DNS_PROVIDER = os.getenv("DNS_PROVIDER", "leaseweb").lower()
DNS_DOMAIN = os.getenv("DNS_DOMAIN")
DNS_RECORD = os.getenv("DNS_RECORD")

# --- Colored Logging Setup ---
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",   # Blue
        "INFO": "\033[92m",    # Green
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "CRITICAL": "\033[95m" # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        reset = self.RESET if color else ""
        record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)

handler = logging.StreamHandler()
formatter = ColoredFormatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

log = logging.getLogger("dns_updater")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
log.propagate = False

def get_public_ip() -> str:
    response = requests.get("https://api.ipify.org")
    response.raise_for_status()
    return response.text.strip()

def load_dns_provider(provider_name: str):
    try:
        log.info(f"Loading DNS provider: {provider_name}")
        module = importlib.import_module(f".dns_providers.{provider_name}", package=__package__)
        class_name = f"{provider_name.capitalize()}DNSProvider"
        provider = getattr(module, class_name)()
        log.info(f"Loaded DNS provider: {class_name}")
        return provider
    except (ImportError, AttributeError) as e:
        log.error(f"Error loading DNS provider: {e}")
        raise ValueError(f"Unsupported or misconfigured DNS provider: {provider_name}") from e

def get_resource_record_set(provider, domain: str):
    """Fetches the resource record set for a given domain."""
    try:
        records = provider.list_records(domain)
        if not isinstance(records, dict):
            raise ValueError("Expected a dict of DNS records")
        return records.get("resourceRecordSets", [])
    except Exception as exc:
        log.error(f"Error fetching resource record set: {exc}")
        raise

def main():
    if not DNS_DOMAIN:
        raise ValueError("DNS_DOMAIN environment variable is required")
    if not DNS_RECORD:
        raise ValueError("DNS_RECORD environment variable is required")
    if not DNS_PROVIDER:
        raise ValueError("DNS_PROVIDER environment variable is required")

    log.info("Starting DNS updater...")

    provider = load_dns_provider(DNS_PROVIDER)
    last_ip = None

    try:
        while True:
            current_ip = get_public_ip()
            log.info(f"Current public IP: {current_ip}")
            log.info(f"Fetching DNS records for domain: {DNS_DOMAIN}")

            entries = get_resource_record_set(provider, DNS_DOMAIN)

            if not entries:
                log.error("No DNS records found.")
                raise ValueError("No DNS records found for the specified domain.")

            for record in entries:
                log.debug(f"Record: {record.get('name')} | Type: {record.get('type')} | Content: {record.get('content')}")

            dns_entry = resolve_fqdn(DNS_RECORD, DNS_DOMAIN).rstrip(".").lower()
            
            for record in entries:
                record_name = record.get("name", "").rstrip(".").lower()
                if record_name == dns_entry:
                    if record.get("type") not in ["A", "AAAA"]:
                        raise ValueError(f"Unsupported DNS record type: {record.get('type')}")
                    content_list = record.get("content", [])
                    if not isinstance(content_list, list) or not content_list:
                        raise ValueError(f"Invalid content for DNS record: {record}")
                    dns_ip = content_list[0]

                    log.info(f"Found DNS record for {DNS_RECORD} of type {record.get('type')} in domain {DNS_DOMAIN}: {dns_ip}")
                    break
            else:
                log.error(f"No DNS record found for {DNS_RECORD} in domain {DNS_DOMAIN}")
                raise ValueError(f"No DNS record found for {DNS_RECORD} in domain {DNS_DOMAIN}")

            if current_ip != dns_ip:
                log.warning(f"Public IP {current_ip} does not match DNS record IP {dns_ip}, updating DNS record...")
                provider.update_A_record(DNS_DOMAIN, dns_entry, current_ip)
                log.info(f"Success! DNS record for {dns_entry} updated to {current_ip}")
            else:
                log.info("No change in public IP, skipping DNS update.")

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        log.info("Exiting DNS updater.")
    except Exception as exc:
        log.error(f"Unhandled error in DNS updater: {exc}")
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.critical(str(e))

