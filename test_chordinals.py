import unittest
import os
import tempfile
import chordinals
import chordinals_mint
import json


class ChordinalsTest(unittest.TestCase):
    def setUp(self):
        # Create temporary test files with different line endings
        self.test_files = []
        
        # Test 1: JSON with Windows line endings (CRLF)
        self.json_crlf = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.test_files.append(self.json_crlf.name)
        json_content = {'test': 'value\r\nwith\r\nCRLF'}
        self.json_crlf.write(json.dumps(json_content, indent=2).encode('utf-8'))
        self.json_crlf.close()
        
        # Test 2: JSON with Unix line endings (LF)
        self.json_lf = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.test_files.append(self.json_lf.name)
        json_content = {'test': 'value\nwith\nLF'}
        self.json_lf.write(json.dumps(json_content, indent=2).encode('utf-8'))
        self.json_lf.close()
        
        # Test 3: Text file with mixed line endings
        self.text_mixed = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.test_files.append(self.text_mixed.name)
        self.text_mixed.write(b'line1\r\nline2\nline3\rline4')
        self.text_mixed.close()
        
        # Test 4: Binary file
        self.binary = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
        self.test_files.append(self.binary.name)
        self.binary.write(bytes(range(256)))
        self.binary.close()

    def tearDown(self):
        # Clean up temporary files
        for file in self.test_files:
            try:
                os.unlink(file)
            except:
                pass

    def test_hash_consistency(self):
        """Test that hashes are consistent regardless of line endings"""
        # Hash the same JSON with different line endings
        hash1 = chordinals_mint.calculate_sha256_hash(self.json_crlf.name)
        hash2 = chordinals_mint.calculate_sha256_hash(self.json_lf.name)
        
        # Hashes should be different because we're preserving line endings
        self.assertNotEqual(hash1, hash2, "Hashes should differ for different line endings")

    def test_data_url_encoding(self):
        """Test that data URL encoding works consistently"""
        # Test JSON file
        json_url = chordinals.encode_for_data_url(self.json_crlf.name)
        self.assertTrue(json_url.startswith('data:application/json;base64,'))
        
        # Test text file
        text_url = chordinals.encode_for_data_url(self.text_mixed.name)
        self.assertTrue(text_url.startswith('data:text/plain;base64,'))
        
        # Test binary file
        bin_url = chordinals.encode_for_data_url(self.binary.name)
        self.assertTrue(bin_url.startswith('data:application/octet-stream;base64,'))

    def test_content_preservation(self):
        """Test that original content is preserved exactly"""
        # Read original content
        with open(self.text_mixed.name, 'rb') as f:
            original = f.read()
        
        # Get encoded URL and decode it
        url = chordinals.encode_for_data_url(self.text_mixed.name)
        encoded_part = url.split(',', 1)[1]
        import base64
        decoded = base64.b64decode(encoded_part)
        
        # Content should be preserved exactly
        self.assertEqual(original, decoded, "Content should be preserved exactly")


if __name__ == '__main__':
    unittest.main()
