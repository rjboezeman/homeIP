from abc import ABC, abstractmethod


class DNSProvider(ABC):
    """Abstract base class for DNS providers."""

    @abstractmethod
    def update_record(self, domain: str, record: str, ip_address: str) -> None:
        """Update a DNS record with the given IP address."""
        raise NotImplementedError

    @abstractmethod
    def list_records(self, domain: str):
        """Return DNS records for the given domain."""
        raise NotImplementedError
