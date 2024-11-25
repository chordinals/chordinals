# Chordinals early beta 0.1

[Chordinals](https://www.chordinals.com/) are onchain NFT's on the Chia blockchain. They must only use onchain URI's in the 3 NFT1 URI fields, uri's, metadata uri's and license uri's.

There are two scripts, one for encoding and one for minting an individual Chordinal. We'll probably combine these into one script soon.

This is an early beta release, and CLI instructions may change as we improve the code in future versions.

## Mint a Chordinal

### To mint a single Chordinal

- Review the values in the template.json file, updating the wallet_id and royalty values etc. as needed

```
python3 chordinals-mint.py urifile metadatafile.json address feemojos
```

where urifile is the content file of the Chordinal, metadatafile.json is the CHIP-0007 metadata file for it, address is the address for the chordinal to be sent to, and feemojos is the blockchain fee in mojos to incentivize farmers to include the mint transaction in a block.

#### Example Usage

```
python3 chordinals-mint.py test.png metadatatest.json xch1cchazmc92k370genxxpyuzqhtyn8m2acv46n3ue2qwnpu5s4urdqsk9fnj 100
```

### Reference Links

- [Chordinals](https://www.chordinals.com/)
- [Chordiforge](https://www.chordiforge.com/)
- [Anarkoic](https://www.anarkoic.com/)

## Data URI Encoder

This script encodes files into data URL's, supporting various file types and correctly handling both text and binary data.

### Features

- **MIME Type Detection:** Automatically determines the MIME type of the input file using the `mimetypes` module.
- **Text and Binary Handling:** Correctly encodes both text and binary files.
- **Base64 Encoding for Binary & Text:** Encodes binary and text content using base64.
- **Error Handling:** Includes fallback mechanisms to handle potential errors during file reading.

### Usage

1.  **Save the script:** Save the code as a Python file (e.g., `chordinals.py`).
2.  **Run from the command line:**

    ```bash
    python chordinals.py encode <filename>
    ```

    Replace `<filename>` with the path to the file you want to encode.

    The script will output the data URI representation of the file to the console.

### Testing

Unit tests are provided in the `tests` directory. To run the tests:

1.  **Make sure you have the `tests` directory** with the test files (`test.txt`, `test.png`, etc.) in the same directory as the script.
2.  **Run the tests from the command line:**

    ```bash
    python -m unittest tests/test_encoding.py
    ```

### Example

```bash
python chordinals.py encode my_image.png
```
