# Suggested Prompts for MojoAuth OIDC — iOS / Swift

## Full Implementation

> "Add passwordless authentication to my iOS/Swift application using MojoAuth.
>
> Follow `skills/authentication/oidc-hosted-page-ios/SKILL.md` exactly.
>
> Requirements:
> 1. Add AppAuth via Swift Package Manager.
> 2. Configure the URL scheme and Info.plist.
> 3. Create an AuthManager to handle the OIDC flow.
> 4. Create a login screen with a 'Sign In with MojoAuth' button.
> 5. Handle the redirect in AppDelegate/SceneDelegate.
>
> My MojoAuth config:
> - MojoAuth Domain: `your-app.mojoauth.com`
> - Client ID: `<my_client_id>`
> - Redirect URI: `com.example.myapp://auth/callback`"

## Add MojoAuth to Existing Login

> "My iOS app already has a login screen. Add MojoAuth as a passwordless alternative.
> Reference `skills/authentication/oidc-hosted-page-ios/SKILL.md`.
> The MojoAuth flow should use AppAuth and PKCE."
