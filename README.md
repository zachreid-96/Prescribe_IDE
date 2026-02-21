# Prescribe Editor & Linter (Lite IDE)
### Why this exists

Kyocera’s Prescribe command language is powerful but difficult to work with.
* Manufacturer tools are limited, dated, and unfriendly.
* Commands must be exact — mistakes lead to wasted paper or devices ignoring input.
* Many copier technicians and admins need to use Prescribe occasionally, but aren’t programmers.

This project aims to bridge the gap: a simple, modern editor that validates Prescribe commands, explains them as you type, and makes it easier to create, edit, and send command files.

### Features
* Syntax Highlighting - custom lexer and style built for Prescribe.
* Suggestion Pane - dynamic reference that shows valid parameters, values, and descriptions as you type.
* Error Pane - highlights syntax mistakes, warnings, or quirks (e.g., multiple commands on one line).
* Formatter - normalizes commands to one-per-line for readability and easier validation.
* Printer Integration (WIP) - open, edit, save, and send command files directly to devices.

### Technical Highlights
* Written in Python 3.x
* CustomTkinter + Chlorophyll CodeView for the GUI editor experience.
* Custom Lexer + Style (via Pygments) for domain-specific syntax highlighting.
* JSON-based Command Definitions
  * FRPO commands with parameters and allowed values
  * Other parent commands (like KCFG)
  * Standalone commands for flexibility
* Singleton Command Loader ensures all JSON data is in memory and routed cleanly.
* Parsing/Validation Layer
  * Grammar checked with pyparsing
  * Per-line parsing logic with multi-command awareness
  * Error handling and lint-style warnings

### Who it’s for
* Copier technicians & admins — quickly build Prescribe files without memorizing syntax.
* Programmers — example of designing a linter + mini IDE for a domain-specific language (DSL).

### Stretch Goals
* Autocomplete (inline) as an optional feature.
* Expand support for full Prescribe PDL (drawing/text commands, not just settings/configuration).
* Build a printer management pane (history of devices, quick-send, etc).
* Add 'dry-run' mode to preview what will be transmitted before sending.
* Export command reference as a searchable manual.

### Status
This project is under active development.

Core features (syntax highlighting, suggestion pane, error pane, JSON-driven validation, format detection and formatting) are working. Printer integration and LPR backend commands are in progress.

![Demo of Address Book Converter](/media/prescribe_ide.gif)
