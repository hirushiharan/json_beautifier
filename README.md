# JSON Beautifier

A Python tool to clean and format "almost-JSON" data that contains common formatting issues.

## Features

This tool can handle and fix:
- **Extra braces**: `{{ ... }}` → `[{ ... }]`
- **Trailing commas**: Removes dangling commas in objects and arrays
- **Unescaped newlines**: Properly escapes newlines within JSON strings

## Installation

No installation required! Just download `json_beautifier.py` and run it with Python 3.6+.

## Usage

### Command Line Interface

```bash
# Read from file, write to file with custom indentation
python json_beautifier.py -i input.txt -o output.json --indent 4
```

### Options

- `-i, --input FILE`: Input file (default: stdin)
- `-o, --output FILE`: Output file (default: stdout)  
- `--indent N`: Number of spaces for indentation (default: 2)
- `--version`: Show version information
- `-h, --help`: Show help message

### Python API

```python
from json_beautifier import clean_almost_json, beautify_json

# Clean almost-JSON text
raw_text = '{{ "name": "test", }}'
cleaned = clean_almost_json(raw_text)  # Returns: '[{ "name": "test" }]'

# Clean and beautify
beautified = beautify_json(raw_text)   # Returns formatted JSON
```

## Examples

### Input
```json
{{ 
  "name": "John Doe",
  "age": 30,
  "city": "New York
with newlines",
  "hobbies": [
    "reading",
    "gaming",
    "cooking",
  ],
}}
```

### Output
```json
[
  {
    "name": "John Doe",
    "age": 30,
    "city": "New York\\nwith newlines",
    "hobbies": [
      "reading",
      "gaming", 
      "cooking"
    ]
  }
]
```

## Testing

Run the test examples:

```bash
python test_example.py
```

## Common Use Cases

- Cleaning JSON data copied from logs or debug output
- Processing JSON-like data from APIs with formatting issues
- Converting JavaScript object literals to valid JSON
- Fixing JSON data with trailing commas (common in JavaScript)

## Error Handling

The tool validates that the cleaned text is valid JSON. If parsing fails, it will:
- Display a helpful error message
- Exit with status code 1
- Show the line number and position of JSON syntax errors

## License

See [LICENSE](LICENSE) file for details.