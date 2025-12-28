#!/usr/bin/env python3
"""
Automated coin addition script for the Jekyll coin collection.

Usage:
    python tools/add_coin.py <notes_docx> <obverse_image> <reverse_image>

Example:
    python tools/add_coin.py \
        "/path/to/Dropbox/Coins/Collection/CoinName/Notes.docx" \
        "/path/to/Dropbox/Coins/Collection/CoinName/Photography/obverse.png" \
        "/path/to/Dropbox/Coins/Collection/CoinName/Photography/reverse.png"
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def extract_text_from_docx(docx_path):
    """Extract text from a Word document using textutil."""
    result = subprocess.run(
        ['textutil', '-convert', 'txt', '-stdout', docx_path],
        capture_output=True,
        text=True
    )
    return result.stdout


def parse_coin_metadata(text):
    """Parse coin metadata from the document text."""
    metadata = {}
    
    # Extract title (first line pattern: "Name – Location – Date")
    lines = text.strip().split('\n')
    if lines:
        first_line = lines[0].strip()
        metadata['title'] = first_line
        
        # Try to parse components from first line
        parts = [p.strip() for p in first_line.split('–')]
        if len(parts) >= 3:
            metadata['ruler'] = parts[0]
            metadata['mint'] = parts[1]
            metadata['date_minted'] = parts[2]
    
    # Extract reference (Crawford pattern)
    crawford_match = re.search(r'Crawford\s+(\d+/\d+[a-z]?)', text, re.IGNORECASE)
    if crawford_match:
        metadata['reference'] = f"Crawford {crawford_match.group(1)}"
    
    # Extract weight and grade from patterns like "gVF; 3.99g"
    weight_match = re.search(r'(\d+\.\d+)g', text)
    if weight_match:
        metadata['weight'] = f"{weight_match.group(1)}g"
    
    grade_match = re.search(r'\b([gv]?[VEF]{1,3})\b', text, re.IGNORECASE)
    if grade_match:
        metadata['grade'] = grade_match.group(1)
    
    # Extract period (Republican, Imperial, Greek)
    if re.search(r'\bRepublic(an)?\b', text, re.IGNORECASE):
        metadata['period'] = 'Republican'
    elif re.search(r'\bImperial\b', text, re.IGNORECASE):
        metadata['period'] = 'Imperial'
    elif re.search(r'\bGreek\b', text, re.IGNORECASE):
        metadata['period'] = 'Greek'
    
    # Extract obverse and reverse descriptions
    obverse_match = re.search(r'\*\*Obverse\*\*:\s*(.+?)(?=\n\n|\*\*Reverse\*\*:|$)', text, re.IGNORECASE | re.DOTALL)
    if obverse_match:
        metadata['obverse_description'] = obverse_match.group(1).strip()
    
    reverse_match = re.search(r'\*\*Reverse\*\*:\s*(.+?)(?=\n\n|Crawford|$)', text, re.IGNORECASE | re.DOTALL)
    if reverse_match:
        metadata['reverse_description'] = reverse_match.group(1).strip()
    
    return metadata


def extract_main_content(text):
    """Extract the main descriptive content from the document."""
    lines = text.strip().split('\n')
    
    # Skip first line (title) and find main content paragraphs
    content_lines = []
    skip_patterns = [
        r'^Figure\s+\d+:',
        r'^Notes$',
        r'^References$',
        r'^<<.*>>$',
        r'^\*\*Obverse\*\*:',
        r'^\*\*Reverse\*\*:',
        r'^Obverse:',
        r'^Reverse:',
        r'^Crawford',
        r'^[gv]?[VEF]{1,3};',
    ]
    
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Skip metadata and reference lines
        if any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
            continue
        
        # Collect content paragraphs
        if len(line) > 50:  # Likely a content paragraph
            content_lines.append(line)
    
    return '\n\n'.join(content_lines[:3])  # Take first 3 main paragraphs


def generate_filename(title):
    """Generate a filename from the coin title."""
    # Remove special characters, convert to lowercase, replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename


def main():
    parser = argparse.ArgumentParser(description='Add a new coin to the collection')
    parser.add_argument('notes_docx', help='Path to the Notes.docx file')
    parser.add_argument('obverse_image', help='Path to the obverse image')
    parser.add_argument('reverse_image', help='Path to the reverse image')
    parser.add_argument('--bg-color', default='black', choices=['black', 'white', 'gray'],
                       help='Background color for aligned image (default: black)')
    
    args = parser.parse_args()
    
    # Validate input files exist
    for path in [args.notes_docx, args.obverse_image, args.reverse_image]:
        if not os.path.exists(path):
            print(f"Error: File not found: {path}")
            sys.exit(1)
    
    # Extract and parse metadata
    print("📄 Extracting text from Word document...")
    text = extract_text_from_docx(args.notes_docx)
    
    print("🔍 Parsing metadata...")
    metadata = parse_coin_metadata(text)
    content = extract_main_content(text)
    
    # Generate filename
    filename = generate_filename(metadata.get('title', 'unknown'))
    
    # Setup paths
    project_root = Path(__file__).parent.parent
    coins_dir = project_root / '_coins'
    img_dir = project_root / 'assets' / 'img' / 'coins'
    
    # Create directories if needed
    coins_dir.mkdir(exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy images
    print("🖼️  Copying coin images...")
    obv_ext = Path(args.obverse_image).suffix
    rev_ext = Path(args.reverse_image).suffix
    
    obv_dest = img_dir / f"{filename}-obv{obv_ext}"
    rev_dest = img_dir / f"{filename}-rev{rev_ext}"
    aligned_dest = img_dir / f"{filename}-aligned.png"
    
    shutil.copy(args.obverse_image, obv_dest)
    shutil.copy(args.reverse_image, rev_dest)
    
    # Create aligned image
    print("⚙️  Creating aligned image...")
    align_script = project_root / 'tools' / 'align_coin_images.py'
    subprocess.run([
        'python', str(align_script),
        str(obv_dest), str(rev_dest), str(aligned_dest),
        '--bg-color', args.bg_color
    ], check=True)
    
    # Create markdown file
    print("📝 Creating coin entry...")
    md_path = coins_dir / f"{filename}.md"
    
    # Build frontmatter
    frontmatter = f"""---
layout: coin
title: "{metadata.get('title', 'Unknown Coin')}"
period: {metadata.get('period', 'Republican')}
ruler: {metadata.get('ruler', '')}
mint: {metadata.get('mint', 'Rome')}
denomination: Denarius
date_minted: "{metadata.get('date_minted', '')}"
reference: "{metadata.get('reference', '')}"
metal: Silver
weight: "{metadata.get('weight', '')}"
grade: "{metadata.get('grade', '')}"
image_obverse: coins/{obv_dest.name}
image_reverse: coins/{rev_dest.name}
image_aligned: coins/{aligned_dest.name}
obverse_description: "{metadata.get('obverse_description', '')}"
reverse_description: "{metadata.get('reverse_description', '')}"
featured: true
---

{content}
"""
    
    md_path.write_text(frontmatter)
    
    print(f"\n✅ Successfully added coin: {metadata.get('title')}")
    print(f"   Markdown file: {md_path}")
    print(f"   Images: {obv_dest.name}, {rev_dest.name}, {aligned_dest.name}")
    print(f"\n💡 Next steps:")
    print(f"   1. Review and edit {md_path}")
    print(f"   2. Add any additional content or formatting")
    print(f"   3. Commit and push changes to deploy")


if __name__ == '__main__':
    main()
