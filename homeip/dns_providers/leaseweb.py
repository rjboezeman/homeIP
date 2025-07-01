import os
import requests
from ..dns_provider import DNSProvider


class LeasewebDNSProvider(DNSProvider):
    """DNS Provider implementation for Leaseweb."""

    BASE_URL = "https://api.leaseweb.com/v1"

    def __init__(self) -> None:
        self.token = os.getenv("LEASEWEB_API_TOKEN")
        if not self.token:
            raise ValueError("LEASEWEB_API_TOKEN is required")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def update_record(self, domain: str, record: str, ip_address: str) -> None:
        url = f"{self.BASE_URL}/domains/{domain}/records/{record}"
        payload = {"content": ip_address, "type": "A", "name": record}
        response = requests.put(url, json=payload, headers=self._headers())
        response.raise_for_status()

    def list_records(self, domain: str):
        url = f"{self.BASE_URL}/domains/{domain}/records"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
