import os
import hashlib
import argparse

# Set the file extensions to scan for here
# Example: EXTENSIONS = ['.txt', '.py', '.jpg'] to scan for text, Python, and JPEG files
# Leave as None or [] to scan all files
EXTENSIONS = ['.7z', '.zip', '.tar']  # Change this to your desired extensions

def calculate_md5(file_path):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            # Read file in 4MB chunks for better performance
            for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def scan_directory(directory_path, extensions=None):
    """Recursively scan directory for files with specific extensions and calculate their MD5 hashes"""
    results = []
    
    # Normalize extensions (ensure they start with a dot)
    if extensions:
        extensions = [ext if ext.startswith('.') else '.' + ext for ext in extensions]
    
    # Walk through directory tree
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if file has one of the specified extensions (or all files if no extensions specified)
            if extensions is None or len(extensions) == 0 or any(file.lower().endswith(ext.lower()) for ext in extensions):
                # Print file path before processing
                print(f"Processing: {file_path}")
                md5_hash = calculate_md5(file_path)
                if md5_hash:
                    results.append((file_path, md5_hash))
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Scan directory for files and calculate their MD5 hashes")
    parser.add_argument("directory", help="Directory path to scan")
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist.")
        return
    
    # Scan directory
    print(f"Scanning directory: {args.directory}")
    if EXTENSIONS:
        print(f"Looking for files with extensions: {', '.join(EXTENSIONS)}")
    else:
        print("Looking for all files")
    
    results = scan_directory(args.directory, EXTENSIONS)
    
    # Output results
    print("\nResults:")
    print("-" * 50)
    for file_path, md5_hash in results:
        print(f"{file_path} | {md5_hash}")

if __name__ == "__main__":
    main()