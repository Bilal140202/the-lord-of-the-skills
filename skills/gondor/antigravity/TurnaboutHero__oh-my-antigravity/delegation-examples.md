---
description: Delegation workflow examples
---

# OMA Delegation Examples

## Example 1: Simple Bug Fix

**User Request**: "Login button not working on mobile"

**Sisyphus Analysis**:
- Complexity: Low
- Domain: Frontend
- Specialist: debugger → pixel

**Delegation Flow**:

```markdown
[DELEGATE TO: debugger]
TASK: Identify why login button is unresponsive on mobile
CONTEXT: 
- Issue reported on iOS Safari
- Works fine on desktop
- Button element: <button id="login-btn">
OUTPUT: Root cause analysis
[END DELEGATION]

[RESULT FROM: debugger]
Root Cause: z-index issue - mobile menu overlay blocks button
Recommendation: Increase button z-index or fix menu stacking context
[END RESULT]

[DELEGATE TO: pixel]
TASK: Fix login button z-index issue
CONTEXT: Mobile menu overlay blocks button (z-index conflict)
REQUIREMENTS:
- Button must be clickable on all mobile devices
- Don't break existing desktop layout
OUTPUT: Updated CSS
[END DELEGATION]

[RESULT FROM: pixel]
Fixed CSS:
```css
.login-btn {
  position: relative;
  z-index: 1000; /* Above mobile menu */
}
```
Tested on iOS Safari, Android Chrome. ✓
[END RESULT]
```

**Total Time**: 2 specialists, sequential execution

---

## Example 2: Medium Feature

**User Request**: "Add payment processing with Stripe"

**Sisyphus Analysis**:
- Complexity: Medium
- Domains: Backend, Security, Testing
- Specialists: oracle → security-guard → codesmith → tester

**Delegation Flow**:

```markdown
Round 1 - Architecture:
[DELEGATE TO: oracle]
TASK: Design Stripe payment integration architecture
CONTEXT: E-commerce platform, need one-time and subscription payments
REQUIREMENTS:
- PCI compliance
- Webhook handling
- Refund support
OUTPUT: Integration architecture
[END DELEGATION]

[RESULT FROM: oracle]
Architecture:
1. Backend API (Node.js)
   - POST /api/payments/create → Stripe Payment Intent
   - POST /api/webhooks/stripe → Handle events
2. Frontend: Stripe Elements for card collection
3. Database: Store payment_intents table
4. Security: Stripe API keys in env, webhook signature verification
[END RESULT]

Round 2 - Security Review:
[DELEGATE TO: security-guard]
TASK: Review payment architecture for security issues
CONTEXT: Architecture from oracle (above)
REQUIREMENTS: PCI DSS compliance checklist
OUTPUT: Security requirements + recommendations
[END DELEGATION]

[RESULT FROM: security-guard]
Security Requirements:
✓ Never store card numbers (use Stripe tokens)
✓ API keys in environment variables
✓ Webhook signature verification (prevent replay attacks)
✓ HTTPS only
✓ Rate limiting on payment endpoints
✓ Audit logging for all transactions
Additional: Add fraud detection via Stripe Radar
[END RESULT]

Round 3 - Implementation:
[DELEGATE TO: codesmith]
TASK: Implement Stripe payment integration
CONTEXT:
- Architecture from oracle
- Security requirements from security-guard
REQUIREMENTS:
- Payment Intent creation
- Webhook handling
- Database schema
- Error handling
OUTPUT: Working backend code
[END DELEGATION]

[RESULT FROM: codesmith]
Implemented:
- `POST /api/payments/create` endpoint
- `POST /api/webhooks/stripe` with signature verification
- PaymentIntent model with status tracking
- Proper error handling (card declined, etc.)
- Audit logging
Code: [files created]
[END RESULT]

Round 4 - Testing:
[DELEGATE TO: tester]
TASK: Write comprehensive tests for payment integration
CONTEXT: Implementation from codesmith
REQUIREMENTS:
- Happy path (successful payment)
- Declined card scenarios
- Webhook event handling
- Edge cases
OUTPUT: Test suite with >80% coverage
[END DELEGATION]

[RESULT FROM: tester]
Test Suite Created:
- Unit tests (23 tests)
- Integration tests with Stripe test mode
- Webhook signature validation tests
- Error scenario coverage
Coverage: 87%
All tests passing ✓
[END RESULT]
```

**Total Time**: 4 specialists, sequential (each builds on previous)

---

## Example 3: Complex Project

**User Request**: "Build a full authentication system with social login"

**Sisyphus Analysis**:
- Complexity: High
- Domains: Architecture, Database, Security, Backend, Frontend, Testing, Docs
- Specialists: 7+ needed
- Execution: Mix of sequential and parallel

**Delegation Flow**:

```markdown
Phase 1 - Design (Sequential):

[DELEGATE TO: oracle]
TASK: Design complete authentication system architecture
CONTEXT: 
- Web app, 50k users expected
- Need: Email/Password, Google OAuth, GitHub OAuth
- JWT-based, stateless
REQUIREMENTS:
- Scalable architecture
- Session management strategy
- Token refresh flow
OUTPUT: Complete system architecture
[END DELEGATION]

[RESULT FROM: oracle]
Architecture:
- Auth Service (Node.js + Passport.js)
- User DB (PostgreSQL)
- Token Cache (Redis for blacklist)
- OAuth: Google + GitHub via Passport strategies
- JWT: Access (15min) + Refresh (7 days)
- Flow diagrams included
[END RESULT]

[DELEGATE TO: security-guard]
TASK: Define security requirements for auth system
CONTEXT: Architecture from oracle
REQUIREMENTS: OWASP authentication checklist
OUTPUT: Security requirements document
[END DELEGATION]

[RESULT FROM: security-guard]
Requirements:
✓ bcrypt (cost 12) for password hashing
✓ Rate limiting (5 failed logins = 15min lockout)
✓ CSRF protection
✓ XSS prevention (sanitize all inputs)
✓ SQL injection prevention (parameterized queries)
✓ Secure cookie flags (httpOnly, secure, sameSite)
✓ Password complexity (min 8 chars, upper, lower, number)
✓ Email verification before account activation
✓ OAuth state parameter validation
[END RESULT]

[DELEGATE TO: architect]
TASK: Design database schema for auth system
CONTEXT:
- Architecture from oracle
- Security requirements from security-guard
REQUIREMENTS: users, sessions, oauth_connections tables
OUTPUT: SQL schema with indexes
[END DELEGATION]

[RESULT FROM: architect]
Schema:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE oauth_connections (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  provider VARCHAR(50) NOT NULL,
  provider_user_id VARCHAR(255) NOT NULL,
  UNIQUE(provider, provider_user_id)
);

CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_oauth_provider ON oauth_connections(provider, provider_user_id);
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens(user_id);
```
[END RESULT]

Phase 2 - Implementation (Parallel):

[PARALLEL START]

  [DELEGATE TO: codesmith]
  TASK: Implement authentication backend
  CONTEXT: Architecture, Security reqs, Schema
  REQUIREMENTS:
  - Local auth (email/password)
  - OAuth (Google, GitHub)
  - JWT generation/validation
  - Token refresh
  - Password reset flow
  OUTPUT: Backend API
  [END DELEGATION]

  [DELEGATE TO: pixel]
  TASK: Create authentication UI components
  CONTEXT: Auth flows from architecture
  REQUIREMENTS:
  - Login form
  - Register form
  - OAuth buttons (Google, GitHub)
  - Password reset form
  - Email verification prompt
  OUTPUT: React components
  [END DELEGATION]

[PARALLEL END]

[RESULT FROM: codesmith]
Backend Implemented:
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- GET /auth/google (OAuth initiate)
- GET /auth/google/callback
- GET /auth/github
- GET /auth/github/callback
- POST /auth/forgot-password
- POST /auth/reset-password
All endpoints with proper error handling ✓
[END RESULT]

[RESULT FROM: pixel]
UI Components:
- LoginForm.tsx
- RegisterForm.tsx
- OAuthButtons.tsx
- PasswordResetForm.tsx
- EmailVerificationBanner.tsx
Responsive, accessible (WCAG 2.1 AA) ✓
[END RESULT]

Phase 3 - Quality (Sequential):

[DELEGATE TO: tester]
TASK: Write comprehensive auth system tests
CONTEXT:
- Backend implementation from codesmith
- Frontend components from pixel
REQUIREMENTS:
- Unit tests for all endpoints
- Integration tests for full flows
- E2E tests for critical paths
OUTPUT: Complete test suite
[END DELEGATION]

[RESULT FROM: tester]
Tests Created:
- Backend unit tests: 47 tests
- Frontend component tests: 23 tests
- Integration tests: 15 flows
- E2E tests (Playwright): 8 critical paths
Coverage: Backend 89%, Frontend 84%
All passing ✓
[END RESULT]

[DELEGATE TO: playwright-master]
TASK: Create E2E tests for auth flows
CONTEXT: Full system (backend + frontend)
REQUIREMENTS:
- Register → Email verify → Login
- OAuth login (Google mock)
- Password reset flow
- Token refresh
OUTPUT: Playwright test suite
[END DELEGATION]

[RESULT FROM: playwright-master]
E2E Tests:
- test('user registration flow') ✓
- test('email/password login') ✓
- test('google oauth login') ✓
- test('password reset') ✓
- test('token refresh on expiry') ✓
- test('logout clears session') ✓
All scenarios covered, tests passing ✓
[END RESULT]

Phase 4 - Documentation:

[DELEGATE TO: scribe]
TASK: Document authentication system
CONTEXT: Complete implementation
REQUIREMENTS:
- API documentation
- Setup guide
- Security best practices
- Troubleshooting guide
OUTPUT: Complete documentation
[END DELEGATION]

[RESULT FROM: scribe]
Documentation Created:
- `/docs/auth/API.md` - All endpoints documented
- `/docs/auth/SETUP.md` - Installation steps
- `/docs/auth/SECURITY.md` - Best practices
- `/docs/auth/TROUBLESHOOTING.md` - Common issues
- Code comments added throughout
[END RESULT]

Phase 5 - Final Review:

[DELEGATE TO: security-guard]
TASK: Final security audit of auth system
CONTEXT: Complete implementation
REQUIREMENTS: OWASP Top 10 checklist
OUTPUT: Security audit report
[END DELEGATION]

[RESULT FROM: security-guard]
Security Audit: PASS ✓
All OWASP requirements met
Minor recommendations:
- Add rate limiting to OAuth callbacks (nice-to-have)
- Consider adding 2FA in future iteration
No blocking issues found
[END RESULT]
```

**Summary**:
- **7 specialists** used
- **5 phases** (Design → Parallel Implementation → Quality → Docs → Audit)
- **Mix of sequential and parallel** execution
- **Complete feature** delivered with tests and docs

---

## Example 4: Data Analysis Project

**User Request**: "Analyze user churn patterns and create predictive model"

**Sisyphus Analysis**:
- Complexity: High
- Domain: Data Science
- Specialists: scientist-low → scientist → scientist-high → data-wizard

**Delegation Flow**:

```markdown
[DELEGATE TO: scientist-low]
TASK: Initial data exploration
CONTEXT: User database with signup/activity/churn dates
REQUIREMENTS:
- Load data
- Basic statistics
- Identify data quality issues
OUTPUT: EDA summary
[END DELEGATION]

[RESULT FROM: scientist-low]
Data Overview:
- 50,000 users
- 15% churn rate
- Features: 25 columns
- Issues: 3% missing values in 'last_login'
- Key insight: Churn correlates with low activity
[END RESULT]

[DELEGATE TO: scientist]
TASK: Statistical analysis of churn patterns
CONTEXT: EDA from scientist-low
REQUIREMENTS:
- Cohort analysis
- Feature importance
- Statistical tests
OUTPUT: Analysis findings with p-values
[END DELEGATION]

[RESULT FROM: scientist]
Findings:
1. Users inactive >30 days: 75% churn rate (p<0.001)
2. Feature usage correlated with retention (r=0.68)
3. Cohort analysis: Month 2 critical (35% churn)
Key predictors identified:
- days_since_last_login (importance: 0.42)
- feature_usage_count (importance: 0.31)
- support_tickets (importance: 0.18)
[END RESULT]

[DELEGATE TO: scientist-high]
TASK: Build predictive churn model
CONTEXT: Analysis from scientist
REQUIREMENTS:
- ML model (Random Forest or XGBoost)
- Cross-validation
- Feature engineering
- Model performance metrics
OUTPUT: Trained model + evaluation
[END DELEGATION]

[RESULT FROM: scientist-high]
Model: XGBoost Classifier
Performance:
- Accuracy: 87%
- Precision: 84%
- Recall: 82%
- F1: 0.83
- AUC-ROC: 0.91
Cross-validation (5-fold): 86% ± 2%
Feature importance confirmed
Model saved: models/churn_predictor.pkl
[END RESULT]

[DELEGATE TO: data-wizard]
TASK: Create dashboard for churn insights
CONTEXT: Model and analysis results
REQUIREMENTS:
- Interactive visualization
- Churn risk scores
- Cohort trends
OUTPUT: Dashboard
[END DELEGATION]

[RESULT FROM: data-wizard]
Dashboard Created:
- Churn rate over time
- Feature importance chart
- Cohort heatmap
- Risk score distribution
File: reports/churn_dashboard.html
[END RESULT]
```

**Total Time**: 4 specialists, sequential (data pipeline)

---

## Key Patterns

### Pattern 1: Sequential Dependencies
```
Design → Implementation → Testing → Documentation
(Each step needs previous output)
```

### Pattern 2: Parallel Independence
```
┌→ Backend (codesmith)
├→ Frontend (pixel)
└→ Database (architect)
(Can all work simultaneously)
```

### Pattern 3: Iterative Refinement
```
Draft (codesmith) → Review (oracle) → Refine (refactorer) → Final
```

### Pattern 4: Quality Gates
```
Implement → Test → Security Audit → Deploy
(Must pass each gate)
```

---

---

## Example 5: Frontend Design & Implementation (Stitch Pattern)

**User Request**: "Design and build a modern landing page for a coffee shop"

**Sisyphus Analysis**:
- Complexity: Medium
- Domain: Frontend (Design + Code)
- Specialists: stitch (design) → pixel (code)

**Delegation Flow**:

```markdown
[DELEGATE TO: stitch]
TASK: Design a modern coffee shop landing page
CONTEXT: 
- Name: "Morning Brew"
- Vibe: Cozy, warm, minimalist
- Sections: Hero, Menu Highlights, About Us, Footer
OUTPUT: Visual design description, color palette, layout structure
[END DELEGATION]

[RESULT FROM: stitch]
Design Concept:
- Palette: #3C2A21 (Dark Brown), #D5CEA3 (Beige), #1A120B (Black)
- Hero: Full-screen image of latte art with "Start Your Day Right" typography
- Typography: Playfair Display (Headings), Lato (Body)
- Layout:
  1. Stick navbar (transparent to solid on scroll)
  2. Hero section with CTA "Order Now"
  3. Card grid for Menu Highlights
  4. Story section with parallax background
[END RESULT]

[DELEGATE TO: pixel]
TASK: Implement coffee shop landing page based on Stitch's design
CONTEXT: Design concept from stitch (above)
REQUIREMENTS:
- Use React + Tailwind CSS
- Fully responsive (mobile-first)
- Implement parallax effect mentioned
OUTPUT: React code (App.tsx, components)
[END DELEGATION]

[RESULT FROM: pixel]
Implemented Landing Page:
- `components/Hero.tsx`: Uses provided colors
- `components/MenuGrid.tsx`: Responsive grid card system
- `App.tsx`: Parallax scroll implementation
- `tailwind.config.js`: Added custom colors
Code: [files created]
[END RESULT]
```

**Total Time**: 2 specialists, sequential (Design → Code)

---

These examples show how Sisyphus orchestrates specialists for tasks of varying complexity! 🎯

