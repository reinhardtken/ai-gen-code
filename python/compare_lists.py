import os
import argparse
from pathlib import Path

def parse_list_file(file_path):
    """
    Parse a list.txt file and extract file paths.
    
    Args:
        file_path (str): Path to the list.txt file
        
    Returns:
        dict: Dictionary with file names as keys and full paths as values
    """
    file_dict = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Extract the root directory from the first line
        root_line = lines[0].strip()
        if root_line.startswith('[ROOT] '):
            root_path = Path(root_line[7:].rstrip('/'))  # Remove '[ROOT] ' and trailing '/'
        else:
            # Fallback to the directory containing the list file
            root_path = Path(file_path).parent
        
        # Process each line to extract file paths
        for line in lines[1:]:  # Skip the first line which is the root
            line = line.strip()
            if not line:
                continue
                
            # Skip error lines
            if '[ERROR]' in line:
                continue
                
            # Extract the relative path from the line
            rel_path = None
            # Lines are formatted as: "  [DIR] folder/" or "  [FILE] filename"
            if '[DIR]' in line:
                # Extract directory name (remove indentation and [DIR] tag)
                parts = line.split('[DIR] ')
                if len(parts) > 1:
                    rel_path = parts[1].rstrip('/')  # Remove trailing slash
            elif '[FILE] ' in line:
                # Extract file name (remove indentation and [FILE] tag)
                parts = line.split('[FILE] ')
                if len(parts) > 1:
                    rel_path = parts[1]
            
            # Only process if we have a valid rel_path
            if rel_path is not None:
                # Construct full path
                full_path = root_path / rel_path
                # Use the file/directory name as the key
                name = full_path.name
                file_dict[name] = str(full_path)
            
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return file_dict

def find_common_files(list1_path, list2_path):
    """
    Find files that exist in both list files.
    
    Args:
        list1_path (str): Path to the first list.txt file
        list2_path (str): Path to the second list.txt file
        
    Returns:
        list: List of tuples containing common file names and their paths from both directories
    """
    # Parse both list files
    files1 = parse_list_file(list1_path)
    files2 = parse_list_file(list2_path)
    
    # Find common file names
    common_names = set(files1.keys()) & set(files2.keys())
    
    # Create list of common files with their paths
    common_files = []
    for name in common_names:
        common_files.append((name, files1[name], files2[name]))
    
    return common_files

def delete_torrent_files(common_files):
    """
    Delete .torrent files from the first directory for files that exist in both directories.
    
    Args:
        common_files (list): List of tuples containing common file names and their paths
        
    Returns:
        int: Number of .torrent files deleted
    """
    deleted_count = 0
    
    for name, path1, path2 in common_files:
        # Check if the file in the first directory has .torrent extension
        if Path(path1).suffix.lower() == '.torrent':
            try:
                os.remove(path1)
                print(f"Deleted .torrent file: {path1}")
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting file {path1}: {e}")
    
    return deleted_count

def main():
    parser = argparse.ArgumentParser(description="Compare two list.txt files and print files that exist in both directories")
    parser.add_argument("list1", help="Path to the first list.txt file")
    parser.add_argument("list2", help="Path to the second list.txt file")
    
    args = parser.parse_args()
    
    # Check if files exist
    if not os.path.exists(args.list1):
        print(f"Error: File '{args.list1}' does not exist.")
        return
    
    if not os.path.exists(args.list2):
        print(f"Error: File '{args.list2}' does not exist.")
        return
    
    # Find common files
    common_files = find_common_files(args.list1, args.list2)
    
    # Delete .torrent files from the first directory
    deleted_count = delete_torrent_files(common_files)
    
    # Define output file path
    output_file_path = r"G:\compare-list.txt"
    
    # Prepare output content
    output_lines = []
    
    if common_files:
        output_lines.append("Files that exist in both directories:")
        output_lines.append("-" * 50)
        for name, path1, path2 in common_files:
            output_lines.append(f"File: {name}")
            output_lines.append(f"  Path in directory 1: {path1}")
            output_lines.append(f"  Path in directory 2: {path2}")
            # Mark .torrent files that were deleted
            if Path(path1).suffix.lower() == '.torrent':
                output_lines.append("  Status: .torrent file deleted from directory 1")
            output_lines.append("")
        
        if deleted_count > 0:
            output_lines.append(f"Total .torrent files deleted: {deleted_count}")
    else:
        output_lines.append("No common files found between the two directories.")
    
    # Print results to console
    for line in output_lines:
        print(line)
    
    # Write results to file
    try:
        # Ensure the directory exists
        output_dir = Path(output_file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for line in output_lines:
                f.write(line + '\n')
        print(f"\nResults also written to: {output_file_path}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    main()