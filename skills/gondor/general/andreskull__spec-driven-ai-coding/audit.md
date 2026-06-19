# Audit Command

System health verification and instruction drift detection. This command analyzes the codebase, specifications, and implementation to ensure everything is aligned and healthy.

## Purpose

- Verify system health and consistency
- Detect instruction drift between spec, design, and code
- Identify missing or incomplete implementations
- Check for violations of coding standards

## Analysis Areas

### 1. Specification Alignment
- Check if code matches `spec.md` requirements
- Verify design follows `design.md` decisions
- Identify features implemented but not in spec
- Identify spec requirements not implemented

### 2. Task Completion
- Verify all tasks in `tasks.md` are addressed
- Check for incomplete or abandoned tasks
- Identify tasks marked complete but not implemented
- Verify Definition of Done criteria met

### 3. Code Quality
- Check adherence to coding standards
- Verify test coverage
- Identify code smells or anti-patterns
- Check for security issues

### 4. Documentation
- Verify code is documented
- Check README is up to date
- Verify API documentation exists
- Check for missing or outdated docs

## Output Format

Generate an audit report with:

1. **Health Score** (0-100)
   - Overall system health rating
   - Breakdown by category

2. **Violations Report**
   - List of violations found
   - Severity (Critical, High, Medium, Low)
   - Location and description
   - Recommended fixes

3. **Drift Detection**
   - Spec vs Implementation drift
   - Design vs Implementation drift
   - Code vs Standards drift

4. **Recommendations**
   - Action items to improve health
   - Priority order
   - Estimated effort

## Usage

Run this command:
- Before major releases
- After completing a feature
- When onboarding new team members
- Periodically for maintenance

## Integration

- Cross-references `spec.md`, `design.md`, `tasks.md`
- Checks against framework-specific standards
- Uses `executor-gate.md` for code quality checks
- Integrates with `task-manager.md` for completion verification
