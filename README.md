# Chordinals early beta 0.1

[Chordinals](https://www.chordinals.com/) are onchain NFT's on the Chia blockchain. They must only use onchain URI's in the 3 NFT1 URI fields, uri's, metadata uri's and license uri's.

There are two scripts, one for encoding and one for minting an individual Chordinal.

This is an early beta release, and CLI instructions may change as we improve the code in future versions.

## Mint a Chordinal

### To mint a single Chordinal

1. Review the values in the `template.json` file, updating the `wallet_id` and `royalty` values etc. as needed

2. Run the minting script:

```bash
python3 chordinals_mint.py urifile metadatafile.json address feemojos [--dryrun]
```

Arguments:

- `urifile`: The content file of the Chordinal
- `metadatafile.json`: The CHIP-0007 metadata file
- `address`: The address where the chordinal will be sent
- `feemojos`: The blockchain fee in mojos to incentivize farmers
- `--dryrun`: Optional flag to preview the transaction without submitting to blockchain

#### Example Usage

```bash
# Preview without minting
python3 chordinals_mint.py test.png metadatatest.json xch1cchazmc92k370genxxpyuzqhtyn8m2acv46n3ue2qwnpu5s4urdqsk9fnj 100 --dryrun

# Mint a Chordinal
python3 chordinals_mint.py test.png metadatatest.json xch1cchazmc92k370genxxpyuzqhtyn8m2acv46n3ue2qwnpu5s4urdqsk9fnj 100
```

## Data URI Encoder

The `chordinals.py` script encodes files into data URLs for use in Chordinals. It handles all file types consistently and preserves file content exactly.

### Features

- **MIME Type Detection:** Automatically determines the MIME type of input files
- **Consistent Encoding:** Treats all files as binary data to ensure consistent results
- **Base64 Encoding:** Encodes content using base64 for blockchain compatibility

### Usage

```bash
python chordinals.py encode <filename>
```

Replace `<filename>` with the path to the file you want to encode. The script will output the data URI representation of the file.

### Testing

The repository includes unit tests to verify encoding consistency. To run the tests:

```bash
python -m pytest test_chordinals.py -v
```

### Reference Links

- [Chordinals](https://www.chordinals.com/)
- [Chordifun](https://www.chordifun.com/)
- [Anarkoic](https://www.anarkoic.com/)
