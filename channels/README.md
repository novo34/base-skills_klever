# JEV Channel Security Contract

## Trust boundary

Channel payloads are untrusted external input.

A real WEB, TELEGRAM or WHATSAPP adapter must authenticate the incoming request/session before it may construct a trusted `ChannelMessage`.

The adapter contract requires:

1. provider/session authentication;
2. external identity verification;
3. mapping of the external identity to an authorized JEV actor;
4. authenticated evidence carried into the normalized `ChannelMessage`;
5. rejection when authentication or identity verification is missing.

Provider-specific implementations belong in `jev-platform`.

Examples of acceptable mechanisms include the official verification mechanism supported by the provider, such as a webhook signature, secret token, or authenticated web session.

A channel adapter must never trust an `actor` value supplied only by the payload.

## Attachments and remote sources

Attachment sources are also untrusted.

Foundation permits:

- internal logical references using `upload://`;
- internal channel references using `channel://`;
- external HTTPS references subject to source validation.

Foundation rejects unsafe schemes and obvious local/private hosts.

The real downloader in `jev-platform` must additionally:

- resolve DNS immediately before connecting;
- reject private, loopback, link-local, reserved or otherwise disallowed resolved addresses;
- connect using an address from that validated resolution set, without silently re-resolving to a different address;
- repeat validation and connection pinning after every redirect;
- use strict redirect limits;
- enforce download size and MIME limits;
- never send internal credentials to remote attachment URLs.

Static URL validation alone is not sufficient protection against DNS rebinding or redirect-based SSRF.
