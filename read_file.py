#!/usr/bin/env python3
"""
File Reader Script
Reads any file on the hard drive and outputs the filename and first 160 lines in a code block.
"""

import os
import sys
import argparse
from pathlib import Path


def read_file_content(file_path, max_lines=160):
    """
    Read the content of a file and return the first max_lines lines.
    
    Args:
        file_path (str): Path to the file to read
        max_lines (int): Maximum number of lines to read (default: 160)
    
    Returns:
        tuple: (success, content_lines, error_message)
    """
    try:
        # Convert to Path object for better handling
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, [], f"File does not exist: {file_path}"
        
        # Check if it's a file (not a directory)
        if not path.is_file():
            return False, [], f"Path is not a file: {file_path}"
        
        # Try to read the file with different encodings
        encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as file:
                    lines = []
                    for i, line in enumerate(file):
                        if i >= max_lines:
                            break
                        lines.append(line.rstrip('\n\r'))
                    return True, lines, None
            except UnicodeDecodeError:
                continue
        
        # If all text encodings fail, try binary mode
        try:
            with open(path, 'rb') as file:
                content = file.read(max_lines * 100)  # Approximate bytes for lines
                lines = content.decode('utf-8', errors='replace').split('\n')[:max_lines]
                return True, lines, "Note: File read in binary mode with error replacement"
        except Exception as e:
            return False, [], f"Failed to read file: {str(e)}"
            
    except Exception as e:
        return False, [], f"Error accessing file: {str(e)}"


def format_output(file_path, lines, error_message=None, show_line_numbers=True):
    """
    Format the output with filename and content in a code block.
    
    Args:
        file_path (str): Path to the file
        lines (list): List of lines from the file
        error_message (str): Optional error message
        show_line_numbers (bool): Whether to show line numbers
    """
    print(f"\n{'='*80}")
    print(f"FILE: {file_path}")
    if error_message:
        print(f"NOTE: {error_message}")
    print(f"LINES: {len(lines)} (showing first 160)")
    print(f"{'='*80}")
    
    print("```")
    for i, line in enumerate(lines, 1):
        if show_line_numbers:
            print(f"{i:3d}: {line}")
        else:
            print(line)
    print("```")
    print(f"{'='*80}\n")


def main():
    """Main function to handle command line arguments and file reading."""
    parser = argparse.ArgumentParser(
        description="Read any file and display first 160 lines in a code block",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python read_file.py "C:\\path\\to\\file.txt"
  python read_file.py "C:\\path\\to\\file.cs" --lines 100
  python read_file.py "C:\\path\\to\\file.py" --no-line-numbers
        """
    )
    
    parser.add_argument(
        'file_path',
        help='Path to the file to read'
    )
    
    parser.add_argument(
        '--lines',
        type=int,
        default=160,
        help='Maximum number of lines to read (default: 160)'
    )
    
    parser.add_argument(
        '--no-line-numbers',
        action='store_true',
        help='Don\'t show line numbers in output'
    )
    
    # If no arguments provided, ask for file path
    if len(sys.argv) == 1:
        print("File Reader Script")
        print("-" * 40)
        file_path = input("Enter the full path to the file: ").strip()
        if not file_path:
            print("No file path provided. Exiting.")
            return
        
        # Create args object manually
        class Args:
            def __init__(self):
                self.file_path = file_path
                self.lines = 160
                self.no_line_numbers = False
        
        args = Args()
    else:
        args = parser.parse_args()
    
    # Expand user path and environment variables
    file_path = os.path.expanduser(os.path.expandvars(args.file_path))
    
    # Read the file
    success, lines, error_message = read_file_content(file_path, args.lines)
    
    if success:
        format_output(
            file_path, 
            lines, 
            error_message, 
            show_line_numbers=not args.no_line_numbers
        )
    else:
        print(f"\nERROR: {error_message}")
        print(f"FILE: {file_path}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
