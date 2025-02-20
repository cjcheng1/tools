import os
import zipfile
import shutil
import hashlib
import json

# 定義版本和OTA URL
FIRMWARE_VERSION = "012_alpha_02"
OTA_URL = "https://www.test123.com/OTA_FW_Andarx.zip"

def compress_directory(source_dir, output_zip_file):
    """Compress the source directory into a ZIP file and create a JSON file with details."""
    shutil.make_archive(output_zip_file, 'zip', source_dir)
    print(f"Directory {source_dir} compressed into {output_zip_file}.zip")

    # Calculate checksum of the compressed file
    zip_file_path = f"{output_zip_file}.zip"
    checksum = calculate_checksum(zip_file_path)

    # Create firmware version JSON
    firmware_info = {
        "version": FIRMWARE_VERSION,
        "ota-url": OTA_URL,
        "sha256": checksum
    }
    json_file_path = os.path.join(os.path.dirname(zip_file_path), 'firmwareX_version.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(firmware_info, json_file, indent=4)

    print(f"Created firmware metadata JSON file: {json_file_path}")

def calculate_checksum(file_path, algorithm='sha256'):
    """Calculate the checksum of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()

def extract_zip(zip_file_path, target_directory, json_file_path):
    """Extract a ZIP file to the target directory if the checksum matches using JSON file."""
    expected_checksum, _, _ = read_firmware_json(json_file_path)

    actual_checksum = calculate_checksum(zip_file_path)
    if actual_checksum != expected_checksum:
        print(f"Checksum mismatch! Expected {expected_checksum}, but got {actual_checksum}.")
        return False

    print("Checksum verified. Proceeding with extraction.")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            zip_ref.extract(member, target_directory)
            print(f"Extracted {member} to {target_directory}")
            
    return True

def read_firmware_json(json_file_path):
    """Read version, ota-url, and checksum from firmware JSON file."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data['sha256'], data['ota-url'], data['version']

def process_compression(source_dir, output_zip_file):
    """Wrapper function to perform compression operation."""
    compress_directory(source_dir, output_zip_file)

def process_extraction(zip_file_path, json_file_path, target_directory):
    """Wrapper function to perform extraction operation."""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    success = extract_zip(zip_file_path, target_directory, json_file_path)
    if success:
        print("Extraction completed successfully.")
    else:
        print("Extraction failed due to checksum mismatch.")

def main():
    # 定義變數，例如：
    compress_source_dir = '/home'
    compress_output_zip = '/path/to/output'

    extract_zip_file = '/path/to/home_backup.zip'
    extract_json_file = '/path/to/firmwareX_version.json'
    extract_target_dir = '/home/linaro'

    # 操作選擇，壓縮或解壓
    action = 'compress'  # 或 'extract'

    if action == 'compress':
        process_compression(compress_source_dir, compress_output_zip)
    elif action == 'extract':
        process_extraction(extract_zip_file, extract_json_file, extract_target_dir)
    else:
        print("Invalid action specified.")

if __name__ == "__main__":
    main()
