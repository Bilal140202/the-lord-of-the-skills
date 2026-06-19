# Workflow: Deployment

**Trigger:** /deploy

**Description:** Prepare and deploy the project to production with security checks and optimization.

**Steps:**

1. Run pre-deployment security audit:
   - Scan for exposed secrets or API keys
   - Check .env.example vs actual environment variables
   - Verify no private paths are committed
2. Build the production bundle:
   - Run build command (npm run build, pnpm build, etc.)
   - Resolve all build errors
3. Optimize assets:
   - Target final bundle size < 500kb (gzipped) where reasonable
   - Optimize images, fonts, and critical CSS
4. Generate deployment instructions (DEPLOY.md) tailored to platform:
   - Vercel → vercel --prod
   - Netlify → netlify deploy --prod
   - Custom server → Dockerfile + deployment steps
5. Simulate deployment success and provide:
   - Live URL placeholder
   - Post-deployment checklist (cache purge, monitoring setup)
6. Update memory.md:
   - Mark deployment phase complete
   - Log deployed version and URL
7. Update specs.md: Check off relevant deployment task
