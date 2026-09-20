# Security Policy

SociaSphere is a Django social application containing authenticated profiles, posts, relationships, and user-generated media.

## Reporting a Vulnerability

Please report security vulnerabilities privately to the repository owner through GitHub or the contact information published on https://allkvd.dev/. Do not publish exploitable details in a public issue.

Include the affected component, reproduction steps, impact, and relevant evidence.

## Security Practices

- State-changing social operations use POST requests with CSRF protection.
- Authentication and ownership checks protect user-scoped operations.
- Profile URLs are validated before being rendered.
- Uploaded profile images are size/dimension limited and verified as images.
- Production secrets are supplied through environment configuration rather than committed files.
- Application errors are handled without intentionally exposing internal stack traces or filesystem paths.
- Local development currently uses SQLite; no PostgreSQL migration is required for the current deployment scope.

## Secret Handling

Never commit `.env` files, credentials, session secrets, database passwords, or API keys.
