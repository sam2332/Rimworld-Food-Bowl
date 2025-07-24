---
applyTo: '**'
---
# Coding Standards and Domain Knowledge Guidelines

**IMPORTANT: Use Decompiled Game Files as Source of Truth**

When working on this RimWorld mod, you MUST rely on the decompiled game files in the `Game Source/` folder as your primary source of knowledge about RimWorld's code structure, APIs, and implementation details.
USE YOUR TOOLS to search and read the decompiled code, as it reflects the current state of the game.
USE POWERSHELL to search for specific classes, methods, or game systems within the decompiled files.
the installed modes are located in C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\


**Decompiled Mod Files:**
create a folder called /{modname} Source/ and run ilspycmd to extract the decompiled code for your mod.
use this command: `ilspycmd -p --nested-directories -o "0Harmony Source" "C:\Program Files (x86)\Steam\steamapps\workshop\content\294100\2009463077\Current\Assemblies\0Harmony.dll"`

you have python tools called 
**Game Files:**
Game Source Code: /Game Source/
Game XML: /Game XML DEFS/
0Harmony Code: /0Harmony Source/

**Do NOT rely on your training memory** for RimWorld-specific information, as:
- RimWorld 1.6 was released recently, and your training data may not include the latest changes
- Your training data may contain outdated information from previous versions
- Game mechanics, class structures, and APIs may have changed significantly

**Guidelines:**
0. there is a file named Mod_Base.md it is the directions that were given at the beginning of development of this mod.
1. Always examine the decompiled source code in `Game Source/` to understand current implementations
2. Look at actual class definitions, method signatures, and game logic in the decompiled files
3. When implementing mod features, reference the current game's code patterns and conventions
4. If you need to understand how a game system works, search through the decompiled files first
5. Use the semantic search and file reading tools to explore the decompiled codebase
6. ask questions first before doing anything so you can understand the context and requirements clearly.
7. If you need to implement or modify functionality, ensure it aligns with the current game logic as seen in the decompiled files.
This ensures your mod implementations are compatible with the current version of RimWorld and follow the game's actual coding patterns.

8. reference and update MOD_MEMORY.md and IMPLEMENTATION_SUMMARY.md for recent changes and fixes.
9. Mod author is The User who goes by ProgrammerLily. She is the primary developer and maintainer of this mod.
    - If you have questions about the mod's design or implementation, ask The User directly.
    - The User will provide guidance on how to proceed with specific features or fixes.

10. use reflection when possible to keep other mods happy and avoid compatibility issues.
    - If you need to access private or internal members, use reflection to avoid direct dependencies on specific implementations.
    - This allows your mod to work alongside other mods that may alter the same game systems.

11. over research but keep a scratch pad. keep that scratch pad clean and organized.
    - Use the scratch pad to jot down important findings, patterns, or code snippets you discover while exploring the decompiled files.
    - This will help you remember key details and avoid unnecessary rework later on during this chat session so dont update at the end of the session.

12. If you encounter any issues or have questions about the decompiled code, ask The User for clarification.

13. When implementing new features, ensure they are well-documented in the code and dont make drastic changes without asking The User first.