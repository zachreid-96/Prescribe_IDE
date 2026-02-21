# Prescribe IDE (Lite)

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Pygments](https://img.shields.io/badge/Syntax-Pygments-orange)
![FAISS](https://img.shields.io/badge/AI-FAISS%20%2B%20HuggingFace-yellow)
![Status](https://img.shields.io/badge/Status-Stable%2C%20Active%20Development-brightgreen)

> **Note:** Source code is hosted on a privately hosted Gitea instance. This repository serves as a public-facing project reference. KCFG command support exists within the full project but is withheld from this public repository pending licensing clarification with Kyocera.

**Author:** Zach Reid | [zforgehub.dev](https://zforgehub.dev)

---

## Overview

Prescribe IDE (Lite) is a purpose-built editor, linter, and AI assistant for Kyocera's Prescribe printer command language (PDL). It sits somewhere between a smart text editor and a lightweight IDE — purpose-built for a domain where no modern tooling has existed until now.

To the best of the author's knowledge, **no manufacturer or third-party tool exists that validates, lints, or generates Prescribe commands interactively.** This project fills that gap entirely.

---

## The Problem It Solves

Kyocera's Prescribe language is powerful but notoriously difficult to work with:

- Commands must be syntactically exact — a single mistake means wasted paper, silent failures, or devices ignoring input entirely
- The official documentation is public-facing but does a poor job of teaching syntax, grammar, or valid parameter values
- No manufacturer or dealer tool exists to help generate, validate, or test Prescribe commands
- Copier technicians and admins who need Prescribe occasionally are not programmers — the barrier to entry is high

This tool eliminates that barrier entirely. Technicians can write, validate, and send Prescribe command files without needing to understand the underlying language — and developers get a well-architected example of building a linter and mini-IDE for a domain-specific language (DSL).

---

## Features

### Editor
- Full syntax highlighting via a **custom Pygments lexer and style** built specifically for Prescribe
- **CustomTkinter + Chlorophyll CodeView** for a modern, clean editing experience
- Formatter that normalizes commands to one-per-line for readability and easier validation

### Suggestion Pane
- Dynamic reference panel that updates as you type
- Shows valid parameters, accepted values, and descriptions for the current command
- Driven entirely by JSON command definitions — no hardcoded logic

### Error Pane
- Lint-style warnings and syntax errors surfaced in real time
- Reports **line numbers and character positions** for precise troubleshooting
- Flags edge cases like multiple commands on a single line
- Grammar validation powered by **pyparsing**

### AI Assistant
- **Fully local, privacy-first** — powered by a Hugging Face model downloaded and run entirely on-device
- No external API calls, no data reporting, no network dependency
- Accepts natural language input and outputs valid, correctly formatted Prescribe commands
- Supports **multiple commands in a single prompt**, separated by semicolons

**Example prompts:**
```
increase RAM from 64MB to 128MB
Set duplex to long-edge binding
increase RAM from 64MB to 128MB; Set duplex to long-edge binding
```
Each prompt returns ready-to-use Prescribe syntax that can be pasted directly into the editor.

### Printer Integration *(in progress)*
- Open, edit, save, and send command files directly to devices via **LPR**
- Backend LPR commands implemented; full UI integration in progress

---

## Technical Highlights

| Component | Technology |
|---|---|
| Language | Python 3.x |
| GUI | CustomTkinter + Chlorophyll CodeView |
| Syntax Highlighting | Custom Pygments Lexer + Style |
| Command Definitions | JSON (FRPO commands, standalone commands) |
| Grammar Validation | pyparsing |
| AI Assistant | FAISS + HuggingFace (fully local) |
| Command Loader | Singleton pattern — JSON loaded once, routed cleanly |
| Printer Integration | LPR (in progress) |

### Architecture Notes

- **JSON-driven command definitions** mean new commands or parameter changes require no code modification — just a JSON update
- **Singleton Command Loader** ensures all command data is loaded into memory once and shared cleanly across all components
- **Per-line parsing logic** with multi-command awareness handles real-world Prescribe files accurately
- The AI assistant uses **FAISS vector search** over command metadata combined with grammar restrictions to ensure generated output is always syntactically valid — not just plausible

---

## KCFG Support

This project includes support for KCFG commands (dealer-level Kyocera configuration). This functionality is present in the full project but **withheld from this public repository** pending licensing clarification with Kyocera. The architecture fully supports it and it is functional in the private build.

---

## Who It's For

**Copier technicians & admins** — build and send Prescribe files without memorizing syntax or reading dense documentation.

**Developers** — a practical example of designing a linter, suggestion engine, and AI assistant for a niche domain-specific language using Python.

---

## Stretch Goals

- Inline autocomplete as an optional editor feature
- Expand support to full Prescribe PDL (drawing and text commands, not just settings/configuration)
- Printer management pane — device history, quick-send, connection management
- Dry-run mode — preview what will be transmitted before sending
- Exportable, searchable command reference manual

---

## Status

Core features are stable and working:
- Syntax highlighting
- Suggestion pane
- Error pane
- JSON-driven validation
- Format detection and formatting
- AI assistant (local FAISS + HuggingFace)
- Printer integration / LPR sending (in progress)

---

## Links

- 🌐 [zforgehub.dev](https://zforgehub.dev) — Portfolio & DevHub


![Demo of Address Book Converter](/media/prescribe_ide.gif)
