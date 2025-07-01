# HomeIP

HomeIP periodically checks your public IP address and updates a DNS record when it changes. The DNS provider is pluggable; currently a Leaseweb implementation is included.

## Usage

Set the following environment variables:

- `CHECK_INTERVAL` - seconds between checks (default `300`)
- `DNS_PROVIDER` - name of the provider (`leaseweb` is the default and only option)
- `DNS_DOMAIN` - domain name to update
- `DNS_RECORD` - record name (e.g. `www` or `@`) – defaults to `@`
- `LEASEWEB_API_TOKEN` - API token for Leaseweb DNS

Install dependencies and run `python -m homeip.main`.
