import os
import re
import shutil
import argparse
from pathlib import Path

def find_image_references(md_file_path):
    """
    Find all image references in a Markdown file
    Returns a list of image paths referenced in the file
    """
    image_paths = []
    
    # Common image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.tiff', '.tif'}
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match Markdown image syntax: ![alt text](path)
        md_image_pattern = r'!\[.*?\]\((.+?)\)'
        md_matches = re.findall(md_image_pattern, content)
        for match in md_matches:
            # Remove any URL parameters or anchors
            image_path = match.split('?')[0].split('#')[0]
            # Check if it has an image extension
            if Path(image_path).suffix.lower() in image_extensions:
                image_paths.append(image_path)
        
        # Pattern to match HTML img tags: <img src="path" ...>
        html_img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        html_matches = re.findall(html_img_pattern, content, re.IGNORECASE)
        for match in html_matches:
            # Remove any URL parameters or anchors
            image_path = match.split('?')[0].split('#')[0]
            # Check if it has an image extension
            if Path(image_path).suffix.lower() in image_extensions:
                image_paths.append(image_path)
                
    except Exception as e:
        print(f"Error reading Markdown file {md_file_path}: {e}")
    
    return image_paths

def resolve_image_paths(md_file_path, image_references):
    """
    Resolve relative image paths to absolute paths
    Returns a tuple of (existing_image_paths, missing_image_references)
    """
    md_dir = Path(md_file_path).parent
    existing_image_paths = []
    missing_image_references = []
    
    for img_ref in image_references:
        # Convert to Path object
        img_path = Path(img_ref)
        
        # If it's an absolute path, use as is
        if img_path.is_absolute():
            if img_path.exists():
                existing_image_paths.append(img_path)
            else:
                missing_image_references.append(img_ref)
        else:
            # It's a relative path, resolve relative to the Markdown file location
            resolved_path = (md_dir / img_path).resolve()
            if resolved_path.exists():
                existing_image_paths.append(resolved_path)
            else:
                missing_image_references.append(img_ref)
    
    return existing_image_paths, missing_image_references

def move_md_with_images(source_md_path, destination_dir):
    """
    Move a Markdown file and all its referenced images to a new location
    This function MOVES files (removes from original location) rather than copying them
    """
    # Check if source Markdown file exists
    if not os.path.exists(source_md_path):
        raise FileNotFoundError(f"Source Markdown file not found: {source_md_path}")
    
    # Check if destination directory exists, create if not
    dest_path = Path(destination_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Find image references in the Markdown file
    print("Finding image references in the Markdown file...")
    image_references = find_image_references(source_md_path)
    print(f"Found {len(image_references)} image references")
    
    # Resolve image paths to absolute paths
    print("Resolving image paths...")
    absolute_image_paths, missing_images = resolve_image_paths(source_md_path, image_references)
    print(f"Found {len(absolute_image_paths)} existing image files")
    
    # Output missing image references
    if missing_images:
        print("\nMissing image references (referenced in MD but files not found):")
        for img_ref in missing_images:
            print(f"  - {img_ref}")
    else:
        print("\nAll image references point to existing files.")
    
    # Move images to destination directory
    moved_images = []
    for img_path in absolute_image_paths:
        try:
            # Get the filename of the image
            img_filename = img_path.name
            dest_img_path = dest_path / img_filename
            
            # If file already exists, add a number to make it unique
            counter = 1
            original_dest_img_path = dest_img_path
            while dest_img_path.exists():
                name_without_ext = img_path.stem
                ext = img_path.suffix
                dest_img_path = dest_path / f"{name_without_ext}_{counter}{ext}"
                counter += 1
            
            # Move the image (remove from original location)
            shutil.move(str(img_path), str(dest_img_path))
            moved_images.append((img_path, dest_img_path))
            print(f"Moved image: {img_path} -> {dest_img_path}")
        except Exception as e:
            print(f"Error moving image {img_path}: {e}")
    
    # Move the Markdown file
    md_filename = Path(source_md_path).name
    dest_md_path = dest_path / md_filename
    
    # If file already exists, add a number to make it unique
    counter = 1
    original_dest_md_path = dest_md_path
    while dest_md_path.exists():
        name_without_ext = Path(source_md_path).stem
        ext = Path(source_md_path).suffix
        dest_md_path = dest_path / f"{name_without_ext}_{counter}{ext}"
        counter += 1
    
    try:
        shutil.move(source_md_path, dest_md_path)
        print(f"Moved Markdown file: {source_md_path} -> {dest_md_path}")
    except Exception as e:
        print(f"Error moving Markdown file: {e}")
        return False
    
    print(f"\nSummary:")
    print(f"  - Markdown file: 1")
    print(f"  - Existing images found and moved: {len(moved_images)}")
    print(f"  - Missing image references: {len(missing_images)}")
    print(f"Successfully moved Markdown file and images to {destination_dir}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Move a Markdown file and its referenced images to a new location")
    parser.add_argument("source_md", help="Path to the source Markdown file")
    parser.add_argument("destination_dir", help="Destination directory path")
    
    args = parser.parse_args()
    
    try:
        move_md_with_images(args.source_md, args.destination_dir)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()