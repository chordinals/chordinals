# Data URI Encoder

This script encodes files into data URL's, supporting various file types and correctly handling both text and binary data.

## Features

- **MIME Type Detection:** Automatically determines the MIME type of the input file using the `mimetypes` module.
- **Text and Binary Handling:** Correctly encodes both text and binary files.
- **Base64 Encoding for Binary & Text:** Encodes binary and text content using base64.
- **Error Handling:** Includes fallback mechanisms to handle potential errors during file reading.

## Usage

1.  **Save the script:** Save the code as a Python file (e.g., `chordinals.py`).
2.  **Run from the command line:**

    ```bash
    python chordinals.py encode <filename>
    ```

    Replace `<filename>` with the path to the file you want to encode.

    The script will output the data URI representation of the file to the console.

## Testing

Unit tests are provided in the `tests` directory. To run the tests:

1.  **Make sure you have the `tests` directory** with the test files (`test.txt`, `test.png`, etc.) in the same directory as the script.
2.  **Run the tests from the command line:**

    ```bash
    python -m unittest tests/test_encoding.py
    ```

## Example

```bash
python chordinals.py encode my_image.png
```
