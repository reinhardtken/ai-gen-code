import os
import struct
import argparse

def detect_audio_format(file_path):
    """
    Detect audio file format by examining file headers (magic numbers)
    Returns the detected format or None if not recognized as audio
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            # Read first 128 bytes which should be enough for most audio file headers
            header = f.read(128)
            
        # Check for different audio formats
        if is_wav(header):
            return "WAV"
        elif is_mp3(header):
            return "MP3"
        elif is_flac(header):
            return "FLAC"
        elif is_ogg(header):
            return "OGG"
        elif is_aiff(header):
            return "AIFF"
        elif is_aac(header):
            return "AAC"
        elif is_m4a(header):
            return "M4A"
        elif is_wma(header):
            return "WMA"
        else:
            return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def is_wav(header):
    """Check if file is WAV format"""
    # WAV files start with "RIFF" and have "WAVE" later in header
    return header.startswith(b'RIFF') and b'WAVE' in header[:16]

def is_mp3(header):
    """Check if file is MP3 format"""
    # MP3 files often start with ID3 tag or frame sync
    # ID3 tag starts with "ID3"
    if header.startswith(b'ID3'):
        return True
    
    # Check for MP3 frame sync (11 bits set to 1)
    # This is more complex but let's check common patterns
    if len(header) >= 3:
        # Check for common MP3 sync patterns
        sync_patterns = [b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2', b'\xFF\xE3']
        for pattern in sync_patterns:
            if header.startswith(pattern):
                return True
                
        # Check for sync pattern anywhere in the first few bytes
        for i in range(min(len(header) - 1, 32)):
            if header[i] == 0xFF and (header[i+1] & 0xE0) == 0xE0:
                return True
    
    return False

def is_flac(header):
    """Check if file is FLAC format"""
    # FLAC files start with "fLaC"
    return header.startswith(b'fLaC')

def is_ogg(header):
    """Check if file is OGG format"""
    # OGG files start with "OggS"
    return header.startswith(b'OggS')

def is_aiff(header):
    """Check if file is AIFF format"""
    # AIFF files start with "FORM" and have "AIFF" later in header
    return header.startswith(b'FORM') and b'AIFF' in header[:16]

def is_aac(header):
    """Check if file is AAC format"""
    # AAC files can have ADIF or ADTS headers
    # ADIF starts with "ADIF"
    if header.startswith(b'ADIF'):
        return True
    
    # ADTS has a specific sync pattern
    if len(header) >= 2:
        # ADTS sync pattern: 12 bits set to 1, followed by specific bits
        if header[0] == 0xFF and (header[1] & 0xF6) == 0xF0:
            return True
    
    return False

def is_m4a(header):
    """Check if file is M4A format"""
    # M4A files are based on MP4 format and start with specific box structures
    # Look for "ftyp" box which indicates MP4/M4A family
    if b'ftyp' in header[:64]:
        # Check for M4A-specific compatible brands
        m4a_brands = [b'M4A ', b'M4B ', b'M4P ', b'M4V ', b'M4R ']
        for brand in m4a_brands:
            if brand in header[:128]:
                return True
        # Generic MP4 is also possible for M4A
        if b'mp42' in header[:128] or b'isom' in header[:128]:
            return True
    return False

def is_wma(header):
    """Check if file is WMA format"""
    # WMA files have a specific GUID header
    # ASF (Windows Media Audio) files start with a specific GUID
    wma_guid = b'\x30\x26\xB2\x75\x8E\x66\xCF\x11\xA6\xD9\x00\xAA\x00\x62\xCE\x6C'
    return header.startswith(wma_guid)

def main():
    """Main function to test audio file detection"""
    parser = argparse.ArgumentParser(description="Detect audio file format by examining file headers")
    parser.add_argument("file_path", help="Path to the file to check")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"Error: File '{args.file_path}' does not exist.")
        return
    
    format_type = detect_audio_format(args.file_path)
    
    if format_type:
        print(f"The file '{args.file_path}' is detected as: {format_type}")
    else:
        print(f"The file '{args.file_path}' is not recognized as a known audio format.")

if __name__ == "__main__":
    main()