import os
import argparse
import hashlib

def calculate_digest(file_path):
    """
    Calculate file digest based on file size:
    - For files < 1MB: MD5 of entire file
    - For files >= 1MB: MD5 of first 500KB + last 500KB
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Digest string or None if error
    """
    try:
        file_size = os.path.getsize(file_path)
        md5_hash = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            if file_size < 1024 * 1024:  # Less than 1MB
                # Read entire file
                content = f.read()
                md5_hash.update(content)
            else:  # 1MB or larger
                # Read first 500KB
                first_part = f.read(500 * 1024)
                md5_hash.update(first_part)
                
                # Seek to last 500KB
                if file_size > 1024 * 1024:  # Larger than 1MB
                    f.seek(-500 * 1024, 2)  # 2 means from end of file
                    last_part = f.read(500 * 1024)
                    md5_hash.update(last_part)
        
        return md5_hash.hexdigest()
    except Exception as e:
        return None

def traverse_directory(path, depth=0, output_file=None):
    """
    Recursively traverse a directory and print all files and folders with indentation
    based on directory depth. Also writes output to a file if specified.
    
    Args:
        path (str): The directory path to traverse
        depth (int): Current depth level for indentation (default: 0)
        output_file (file object): File object to write output to (default: None)
    """
    # Create indentation based on depth
    indent = "  " * depth
    
    try:
        # Get all items in the directory
        items = os.listdir(path)
        # Sort items to have consistent ordering (directories first, then files)
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        
        for item in items:
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                # Print directory name with trailing slash
                output_line = f"{indent}[DIR] {item}/"
                print(output_line)
                if output_file:
                    output_file.write(output_line + "\n")
                # Recursively traverse subdirectory
                traverse_directory(item_path, depth + 1, output_file)
            else:
                # For files, also calculate and display digest
                digest = calculate_digest(item_path)
                if digest:
                    output_line = f"{indent}[FILE] {item} (Digest: {digest})"
                else:
                    output_line = f"{indent}[FILE] {item}"
                print(output_line)
                if output_file:
                    output_file.write(output_line + "\n")
                
    except PermissionError:
        error_line = f"{indent}[ERROR] Permission denied: {path}"
        print(error_line)
        if output_file:
            output_file.write(error_line + "\n")
    except FileNotFoundError:
        error_line = f"{indent}[ERROR] Directory not found: {path}"
        print(error_line)
        if output_file:
            output_file.write(error_line + "\n")
    except Exception as e:
        error_line = f"{indent}[ERROR] {e}"
        print(error_line)
        if output_file:
            output_file.write(error_line + "\n")

def main():
    parser = argparse.ArgumentParser(description="Recursively traverse a directory and print all files and folders with indentation")
    parser.add_argument("directory", nargs="?", default=".", help="Directory path to traverse (default: current directory)")
    
    args = parser.parse_args()
    
    # Check if the provided path exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        return
    
    # Check if the provided path is a directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a directory.")
        return
    
    # Create output file path
    output_file_path = os.path.join(args.directory, "list.txt")
    
    try:
        # Open output file for writing
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            # Print the root directory
            root_line = f"[ROOT] {os.path.abspath(args.directory)}/"
            print(root_line)
            output_file.write(root_line + "\n")
            
            # Traverse the directory
            traverse_directory(args.directory, output_file=output_file)
        
        print(f"\nOutput also written to: {output_file_path}")
        
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    main()