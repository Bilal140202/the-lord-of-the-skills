# The Caveman Standard 🍖

So, you want to add a skill to `Gemini CLI Prompts and Skills`? Good. But remember: we aren't building a chat-bot library. We are building a **high-velocity engine**. 

To maintain the quality (and the 90% token savings), every submission must follow the **Caveman Protocol**.

---

## 🛑 Rule #1: No Yapping
If your skill allows Claude to say "Here is the code you requested," it will be rejected. 
- **Bad:** "I've updated the CSS for you..."
- **Good:** `File: style.css` [Code]

## 🛠️ How to Submit a Skill
1. **Fork** the repo.
2. **Create a file** in `/skills` named `[name].md`.
3. **Follow the Template:** Use the structure below.
4. **Test it:** Run it against a rate-limited account. If it wastes tokens on fluff, refine the constraints.
5. **Open a PR:** Keep the PR description short. (We like irony).

## 📄 The Skill Template
```markdown
---
name: [skill-name]
alias: /[shorthand]
description: [One sentence max]
---

# GUIDELINES FOR CONTRIBUTORS

1. The First Contributors must first contribute to my project macOS-evolution by filling in all OSes, from Tahoe which I will do to Sonoma to Sierra to Leopard to MacOS 9 to System 1 to Apple II Terminal.
2. Contributors must do 5 projects and must sumbit it to me for testing through my email 'aashmanshukla323@gmail.com' and Please do not send me a localhost link, do it in Vercel.
3. Contributors must love, star and fork this repo to create a skill.
4. I will be checking every single project.

---

# CONSTRAINTS
- Zero preamble.
- Output ONLY [specific output type].
- [Specific technical constraint 1]
- [Specific technical constraint 2]

# TRIGGER
{{input}}


