"""
Functions for encoding content and generating data URLs.

This script provides functions for encoding content as base64 and generating data URLs
representing files. All files are treated as binary to ensure consistent handling
across platforms.
"""
import sys
import base64
import mimetypes


def encode_content(content):
    """Encodes binary content as base64.

    Args:
      content: The binary content to encode.

    Returns:
      The base64 encoded content as string.
    """
    return base64.b64encode(content).decode('ascii')


def encode_for_data_url(filename):
    """Encodes a file as a base64 data URL.

    Args:
      filename: The path to the file to encode.

    Returns:
      A base64 data URL representing the file.
    """
    # Guess the MIME type based on the filename
    mediatype, _ = mimetypes.guess_type(filename)
    if mediatype is None:
        mediatype = "application/octet-stream"  # Default to generic binary type

    with open(filename, 'rb') as f:
        content = f.read()

    encoded_data = encode_content(content)
    uri = f"data:{mediatype};base64,{encoded_data}"
    return uri


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chordinals.py encode <filename>")
        sys.exit(1)

    input_filename = sys.argv[2]
    output_uri = encode_for_data_url(input_filename)
    print(output_uri)
