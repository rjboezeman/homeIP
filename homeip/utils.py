def resolve_fqdn(dns_record: str, dns_domain: str) -> str:
    """
    Resolves a DNS record into a fully qualified domain name (FQDN).

    - If `dns_record` is not a FQDN (no dots), it will be combined with `dns_domain`.
    - If `dns_record` is already a FQDN, it must end with `dns_domain`.
    - Returns the FQDN (without trailing dot).
    """

    if not dns_record or not dns_domain:
        raise ValueError("Both dns_record and dns_domain are required")

    dns_record = dns_record.strip(".").lower()
    dns_domain = dns_domain.strip(".").lower()

    if "." not in dns_record:
        # Not a FQDN, assume it's a short record name (like '@' or 'www')
        fqdn = f"{dns_record}.{dns_domain}" if dns_record != "@" else dns_domain
    else:
        # Already looks like a FQDN — verify it falls under dns_domain
        if not dns_record.endswith(dns_domain):
            raise ValueError(f"Record '{dns_record}' is not within domain '{dns_domain}'")
        fqdn = dns_record

    return fqdn
