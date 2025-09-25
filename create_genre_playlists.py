#!/usr/bin/env python3
"""
Create genre-based playlists from the SONICS dataset
"""
import os
import sys
import csv
import json
from collections import defaultdict
from urllib.parse import quote

def read_real_songs(csv_path):
    """Read real_songs.csv and return songs grouped by multiple categories"""
    songs_by_category = {
        'artist': defaultdict(list),
        'year': defaultdict(list),
        'decade': defaultdict(list),
        'label': defaultdict(list)
    }
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Skip entries without youtube_id (unplayable)
            if not row.get('youtube_id'):
                continue
                
            youtube_url = f"https://www.youtube.com/watch?v={row['youtube_id']}"
            
            song_data = {
                'filename': row['filename'],
                'title': row['title'],
                'artist': row['artist'],
                'year': row.get('year', ''),
                'duration': row.get('duration', ''),
                'label': row.get('label', ''),
                'url': youtube_url,
                'type': 'real'
            }
            
            # Group by artist
            songs_by_category['artist'][row['artist']].append(song_data)
            
            # Group by year
            year = row.get('year', '').strip()
            if year and year.isdigit():
                songs_by_category['year'][year].append(song_data)
                
                # Group by decade
                decade = f"{year[:3]}0s"
                songs_by_category['decade'][decade].append(song_data)
            
            # Group by label
            label = row.get('label', '').strip()
            if label and label.lower() not in ['', 'unknown', 'none', 'null']:
                songs_by_category['label'][label].append(song_data)
    
    return songs_by_category

def read_fake_songs(csv_path):
    """Read fake_songs.csv and return songs grouped by genre, mood, topic, style"""
    songs_by_category = {
        'genre': defaultdict(list),
        'mood': defaultdict(list), 
        'topic': defaultdict(list),
        'style': defaultdict(list),
        'algorithm': defaultdict(list)
    }
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            song_data = {
                'id': row['id'],
                'filename': row['filename'],
                'algorithm': row['algorithm'],
                'style': row['style'],
                'genre': row['genre'],
                'mood': row['mood'],
                'topic': row['topic'],
                'duration': row.get('duration', ''),
                'type': 'fake',
                'url': None  # Fake songs don't have YouTube URLs
            }
            
            # Add to each category
            for category in ['genre', 'mood', 'topic', 'style', 'algorithm']:
                value = row[category].strip()
                if value and value.lower() not in ['', 'unknown', 'none', 'null']:
                    songs_by_category[category][value].append(song_data)
    
    return songs_by_category

def create_m3u_playlist(songs, output_path, title="Playlist"):
    """Create M3U playlist format"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n") 
        f.write(f"#PLAYLIST:{title}\n")
        
        for song in songs:
            if song['type'] == 'real' and song['url']:
                # Real songs with YouTube URLs
                f.write(f"#EXTINF:-1,{song['artist']} - {song['title']}\n")
                f.write(f"{song['url']}\n")
            elif song['type'] == 'fake':
                # Fake songs - just reference info (no playable URL)
                f.write(f"#EXTINF:-1,{song['algorithm']} - {song['filename']} ({song['genre']})\n")
                f.write(f"# Fake song: {song['filename']}\n")

def create_html_playlist(songs, output_path, title="Playlist"):
    """Create HTML playlist"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
        h1 {{ color: #333; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
        .stats {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .song {{ margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; }}
        .real-song {{ border-left: 4px solid #4caf50; }}
        .fake-song {{ border-left: 4px solid #ff9800; }}
        .title {{ font-weight: bold; color: #333; font-size: 1.1em; }}
        .artist {{ color: #666; font-style: italic; margin: 5px 0; }}
        .metadata {{ font-size: 0.9em; color: #888; }}
        .filename {{ font-size: 0.8em; color: #999; font-family: monospace; }}
        a {{ color: #1a73e8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .tag {{ display: inline-block; background: #e1f5fe; color: #0277bd; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin: 2px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="stats">
            <strong>Total songs:</strong> {len(songs)} | 
            <strong>Real songs:</strong> {len([s for s in songs if s['type'] == 'real'])} | 
            <strong>Fake songs:</strong> {len([s for s in songs if s['type'] == 'fake'])}
        </div>
"""
    
    for i, song in enumerate(songs, 1):
        song_class = "real-song" if song['type'] == 'real' else "fake-song"
        
        if song['type'] == 'real':
            html_content += f"""
        <div class="song {song_class}">
            <div class="title">{i}. <a href="{song['url']}" target="_blank">{song['title']}</a></div>
            <div class="artist">by {song['artist']}</div>
            <div class="metadata">
                <span class="tag">Real Song</span>
                {f'<span class="tag">Year: {song["year"]}</span>' if song['year'] else ''}
                {f'<span class="tag">Duration: {song["duration"]}s</span>' if song['duration'] else ''}
            </div>
            <div class="filename">{song['filename']}</div>
        </div>
"""
        else:  # fake song
            html_content += f"""
        <div class="song {song_class}">
            <div class="title">{i}. {song['filename']}</div>
            <div class="artist">Generated by {song['algorithm']}</div>
            <div class="metadata">
                <span class="tag">Fake Song</span>
                <span class="tag">Genre: {song['genre']}</span>
                <span class="tag">Mood: {song['mood']}</span>
                <span class="tag">Topic: {song['topic']}</span>
                <span class="tag">Style: {song['style']}</span>
            </div>
            <div class="filename">{song['filename']}</div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def safe_filename(name):
    """Convert a string to a safe filename"""
    return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()

def main():
    real_songs_path = 'dataset/real_songs.csv'
    fake_songs_path = 'dataset/fake_songs.csv'
    
    if not os.path.exists(real_songs_path):
        print(f"Error: {real_songs_path} not found!")
        sys.exit(1)
    
    if not os.path.exists(fake_songs_path):
        print(f"Error: {fake_songs_path} not found!")
        sys.exit(1)
    
    print("Reading real songs...")
    real_songs_by_category = read_real_songs(real_songs_path)
    
    print("Reading fake songs...")
    fake_songs_by_category = read_fake_songs(fake_songs_path)
    
    # Create output directories
    os.makedirs('playlists/by_genre', exist_ok=True)
    os.makedirs('playlists/by_mood', exist_ok=True)
    os.makedirs('playlists/by_topic', exist_ok=True)
    os.makedirs('playlists/by_style', exist_ok=True)
    os.makedirs('playlists/by_algorithm', exist_ok=True)
    os.makedirs('playlists/by_artist', exist_ok=True)
    os.makedirs('playlists/by_year', exist_ok=True)
    os.makedirs('playlists/by_decade', exist_ok=True)
    os.makedirs('playlists/by_label', exist_ok=True)
    
    # Create genre-based playlists (fake songs)
    print(f"\nCreating genre-based playlists...")
    for genre, songs in fake_songs_by_category['genre'].items():
        if len(songs) >= 5:  # Only create playlist if there are enough songs
            safe_genre = safe_filename(genre)
            
            # M3U format
            m3u_path = f'playlists/by_genre/{safe_genre}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Genre: {genre}")
            
            # HTML format
            html_path = f'playlists/by_genre/{safe_genre}.html'
            create_html_playlist(songs, html_path, f"Genre: {genre} ({len(songs)} songs)")
            
            print(f"  Created playlist for genre '{genre}' ({len(songs)} songs)")
    
    # Create mood-based playlists (fake songs)
    print(f"\nCreating mood-based playlists...")
    for mood, songs in fake_songs_by_category['mood'].items():
        if len(songs) >= 5:
            safe_mood = safe_filename(mood)
            
            m3u_path = f'playlists/by_mood/{safe_mood}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Mood: {mood}")
            
            html_path = f'playlists/by_mood/{safe_mood}.html'
            create_html_playlist(songs, html_path, f"Mood: {mood} ({len(songs)} songs)")
            
            print(f"  Created playlist for mood '{mood}' ({len(songs)} songs)")
    
    # Create artist-based playlists (real songs - PLAYABLE with YouTube URLs)
    print(f"\nCreating artist-based playlists...")
    for artist, songs in real_songs_by_category['artist'].items():
        if len(songs) >= 3:  # Only create if artist has multiple songs
            safe_artist = safe_filename(artist)
            
            m3u_path = f'playlists/by_artist/{safe_artist}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Artist: {artist}")
            
            html_path = f'playlists/by_artist/{safe_artist}.html'
            create_html_playlist(songs, html_path, f"Artist: {artist} ({len(songs)} songs)")
            
            print(f"  Created playlist for artist '{artist}' ({len(songs)} songs)")
    
    # Create year-based playlists (real songs - PLAYABLE with YouTube URLs)
    print(f"\nCreating year-based playlists...")
    for year, songs in real_songs_by_category['year'].items():
        if len(songs) >= 5:  # Only create if year has enough songs
            safe_year = safe_filename(year)
            
            m3u_path = f'playlists/by_year/{safe_year}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Year: {year}")
            
            html_path = f'playlists/by_year/{safe_year}.html'
            create_html_playlist(songs, html_path, f"Music from {year} ({len(songs)} songs)")
            
            print(f"  Created playlist for year '{year}' ({len(songs)} songs)")
    
    # Create decade-based playlists (real songs - PLAYABLE with YouTube URLs)
    print(f"\nCreating decade-based playlists...")
    for decade, songs in real_songs_by_category['decade'].items():
        if len(songs) >= 10:  # Only create if decade has enough songs
            safe_decade = safe_filename(decade)
            
            m3u_path = f'playlists/by_decade/{safe_decade}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Decade: {decade}")
            
            html_path = f'playlists/by_decade/{safe_decade}.html'
            create_html_playlist(songs, html_path, f"Music from the {decade} ({len(songs)} songs)")
            
            print(f"  Created playlist for decade '{decade}' ({len(songs)} songs)")
    
    # Create algorithm-based playlists (fake songs)
    print(f"\nCreating algorithm-based playlists...")
    for algorithm, songs in fake_songs_by_category['algorithm'].items():
        if len(songs) >= 10:  # Algorithms usually have many songs
            safe_algo = safe_filename(algorithm)
            
            m3u_path = f'playlists/by_algorithm/{safe_algo}.m3u'
            create_m3u_playlist(songs, m3u_path, f"Algorithm: {algorithm}")
            
            html_path = f'playlists/by_algorithm/{safe_algo}.html'
            create_html_playlist(songs, html_path, f"Algorithm: {algorithm} ({len(songs)} songs)")
            
            print(f"  Created playlist for algorithm '{algorithm}' ({len(songs)} songs)")
    
    print(f"\n✅ Category-based playlists created!")
    print(f"📁 Check the following directories:")
    print(f"  • playlists/by_genre/ - Fake songs by genre")
    print(f"  • playlists/by_mood/ - Fake songs by mood") 
    print(f"  • playlists/by_artist/ - Real songs by artist (PLAYABLE)")
    print(f"  • playlists/by_year/ - Real songs by year (PLAYABLE)")
    print(f"  • playlists/by_decade/ - Real songs by decade (PLAYABLE)")
    print(f"  • playlists/by_algorithm/ - Fake songs by AI algorithm")
    print(f"\n🎵 All real songs have YouTube URLs and are playable in VLC/browsers!")

if __name__ == "__main__":
    main()