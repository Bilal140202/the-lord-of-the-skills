---
name: browser-tests
description: Browser tool usage guide for testing and verification. Use when you need to test web pages, capture screenshots, verify deployments, or check responsive design.
version: 1.0
author: Antigravity
---

# Browser Testing & Verification

> [!IMPORTANT]
> This skill MUST be executed strictly under the **Omni-Architect Agent Protocol v1.0**.
> All tool executions, code modifications, and communications MUST adhere to the 13 core protocols.

Guide for using the browser tool effectively during testing and verification.

## When to Use

- Verifying deployed sites
- Testing responsive design at different breakpoints
- Capturing screenshots for walkthroughs
- Validating user flows end-to-end
- Visual regression testing
- Checking cross-browser rendering

## Responsive Breakpoints

| Device    | Width  | Usage            |
| --------- | ------ | ---------------- |
| Mobile    | 375px  | iPhone SE/Mini   |
| Mobile L  | 428px  | iPhone Pro Max   |
| Tablet    | 768px  | iPad             |
| Desktop   | 1024px | Laptop           |
| Desktop L | 1440px | External monitor |

## Workflow

### 1. Open Page

Navigate to the target URL using `browser_subagent`.

### 2. Visual Inspection

- Check layout integrity
- Verify dark mode rendering
- Confirm typography and spacing
- Validate color contrast

### 3. Interactive Testing

- Click buttons and links
- Fill and submit forms
- Test navigation flows
- Verify error states

### 4. Responsive Testing

Resize the browser to each breakpoint and verify:

- No horizontal overflow
- Text remains readable
- Touch targets are adequate (≥44px)
- Images scale correctly

### 5. Capture Evidence

Take screenshots at key states for documentation in walkthroughs.

## Best Practices

- Always test on mobile (375px) first
- Check both dark and light modes
- Verify keyboard navigation works
- Test with and without JavaScript
- Validate forms with invalid data
- Check loading states and empty states
