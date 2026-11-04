---
description: Windows PowerShell execution syntax and stdout encoding invariants
globs: ["*"]
---

# Windows PowerShell & UTF-8 Console Invariants

1. **Command Chaining in PowerShell**:
   - NEVER use `&&` or `||` as command separators in Windows PowerShell.
   - ALWAYS use `;` (semicolon) or separate command invocations:
     ```powershell
     # Correct:
     git add -A; git commit -m "feat: update"
     # Incorrect (causes parser error):
     git add -A && git commit -m "feat: update"
     ```

2. **Standard Output UTF-8 Encoding**:
   - Windows default console encoding (`cp1252`) fails on currency symbols (`₹`, `€`) and emojis.
   - Always reconfigure stdout at the top of executable scripts and CLI entrypoints:
     ```python
     import sys
     if sys.stdout.encoding.lower() != 'utf-8':
         try:
             sys.stdout.reconfigure(encoding='utf-8')
         except Exception:
             pass
     ```
