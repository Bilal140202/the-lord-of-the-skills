# Project Constitution (gemini.md)

## North Star
Generate automated AI newsletter from NotebookLM research.

## Integrations
- NotebookLM
- Supabase
- Email (Zapier)

## Behavioral Rules
- Output must always follow JSON schema
- No personal data
- Professional tone only

---

## Data Schema (MANDATORY)

### Input
{
  "query": "string",
  "category": "string"
}

### Output
{
  "newsletter_list": [
    {
      "title": "string",
      "summary": "string",
      "url": "string"
    }
  ]
}
