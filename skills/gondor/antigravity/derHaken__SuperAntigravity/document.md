---
name: document
description: name: document
---
# Document

Generate focused documentation for components, functions, APIs, and features.

## Documentation Types

### Inline (docstrings/JSDoc)
For: functions, classes, complex logic
Format: language-appropriate (JSDoc for JS/TS, docstrings for Python)
Include: what it does, parameters, return value, example

### API Reference
For: external-facing APIs
Include: endpoints, request/response format, auth, error codes, examples

### User Guide
For: features users interact with
Include: what it does, how to use it, common patterns, gotchas

### Architecture Docs
For: system components and their relationships
Include: purpose, dependencies, data flow, deployment

## Rules
- Document the WHY, not the WHAT (code shows what, comments explain why)
- Don't document obvious things
- Keep docs close to the code they describe
- Update docs when code changes — stale docs are worse than no docs

## Usage
`/document [target] [--type inline|api|guide|architecture]`
