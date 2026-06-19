---
name: browser-5mb-limit
description: |
version: 1.0
author: Antigravity
---

# Handling Browser 5MB Limit Error (image exceeds 5 MB maximum)

> [!IMPORTANT]
> This skill MUST be executed strictly under the **Omni-Architect Agent Protocol v1.0**.
> All tool executions, code modifications, and communications MUST adhere to the 13 core protocols.

## 📌 Context of the Problem

The underlying AI engine (Vertex AI) has a **hard limit of 5 Megabytes per image payload**.

Actions that trigger this crash immediately:

1. Instructing the `browser_subagent` to perform a long scroll taking screenshots of the entire page ("Take a full page screenshot by scrolling down").
2. Requesting the subagent to capture web components with extremely high-definition load, gradients, and simultaneous overlays.
3. Accumulating more than 2 screenshots from a modern display in a single interaction (Response).

The reported error looks exactly like this:
`messages.62.content.1.tool_result.content.1.image.source.base64: image exceeds 5 MB maximum: 6255808 bytes > 5242880 bytes` and usually returns an HTTP 400 Bad Request or HTTP 401 Unauthorized.

## 🛑 Preventive Actions (BEFORE using the Browser Subagent)

When you decide to visually audit an application using the temporary browser, **ALWAYS explicitly add these constraints inside your TaskPrompt**:

1. **NO INFINITE SCROLLING (Full-Page Screenshot)**: Never ask it to review the structure by taking a screenshot of every piece.
2. **PRIORITIZE THE DOM**: For text and HTML class audits, specifically instruct the subagent to use `browser_get_dom`.
3. **MAXIMUM 1 OR 2 SCREENSHOTS**: Add as a strict guideline inside the prompt sent to your subagent sibling: _"CRITICAL: Do NOT return more than 1 or 2 screenshots total to avoid crashing the AI engine. Use DOM reading for the rest of your context."_
4. **SEPARATE MOBILE/DESKTOP VERSIONS**: Never order it to repeatedly Resize -> Screenshot -> Resize -> Screenshot. Ask for it in different iterations or mitigated parallel tasks.

## 🛠️ Reactive Actions (WHAT TO DO IF IT ALREADY HAPPENED)

If during your planning a user sends you a 400/401 error with this footprint (TraceID), it means you have broken the memory with your visual requests:

1. **Immediately Acknowledge the Cause**: Do not lie to the user, explain that the returned images weighed more than 5MB.
2. **Use Other Tools**: Momentarily stop the "full visual audit". Let the context rest.
3. **Re-Audit Exclusively Analytically (DOM)**: Launch the `browser_subagent` again but with the severe order: `"DO NOT take any screenshots at all. Try to describe what you see exclusively by reading the DOM (classes, ids, texts)."`.
4. **Trust User Feedback**: If the subagent failed due to visual memory, ask the user what they saw on their screen to patch it with code (`view_file`, `multi_replace`).

---

**Remember**: We are efficient at writing code, not consuming Google's memory trying to view 10000-pixel-high web pages in a single view.
