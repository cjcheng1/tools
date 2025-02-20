import os
import shutil
import subprocess

def change_file_permissions(file_path, permissions='664'):
    """Change permissions for the specified file."""
    try:
        print(f"Changing permissions for {file_path}")
        subprocess.run(['sudo', 'chmod', permissions, file_path], check=True)
        print(f"Permissions changed for {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change file permissions {file_path}: {e}")

def delete_file(file_path):
    """Delete a file if it exists."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

def compress_directory(source_dir, output_zip_file):
    """Compress the source directory into a ZIP file."""
    try:
        shutil.make_archive(output_zip_file, 'zip', source_dir)
        print(f"Directory {source_dir} compressed into {output_zip_file}.zip")
    except Exception as e:
        print(f"Error compressing directory {source_dir}: {e}")

def main():
    # 定義目標文件和目錄
    utils_directory = '/home/linaro/utils'
    make_swap_directory = os.path.join(utils_directory, 'make_swap')
    swap_file_path = os.path.join(make_swap_directory, 'swapfile')
    backup_zip = '/home/linaro/utils_backup'
    
    # 修改swapfile的權限以便刪除
    change_file_permissions(swap_file_path, '664')
    
    # 刪除swapfile
    delete_file(swap_file_path)
    
    # 壓縮utils目錄
    compress_directory(utils_directory, backup_zip)

if __name__ == "__main__":
    main()
