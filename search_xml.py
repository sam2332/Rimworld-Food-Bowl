#! /usr/bin/env python3
"""XML Search Script
Searches for a keyword in XML files across specified directories.
invoking:
python search_xml.py [keyword] [limited_path]
If limited_path is provided, it will search only in that directory.
"""

import os
import sys
import xml.etree.ElementTree as ET
from typing import Optional, List

# Fix raw string literals to avoid escape sequence warnings

search_roots = [
    r'C:\Program Files (x86)\Steam\steamapps\workshop\content\294100',
    r"C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Data"
    r"C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Mods",
]
keyword = sys.argv[1] if len(sys.argv) > 1 else 'Portal Gun'
limited_path = sys.argv[2] if len(sys.argv) > 2 else None
if limited_path:
    search_roots = [limited_path]   
def read_xml_file_robust(file_path: str) -> Optional[List[str]]:
    """
    Robustly read XML file content with multiple encoding attempts.
    Returns list of lines or None if file cannot be read.
    """
    # List of encodings to try in order
    encodings_to_try = [
        'utf-8',
        'utf-8-sig',  # UTF-8 with BOM
        'latin1',     # ISO-8859-1, can decode any byte sequence
        'cp1252',     # Windows-1252, common for Windows files
        'iso-8859-1', # Similar to latin1
        'utf-16',     # UTF-16 with BOM detection
        'utf-16le',   # UTF-16 Little Endian
        'utf-16be',   # UTF-16 Big Endian
    ]
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                lines = f.readlines()
            
            # Validate that it's actually XML content
            if is_valid_xml_content(lines):
                return lines
                
        except (UnicodeDecodeError, UnicodeError, OSError) as e:
            continue  # Try next encoding
        except Exception as e:
            # For other errors, log and continue
            continue
    
    # If all encodings fail, try one more time with utf-8 and ignore errors
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        return lines
    except Exception:
        return None

def is_valid_xml_content(lines: List[str]) -> bool:
    """
    Check if the content looks like valid XML.
    """
    if not lines:
        return False
    
    # Look for XML declaration or root elements in first few lines
    first_few_lines = ''.join(lines[:5]).strip()
    xml_indicators = ['<?xml', '<Defs>', '<LanguageData>', '<ThingDefs>', '<GameDef>', '<Def>', '<xml']
    
    return any(indicator in first_few_lines for indicator in xml_indicators)

def search_xml_files():
    """
    Search for keyword in XML files across specified directories.
    """
    for search_root in search_roots:
        if not os.path.exists(search_root):
            print(f"Warning: Search path does not exist: {search_root}")
            continue
            
        for root, dirs, files in os.walk(search_root):
            for file in files:
                if file.lower().endswith('.xml'):
                    file_path = os.path.join(root, file)
                    
                    lines = read_xml_file_robust(file_path)
                    if lines is None:
                        print(f'Error: Could not read {file_path} with any encoding')
                        continue
                    
                    # Search for keyword in lines
                    matches = [i for i, line in enumerate(lines) if keyword.lower() in line.lower()]
                    
                    if matches:
                        file_size = os.path.getsize(file_path)
                        for i in matches:
                            start = max(0, i - 4)
                            end = min(len(lines), i + 5)
                            
                            print(f'File: {file_path}')
                            print(f'Size: {file_size} bytes')
                            print(f'Match at line {i+1}:')
                            print('```xml')
                            for j in range(start, end):
                                print(lines[j], end='')
                            print('```\n')

if __name__ == "__main__":
    search_xml_files()
