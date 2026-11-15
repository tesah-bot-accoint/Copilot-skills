# Copilot-skills

Teaches GitHub Copilot to resolve ambiguous prompts against a shared glossary (a lightweight applied ontology) instead of guessing.

- `.github/copilot-instructions.md`: the standing rule Copilot reads on every request.
- `GLOSSARY.md`: canonical terms, their parent class, relationships, and resolved ambiguities. It grows as Copilot's clarifying questions get answered.

## Try it

Ask Copilot something deliberately vague, such as "close the stale tickets". It should ask one question naming the candidate meanings before acting, then offer a glossary entry for the answer.
