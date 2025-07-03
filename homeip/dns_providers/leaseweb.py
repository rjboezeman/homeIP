import os
import requests
from ..dns_provider import DNSProvider


class LeasewebDNSProvider(DNSProvider):
    """DNS Provider implementation for Leaseweb."""

    BASE_URL = "https://api.leaseweb.com/hosting/v2"

    def __init__(self) -> None:
        self.token = os.getenv("LEASEWEB_API_TOKEN")
        if not self.token:
            raise ValueError("LEASEWEB_API_TOKEN is required")

    def _headers(self):
        return {
            "X-LSW-Auth": self.token,
            "Content-Type": "application/json",
        }

    def update_A_record(self, domain: str, fqdn: str, ip_address: str, record_type: str = "A", ttl: int = 60) -> None:
        """Update an A/AAAA record for a given fully qualified domain name (FQDN)."""
        fqdn = fqdn.rstrip(".") + "."  # Ensure trailing dot per Leaseweb API requirement
        url = f"{self.BASE_URL}/domains/{domain}/resourceRecordSets/{fqdn}/{record_type}"

        payload = {
            "content": [ip_address],
            "ttl": ttl
        }

        response = requests.put(url, json=payload, headers=self._headers())
        response.raise_for_status()

    def list_records(self, domain: str):
        url = f"{self.BASE_URL}/domains/{domain}/resourceRecordSets"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
