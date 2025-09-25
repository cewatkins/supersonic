#!/usr/bin/env python3
"""
Create playlists from all_real_songs.txt in various formats
"""
import os
import sys
import json
import xml.etree.ElementTree as ET
from urllib.parse import quote

def parse_real_songs_file(filepath):
    """Parse the all_real_songs.txt file and return list of song data"""
    songs = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(' ')
            if len(parts) < 4:
                print(f"Warning: Line {line_num} has insufficient parts: {line}")
                continue
            
            # First part is filename, last part is URL, everything in between is title + artist
            filename = parts[0]
            url = parts[-1]
            
            # Everything between filename and URL is title + artist
            # We need to split this intelligently
            middle_parts = parts[1:-1]
            middle_text = ' '.join(middle_parts)
            
            # Try to split on common separators or patterns
            # This is a heuristic - you might need to adjust based on your data
            if ' - ' in middle_text:
                title, artist = middle_text.split(' - ', 1)
            elif ' by ' in middle_text.lower():
                title, artist = middle_text.lower().split(' by ', 1)
                artist = artist.title()
            else:
                # If no clear separator, assume last word(s) are artist
                words = middle_text.split()
                if len(words) > 2:
                    title = ' '.join(words[:-1])
                    artist = words[-1]
                else:
                    title = middle_text
                    artist = "Unknown Artist"
            
            songs.append({
                'filename': filename,
                'title': title.strip(),
                'artist': artist.strip(),
                'url': url,
                'line_num': line_num
            })
    
    return songs

def create_m3u_playlist(songs, output_path):
    """Create M3U playlist format (compatible with VLC, etc.)"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for song in songs:
            # M3U format with metadata
            f.write(f"#EXTINF:-1,{song['artist']} - {song['title']}\n")
            f.write(f"{song['url']}\n")
    print(f"Created M3U playlist: {output_path}")

def create_xspf_playlist(songs, output_path):
    """Create XSPF playlist format (XML-based, rich metadata)"""
    playlist = ET.Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
    
    title_elem = ET.SubElement(playlist, "title")
    title_elem.text = "Real Songs Playlist"
    
    track_list = ET.SubElement(playlist, "trackList")
    
    for song in songs:
        track = ET.SubElement(track_list, "track")
        
        location = ET.SubElement(track, "location")
        location.text = song['url']
        
        title = ET.SubElement(track, "title")
        title.text = song['title']
        
        creator = ET.SubElement(track, "creator")
        creator.text = song['artist']
        
        # Add custom metadata
        meta_filename = ET.SubElement(track, "meta", rel="filename")
        meta_filename.text = song['filename']
    
    # Write XML with proper formatting
    ET.indent(playlist, space="  ", level=0)
    tree = ET.ElementTree(playlist)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Created XSPF playlist: {output_path}")

def create_json_playlist(songs, output_path):
    """Create JSON playlist (for custom applications)"""
    playlist_data = {
        "name": "Real Songs Playlist",
        "description": "Generated from all_real_songs.txt",
        "tracks": songs
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(playlist_data, f, indent=2, ensure_ascii=False)
    print(f"Created JSON playlist: {output_path}")

def create_youtube_links_html(songs, output_path):
    """Create HTML page with clickable YouTube links"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Real Songs Playlist</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .song {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .title {{ font-weight: bold; color: #333; }}
        .artist {{ color: #666; font-style: italic; }}
        .filename {{ font-size: 0.8em; color: #999; }}
        a {{ color: #1a73e8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Real Songs Playlist ({len(songs)} songs)</h1>
"""
    
    for i, song in enumerate(songs, 1):
        html_content += f"""
    <div class="song">
        <div class="title">{i}. <a href="{song['url']}" target="_blank">{song['title']}</a></div>
        <div class="artist">by {song['artist']}</div>
        <div class="filename">{song['filename']}</div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created HTML playlist: {output_path}")

def create_vlc_batch_script(songs, output_path):
    """Create a batch script to open all URLs in VLC"""
    if os.name == 'nt':  # Windows
        script_content = "@echo off\n"
        script_content += f'start "" "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe" '
    else:  # Linux/Mac
        script_content = "#!/bin/bash\n"
        script_content += "vlc "
    
    # Add all URLs
    for song in songs:
        script_content += f'"{song["url"]}" '
    
    script_content += "\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    if os.name != 'nt':
        os.chmod(output_path, 0o755)  # Make executable on Unix
    
    print(f"Created VLC batch script: {output_path}")

def main():
    input_file = 'dataset/all_real_songs.txt'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        print("Make sure you're in the supersonic directory and the file exists.")
        sys.exit(1)
    
    print(f"Parsing {input_file}...")
    songs = parse_real_songs_file(input_file)
    print(f"Found {len(songs)} songs")
    
    # Create output directory
    output_dir = 'playlists'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate different playlist formats
    create_m3u_playlist(songs, f'{output_dir}/real_songs.m3u')
    create_xspf_playlist(songs, f'{output_dir}/real_songs.xspf')
    create_json_playlist(songs, f'{output_dir}/real_songs.json')
    create_youtube_links_html(songs, f'{output_dir}/real_songs.html')
    create_vlc_batch_script(songs, f'{output_dir}/play_all_vlc.sh')
    
    print(f"\n✅ All playlists created in '{output_dir}/' directory!")
    print("\n📋 Usage options:")
    print("  • Open real_songs.m3u in VLC, foobar2000, or similar")
    print("  • Open real_songs.xspf in VLC or other XSPF-compatible players") 
    print("  • Open real_songs.html in your web browser for clickable links")
    print("  • Use real_songs.json for custom applications")
    print("  • Run play_all_vlc.sh to open everything in VLC at once")

if __name__ == "__main__":
    main()