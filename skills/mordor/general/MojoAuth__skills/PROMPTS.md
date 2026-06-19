# Suggested Prompts for MojoAuth OIDC — PHP

## Full Implementation

> "Add passwordless authentication to my PHP application using MojoAuth.
>
> Follow `skills/authentication/oidc-hosted-page-php/SKILL.md` exactly.
>
> Requirements:
> 1. Install `jumbojett/openid-connect-php`.
> 2. Configure the OIDC client with my MojoAuth Domain and credentials.
> 3. Create a login page with a 'Sign In with MojoAuth' link.
> 4. Handle the OIDC callback and create a session.
>
> My MojoAuth config:
> - MojoAuth Domain: `your-app.mojoauth.com`
> - Client ID: `<my_client_id>`
> - Redirect URI: `http://localhost:8000/callback.php`"

## Add MojoAuth to Existing Login

> "My PHP app already has session-based login. Add MojoAuth as a passwordless alternative.
> Reference `skills/authentication/oidc-hosted-page-php/SKILL.md`.
> Both paths should result in the same $_SESSION['user'] data."
