import json
import hashlib
import sys
import subprocess
import tempfile
import argparse
import chordinals
import mimetypes


def calculate_sha256_hash(input_filename):
    """Calculates the SHA-256 hash of a file's content.
    
    Treats all files as binary to ensure consistent hashes across platforms.

    Args:
      input_filename: The path to the file to hash.

    Returns:
      A string containing the hexadecimal representation of the hash.
    """
    with open(input_filename, 'rb') as f:
        content = f.read()
    sha256_hash = hashlib.sha256(content).hexdigest()
    return sha256_hash


def main():
    parser = argparse.ArgumentParser(description="Mint a chordinal NFT")
    parser.add_argument("urifile", type=str, help="Path to the URI file")
    parser.add_argument("metadatafile", type=str,
                        help="Path to the metadata JSON file")
    parser.add_argument("address", type=str, help="Your wallet address")
    parser.add_argument("feemojos", type=str, help="Feemojos to spend")
    parser.add_argument("--dryrun", action="store_true",
                        help="Perform a dry run without actually minting")
    args = parser.parse_args()

    urifile = args.urifile  # sys.argv[1]
    metadatafile = args.metadatafile  # sys.argv[2]
    address = args.address  # sys.argv[3]
    feemojos = args.feemojos  # sys.argv[4]

    # 1. Encode urifile and calculate its hash
    uri_data_uri = chordinals.encode_for_data_url(urifile)
    uri_hash = calculate_sha256_hash(urifile)

    # 2. Encode metadatafile.json and calculate its hash
    metadata_data_uri = chordinals.encode_for_data_url(metadatafile)
    metadata_hash = calculate_sha256_hash(metadatafile)

    # 3. Read template.json
    with open("template.json", "r") as f:
        template_json = json.load(f)

    # 4. & 5. Replace values in template.json
    template_json["target_address"] = address
    template_json["fee"] = feemojos
    template_json["uris"] = [uri_data_uri]
    template_json["hash"] = uri_hash
    template_json["meta_uris"] = [metadata_data_uri]
    template_json["meta_hash"] = metadata_hash

    # --- Create a temporary file ---
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as temp_file:
        json.dump(template_json, temp_file, indent=4)
        temp_file_path = temp_file.name

    # Construct the chia rpc command using the temporary file path
    command = f"chia rpc wallet nft_mint_nft -j {temp_file_path}"

    print(command)

    # Run the command
    if args.dryrun:
        print(template_json)
    else:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error minting NFT: {e}")


if __name__ == "__main__":
    main()
