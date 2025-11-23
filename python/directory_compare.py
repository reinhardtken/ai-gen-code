import os
import argparse

def compare_directories(dir_a, dir_b):
    """
    Compare two directories and find files that exist in dir_a but not in dir_b
    
    Args:
        dir_a (str): Path to directory A
        dir_b (str): Path to directory B
        
    Returns:
        list: Files that exist in dir_a but not in dir_b
    """
    # Get all files in directory A
    files_a = set()
    for root, dirs, files in os.walk(dir_a):
        for file in files:
            # Get relative path from dir_a
            rel_path = os.path.relpath(os.path.join(root, file), dir_a)
            files_a.add(rel_path)
    
    # Get all files in directory B
    files_b = set()
    for root, dirs, files in os.walk(dir_b):
        for file in files:
            # Get relative path from dir_b
            rel_path = os.path.relpath(os.path.join(root, file), dir_b)
            files_b.add(rel_path)
    
    # Find files that exist in A but not in B
    diff_files = files_a - files_b
    
    return sorted(list(diff_files))

def main():
    parser = argparse.ArgumentParser(description='Compare two directories and find files that exist in directory A but not in directory B')
    parser.add_argument('dir_a', help='Path to directory A')
    parser.add_argument('dir_b', help='Path to directory B')
    
    args = parser.parse_args()
    
    # Check if directories exist
    if not os.path.exists(args.dir_a):
        print(f"Error: Directory A '{args.dir_a}' does not exist.")
        return
    
    if not os.path.exists(args.dir_b):
        print(f"Error: Directory B '{args.dir_b}' does not exist.")
        return
    
    # Compare directories
    diff_files = compare_directories(args.dir_a, args.dir_b)
    
    # Output results
    if diff_files:
        print(f"Files that exist in '{args.dir_a}' but not in '{args.dir_b}':")
        for file in diff_files:
            print(file)
    else:
        print(f"No files found in '{args.dir_a}' that don't exist in '{args.dir_b}'.")

if __name__ == "__main__":
    main()