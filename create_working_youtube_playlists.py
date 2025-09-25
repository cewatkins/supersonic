#!/usr/bin/env python3
"""
Create playlists with yt-dlp integration for YouTube playback
"""
import os
import sys
import csv
from collections import defaultdict

def create_ytdlp_playlist(songs, output_path, title="Playlist"):
    """Create playlist that works with yt-dlp + mpv"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        f.write(f"#PLAYLIST:{title}\n")
        
        for song in songs:
            if song.get('url'):
                f.write(f"#EXTINF:-1,{song['artist']} - {song['title']}\n")
                f.write(f"{song['url']}\n")

def create_mpv_script(songs, output_path, title="Playlist"):
    """Create a script that uses mpv with yt-dlp to play YouTube URLs"""
    script_content = f"""#!/bin/bash
# {title}
# Usage: ./script.sh [song_number] or ./script.sh to play all

if [ "$1" ]; then
    # Play specific song number
    SONG_NUM=$1
    echo "Playing song #$SONG_NUM..."
else
    # Play all songs
    echo "Playing all {len(songs)} songs..."
    SONG_NUM=1
fi

SONGS=(
"""
    
    for i, song in enumerate(songs, 1):
        if song.get('url'):
            script_content += f'    "{song["url"]}"  # {i}. {song["artist"]} - {song["title"]}\n'
    
    script_content += f""")

if [ "$1" ]; then
    if [ $SONG_NUM -le {len(songs)} ] && [ $SONG_NUM -ge 1 ]; then
        echo "Playing: ${{SONGS[$SONG_NUM-1]}}"
        mpv --ytdl-format=best "${{SONGS[$SONG_NUM-1]}}"
    else
        echo "Invalid song number. Choose 1-{len(songs)}"
    fi
else
    # Play all songs
    for url in "${{SONGS[@]}}"; do
        echo "Playing: $url"
        mpv --ytdl-format=best "$url"
    done
fi
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(output_path, 0o755)  # Make executable

def create_web_player(songs, output_path, title="Playlist"):
    """Create HTML page with embedded YouTube players"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; text-align: center; }}
        .player-container {{ background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .song-info {{ margin: 10px 0; }}
        .song-title {{ font-size: 1.2em; font-weight: bold; color: #333; }}
        .song-artist {{ color: #666; font-style: italic; }}
        .youtube-player {{ width: 100%; height: 315px; border: none; border-radius: 5px; }}
        .controls {{ margin: 10px 0; }}
        button {{ background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 5px; }}
        button:hover {{ background: #1557b0; }}
        .playlist-nav {{ position: fixed; top: 20px; right: 20px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); max-height: 400px; overflow-y: auto; width: 300px; }}
        .nav-item {{ padding: 5px; cursor: pointer; border-bottom: 1px solid #eee; }}
        .nav-item:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title} ({len(songs)} songs)</h1>
        
        <div class="playlist-nav">
            <h3>Playlist Navigation</h3>
"""
    
    for i, song in enumerate(songs):
        if song.get('url'):
            video_id = song['url'].split('v=')[-1].split('&')[0]
            html_content += f'            <div class="nav-item" onclick="scrollToSong({i})">{i+1}. {song["artist"]} - {song["title"]}</div>\n'
    
    html_content += """        </div>
"""
    
    for i, song in enumerate(songs):
        if song.get('url'):
            video_id = song['url'].split('v=')[-1].split('&')[0]
            html_content += f"""
        <div class="player-container" id="song-{i}">
            <div class="song-info">
                <div class="song-title">{i+1}. {song['title']}</div>
                <div class="song-artist">by {song['artist']}</div>
            </div>
            <iframe class="youtube-player" 
                    src="https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1" 
                    allowfullscreen>
            </iframe>
            <div class="controls">
                <button onclick="window.open('{song['url']}', '_blank')">Open in YouTube</button>
                <button onclick="copyToClipboard('{song['url']}')">Copy URL</button>
            </div>
        </div>
"""
    
    html_content += """
    </div>
    
    <script>
        function scrollToSong(index) {
            document.getElementById('song-' + index).scrollIntoView({behavior: 'smooth'});
        }
        
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('URL copied to clipboard!');
            });
        }
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    # Read from the existing playlists or create a simple test
    songs = [
        {
            'title': 'Test Song',
            'artist': 'Test Artist', 
            'url': 'https://www.youtube.com/watch?v=UZtMKpvksvE'
        }
    ]
    
    os.makedirs('playlists/working_solutions', exist_ok=True)
    
    print("Creating working YouTube playlist solutions...")
    
    # Create mpv script (requires yt-dlp)
    create_mpv_script(songs, 'playlists/working_solutions/play_with_mpv.sh', 'YouTube Playlist (mpv + yt-dlp)')
    print("✅ Created mpv script: playlists/working_solutions/play_with_mpv.sh")
    
    # Create web player
    create_web_player(songs, 'playlists/working_solutions/web_player.html', 'YouTube Web Player')
    print("✅ Created web player: playlists/working_solutions/web_player.html")
    
    # Create instructions
    with open('playlists/working_solutions/README.md', 'w') as f:
        f.write("""# YouTube Playlist Solutions

## The Problem
Direct YouTube URLs don't work with mpv/VLC due to anti-bot protections (HTTP 403 errors).

## Working Solutions

### 1. mpv + yt-dlp (Recommended for terminal)
```bash
# Install yt-dlp first
pip install yt-dlp

# Then run the script
./play_with_mpv.sh        # Play all songs
./play_with_mpv.sh 5      # Play song #5
```

### 2. Web Player (Recommended for GUI)
Open `web_player.html` in your browser. Features:
- Embedded YouTube players
- Playlist navigation
- Copy URLs to clipboard
- Direct YouTube links

### 3. VLC with yt-dlp
```bash
# Install yt-dlp
pip install yt-dlp

# Play single video
vlc "$(yt-dlp -g 'https://www.youtube.com/watch?v=VIDEO_ID')"
```

### 4. Browser-based (Simplest)
Just open the HTML playlists in your browser and click the YouTube links.

## Why Direct URLs Don't Work
YouTube uses:
- Dynamic URLs that expire
- Bot detection
- Geographic restrictions
- Rate limiting

Use yt-dlp to extract the actual stream URLs dynamically.
""")
    
    print("✅ Created instructions: playlists/working_solutions/README.md")
    print("\n🎵 Solutions created! Check playlists/working_solutions/")

if __name__ == "__main__":
    main()