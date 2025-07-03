from abc import ABC, abstractmethod


class DNSProvider(ABC):
    """Abstract base class for DNS providers."""

    @abstractmethod
    def update_A_record(self, domain: str, fqdn: str, ip_address: str, ttl: int = 60) -> None:
        """Update an A record with the given IP address."""
        raise NotImplementedError

    @abstractmethod
    def list_records(self, domain: str):
        """Return DNS records for the given domain."""
        raise NotImplementedError
