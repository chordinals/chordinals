import json
import hashlib
import sys
import subprocess
import tempfile
import chordinals


def calculate_sha256_hash(input_filename):
    """Calculates the SHA-256 hash of a file's content.

    Args:
      input_filename: The path to the file to hash.

    Returns:
      A string containing the hexadecimal representation of the hash.
    """
    with open(input_filename, 'rb') as f:
        file_content = f.read()
        sha256_hash = hashlib.sha256(file_content).hexdigest()
    return sha256_hash


def main():
    if len(sys.argv) != 5:
        print("Usage: python3 mint-chordinal.py urifile metadatafile.json address feemojos")
        sys.exit(1)

    urifile = sys.argv[1]
    metadatafile = sys.argv[2]
    address = sys.argv[3]
    feemojos = sys.argv[4]

    # 1. Encode urifile and calculate its hash
    uri_data_uri = chordinals.encode_for_data_uri(urifile)
    uri_hash = calculate_sha256_hash(urifile)

    # 2. Encode metadatafile.json and calculate its hash
    metadata_data_uri = chordinals.encode_for_data_uri(metadatafile)
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

    # Construct the chia rpc command
    # command = f"chia rpc wallet nft_mint_nft '{json.dumps(template_json)}'"
    # command = f"chia rpc wallet nft_mint_nft '{json.dumps(template_json)}'"
    # command = f"chia wallet nft mint -i 3 -ta {address} -u {uri_data_uri} -nh {uri_hash} -mu {shlex.quote(metadata_data_uri.replace("\n", "\\n"))} -mh {metadata_hash} -m {(int(feemojos)/1e12):.12f}"
    # command = f"chia rpc wallet nft_mint_nft '{template_json}'"
    print(command)

    # Run the command
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error minting NFT: {e}")


if __name__ == "__main__":
    main()
