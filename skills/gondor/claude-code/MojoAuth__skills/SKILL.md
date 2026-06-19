---
name: oidc-hosted-page-ios
description: Implement passwordless authentication in native iOS/Swift applications using MojoAuth OIDC with AppAuth.
---

# Implement MojoAuth OIDC (iOS / Swift)

This expert AI assistant guide walks you through integrating passwordless authentication into an existing iOS application using MojoAuth's Hosted Login Page as an OIDC identity provider via AppAuth for iOS. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing iOS 15+ application (Swift 5.7+) with a login screen.
- Xcode 14+ installed.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required library: `openid/AppAuth-iOS`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the callback URI using a custom scheme (e.g., `com.example.myapp://auth/callback`).
4. Retrieve **Client ID**.
5. Enable your preferred authentication methods.

> **Note:** For native/mobile apps, use **Authorization Code with PKCE** (no Client Secret on the device).

### Step 2: Modify the Existing iOS Project

#### Substep 2.1: Add Dependencies

Add AppAuth via **Swift Package Manager**:
1. In Xcode, go to **File > Add Package Dependencies**.
2. Enter: `https://github.com/openid/AppAuth-iOS.git`.
3. Select the latest stable version and add to your target.

Or via **CocoaPods**:

```ruby
# Podfile
pod 'AppAuth'
```

```bash
pod install
```

#### Substep 2.2: Configure URL Scheme

Add a custom URL scheme in your `Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>com.example.myapp</string>
        </array>
        <key>CFBundleURLName</key>
        <string>com.example.myapp</string>
    </dict>
</array>
```

#### Substep 2.3: Configure OIDC

Create an auth configuration helper (e.g., `AuthConfig.swift`):

```swift
// AuthConfig.swift
import Foundation

struct AuthConfig {
    static let issuerURL = URL(string: "https://your-app.mojoauth.com")!
    static let clientID = "your_client_id"
    static let redirectURI = URL(string: "com.example.myapp://auth/callback")!
    static let scopes = ["openid", "profile", "email"]
}
```

#### Substep 2.4: Create Auth Manager

Create a centralised auth manager (e.g., `AuthManager.swift`):

```swift
// AuthManager.swift
import UIKit
import AppAuth

class AuthManager: NSObject {
    static let shared = AuthManager()
    var currentAuthorizationFlow: OIDExternalUserAgentSession?
    var authState: OIDAuthState?

    func login(from viewController: UIViewController, completion: @escaping (Result<OIDAuthState, Error>) -> Void) {
        // Discover OIDC configuration
        OIDAuthorizationService.discoverConfiguration(forIssuer: AuthConfig.issuerURL) { config, error in
            guard let config = config else {
                completion(.failure(error ?? NSError(domain: "OIDC", code: -1, userInfo: [NSLocalizedDescriptionKey: "Discovery failed"])))
                return
            }

            // Build authorization request
            let request = OIDAuthorizationRequest(
                configuration: config,
                clientId: AuthConfig.clientID,
                scopes: AuthConfig.scopes,
                redirectURL: AuthConfig.redirectURI,
                responseType: OIDResponseTypeCode,
                additionalParameters: nil
            )

            // Launch auth flow — opens MojoAuth Hosted Login Page
            self.currentAuthorizationFlow = OIDAuthState.authState(
                byPresenting: request,
                presenting: viewController
            ) { authState, error in
                if let authState = authState {
                    self.authState = authState
                    print("Authenticated! Access Token: \(authState.lastTokenResponse?.accessToken ?? "nil")")
                    completion(.success(authState))
                } else {
                    print("OIDC Error: \(error?.localizedDescription ?? "Unknown error")")
                    completion(.failure(error ?? NSError(domain: "OIDC", code: -1)))
                }
            }
        }
    }

    func logout() {
        authState = nil
    }
}
```

#### Substep 2.5: Handle Redirect in AppDelegate / SceneDelegate

```swift
// AppDelegate.swift (or SceneDelegate.swift)
import AppAuth

// In AppDelegate:
func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey: Any] = [:]) -> Bool {
    if let flow = AuthManager.shared.currentAuthorizationFlow,
       flow.resumeExternalUserAgentFlow(with: url) {
        AuthManager.shared.currentAuthorizationFlow = nil
        return true
    }
    return false
}

// If using SceneDelegate:
func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
    guard let url = URLContexts.first?.url else { return }
    if let flow = AuthManager.shared.currentAuthorizationFlow,
       flow.resumeExternalUserAgentFlow(with: url) {
        AuthManager.shared.currentAuthorizationFlow = nil
    }
}
```

#### Substep 2.6: Update Login View Controller

Since MojoAuth handles all authentication on its Hosted Login Page, your login screen only needs a **"Sign In" button**:

```swift
// LoginViewController.swift
import UIKit

class LoginViewController: UIViewController {
    private let signInButton = UIButton(type: .system)

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    private func setupUI() {
        view.backgroundColor = .systemBackground
        title = "Welcome"

        let titleLabel = UILabel()
        titleLabel.text = "Welcome"
        titleLabel.font = .systemFont(ofSize: 28, weight: .bold)
        titleLabel.textAlignment = .center

        let subtitleLabel = UILabel()
        subtitleLabel.text = "Sign in with your preferred method"
        subtitleLabel.font = .systemFont(ofSize: 14)
        subtitleLabel.textColor = .secondaryLabel
        subtitleLabel.textAlignment = .center

        signInButton.setTitle("Sign In with MojoAuth", for: .normal)
        signInButton.addTarget(self, action: #selector(handleSignIn), for: .touchUpInside)
        signInButton.titleLabel?.font = .systemFont(ofSize: 17, weight: .semibold)

        let poweredByLabel = UILabel()
        poweredByLabel.text = "Powered by MojoAuth"
        poweredByLabel.font = .systemFont(ofSize: 12)
        poweredByLabel.textColor = .tertiaryLabel
        poweredByLabel.textAlignment = .center

        let stack = UIStackView(arrangedSubviews: [titleLabel, subtitleLabel, signInButton, poweredByLabel])
        stack.axis = .vertical
        stack.spacing = 16
        stack.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(stack)

        NSLayoutConstraint.activate([
            stack.centerYAnchor.constraint(equalTo: view.centerYAnchor),
            stack.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -24),
        ])
    }

    @objc private func handleSignIn() {
        AuthManager.shared.login(from: self) { result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    let dashboard = DashboardViewController()
                    self.navigationController?.pushViewController(dashboard, animated: true)
                case .failure(let error):
                    let alert = UIAlertController(title: "Error", message: error.localizedDescription, preferredStyle: .alert)
                    alert.addAction(UIAlertAction(title: "OK", style: .default))
                    self.present(alert, animated: true)
                }
            }
        }
    }
}
```

### Step 3: Test the Implementation

1. Run on a simulator or device.
2. Tap **"Sign In with MojoAuth"**.
3. A browser/ASWebAuthenticationSession opens to the MojoAuth Hosted Login Page.
4. Authenticate using any available method.
5. Verify you are redirected back to the app and into the Dashboard.

## 3. Additional Considerations

- **Security**: PKCE is handled automatically by AppAuth. Never embed Client Secrets in mobile apps.
- **Token Storage**: Use the iOS Keychain to store tokens securely.
- **SwiftUI**: For SwiftUI apps, wrap the `OIDAuthState.authState(byPresenting:)` call in a coordinator or use `ASWebAuthenticationSession` directly.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Library Documentation**: Refer to the [AppAuth for iOS documentation](https://github.com/openid/AppAuth-iOS).
