"""
Functions for encoding content based on its MIME type and generating data URL's.

This script provides functions for encoding content as base64 and generating data URL's
representing files.
"""
import sys
import base64
import mimetypes

def encode_content(content, mediatype):
    """Encodes content based on its MIME type.

    Args:
      content: The content to encode.
      mediatype: The MIME type of the content.

    Returns:
      The encoded content as bytes.
    """

    if mediatype.startswith("text/") or mediatype == "application/json":
        # Text mode, encode the content as UTF-8 and quote it
        text_bytes = content.encode("utf-8")
        base64_bytes = base64.b64encode(text_bytes)
        encoded_content = base64_bytes.decode("utf-8")
    else:
        # Binary mode, encode the content as base64
        encoded_content = base64.b64encode(content)
    return encoded_content


def encode_for_data_url(filename):
    """Encodes a file as a base64 data URL.

    Args:
      filename: The path to the file to encode.

    Returns:
      A base64 data URL representing the file.
    """

    # Guess the MIME type based on the filename
    mediatype, _ = mimetypes.guess_type(filename)
    # use text/plain for json, for now to test
    #if mediatype == "application/json":
    #    mediatype = "text/plain"
    if mediatype is None:
        mediatype = "application/octet-stream"  # Default to generic binary type

    mode = "r" if (mediatype.startswith("text/") or mediatype == "application/json") else "rb"

    with open(filename, mode) as f:
        try:
            content = f.read()
        except UnicodeDecodeError:
            # Fallback to binary mode if text mode fails
            with open(filename, "rb") as f:
                content = f.read()
                mediatype = "application/octet-stream"

    encoded_data = encode_content(content, mediatype)
    # Include charset=utf-8 for text-based MIME types
    #print(mediatype)
    if mediatype.startswith("text/") or mediatype == "application/json":
        #uri = f"data:{mediatype};charset=utf-8,{encoded_data}"
        uri = f"data:{mediatype};base64,{encoded_data}"
    #else:
    #    if mediatype == "application/json": # must be utf-8 per JSON spec
    #        uri = f"data:{mediatype};base64,{encoded_data}"
    else:
        uri = f"data:{mediatype};base64,{encoded_data.decode()}"


    return uri


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chordinals.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_uri = encode_for_data_url(input_filename)
    print(output_uri)
