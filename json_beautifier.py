#!/usr/bin/env python3
"""
JSON Beautifier - A tool to clean and format "almost-JSON" data

This script can handle:
- Extra braces: "{{ ... }}" -> "[{ ... }]"
- Trailing commas in objects/arrays
- Unescaped newlines in JSON strings
"""

import json
import re
import sys
import argparse
from typing import TextIO


def clean_almost_json(raw: str) -> str:
    """
    Clean "almost-JSON" text to make it valid JSON.
    
    Args:
        raw: Raw input string containing almost-JSON
        
    Returns:
        Cleaned JSON string
    """
    # 1. Trim & collapse "{{ … }}" to "[{ … }]"
    cleaned = re.sub(r'^\s*\{\s*\{', '[{', raw.strip(), count=1)
    cleaned = re.sub(r'\}\s*\}\s*$', '}]', cleaned, count=1)
    
    # 1b. Fix malformed ending: },} should be }]
    cleaned = re.sub(r'\},\s*\}\s*$', '}]', cleaned)

    # 2. Remove trailing commas inside objects/arrays
    cleaned = re.sub(r',(\s*[\]\}])', r'\1', cleaned)

    # 3. Add missing commas between array elements (when closing quote is followed by whitespace and opening quote)
    cleaned = re.sub(r'"\s*\n\s*"', '",\n        "', cleaned)
    
    # 4. Fix unquoted identifiers in examples (common pattern: word-digit combinations)
    # This handles cases like 'CZ1182-011' that should be "'CZ1182-011'"
    cleaned = re.sub(r"(\s)([A-Z]+\d+(?:-\d+)?)(\))", r"\1'\2'\3", cleaned)
    
    # 4. Replace literal newlines inside JSON strings with \n
    # Use DOTALL flag to make . match newlines, and handle multi-line strings
    def _escape_lines(match):
        string_content = match.group(0)
        # Replace literal newlines with \n escape sequence
        string_content = string_content.replace('\n', '\\n')
        # Replace literal tabs with \t escape sequence
        string_content = string_content.replace('\t', '\\t')
        # Replace other control characters
        string_content = re.sub(r'[\x00-\x1f\x7f-\x9f]', lambda m: f'\\u{ord(m.group(0)):04x}', string_content)
        return string_content
    
    # Use DOTALL flag to match newlines within strings
    cleaned = re.sub(r'"(?:[^"\\]|\\.)*"', _escape_lines, cleaned, flags=re.DOTALL)

    return cleaned


def beautify_json(input_text: str, indent: int = 2) -> str:
    """
    Clean and beautify JSON text.
    
    Args:
        input_text: Raw input containing almost-JSON
        indent: Number of spaces for indentation
        
    Returns:
        Pretty-printed JSON string
        
    Raises:
        json.JSONDecodeError: If the cleaned text is still not valid JSON
    """
    cleaned_text = clean_almost_json(input_text)
    parsed = json.loads(cleaned_text)  # Validate JSON
    return json.dumps(parsed, indent=indent, ensure_ascii=False)


def process_input(input_file: TextIO, output_file: TextIO, indent: int = 2) -> None:
    """
    Process input from file or stdin and write to output file or stdout.
    
    Args:
        input_file: Input file object (stdin or opened file)
        output_file: Output file object (stdout or opened file)
        indent: Number of spaces for indentation
    """
    try:
        raw_text = input_file.read()
        if not raw_text.strip():
            print("Warning: Empty input", file=sys.stderr)
            return
            
        beautified = beautify_json(raw_text, indent)
        output_file.write(beautified)
        output_file.write('\n')
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON after cleaning - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Clean and beautify almost-JSON data",
        epilog="Examples:\n"
               "  echo '{{ \"name\": \"test\", }}' | python json_beautifier.py\n"
               "  python json_beautifier.py -i input.txt -o output.json\n"
               "  python json_beautifier.py --indent 4 < data.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input',
        type=argparse.FileType('r', encoding='utf-8'),
        default=sys.stdin,
        help='Input file (default: stdin)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=argparse.FileType('w', encoding='utf-8'),
        default=sys.stdout,
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help='Number of spaces for indentation (default: 2)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='JSON Beautifier 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        process_input(args.input, args.output, args.indent)
    finally:
        # Close files if they're not stdin/stdout
        if args.input != sys.stdin:
            args.input.close()
        if args.output != sys.stdout:
            args.output.close()


if __name__ == '__main__':
    main()