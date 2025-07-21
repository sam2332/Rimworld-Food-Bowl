---
applyTo: '**'
---
# Coding Standards and Domain Knowledge Guidelines

**IMPORTANT: Use Decompiled Game Files as Source of Truth**

When working on this RimWorld mod, you MUST rely on the decompiled game files in the `Game Source/` folder as your primary source of knowledge about RimWorld's code structure, APIs, and implementation details.

**Do NOT rely on your training memory** for RimWorld-specific information, as:
- RimWorld 1.6 was released today (July 11, 2025)
- Your training data may contain outdated information from previous versions
- Game mechanics, class structures, and APIs may have changed significantly

**Guidelines:**
1. Always examine the decompiled source code in `Game Source/` to understand current implementations
2. Look at actual class definitions, method signatures, and game logic in the decompiled files
3. When implementing mod features, reference the current game's code patterns and conventions
4. If you need to understand how a game system works, search through the decompiled files first
5. Use the semantic search and file reading tools to explore the decompiled codebase
6. keep a notepad of any relevant findings or patterns you discover in the decompiled files to help future you or other developers.
7. ask questions first before doing anything so you can understand the context and requirements clearly.
8. If you need to implement or modify functionality, ensure it aligns with the current game logic as seen in the decompiled files.
This ensures your mod implementations are compatible with the current version of RimWorld and follow the game's actual coding patterns.

9. reference and update MOD_MEMORY.md and IMPLEMENTATION_SUMMARY.md for recent changes and fixes.