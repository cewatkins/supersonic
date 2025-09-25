# YouTube Playlist Solutions

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
