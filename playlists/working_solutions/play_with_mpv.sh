#!/bin/bash
# YouTube Playlist (mpv + yt-dlp)
# Usage: ./script.sh [song_number] or ./script.sh to play all

if [ "$1" ]; then
    # Play specific song number
    SONG_NUM=$1
    echo "Playing song #$SONG_NUM..."
else
    # Play all songs
    echo "Playing all 1 songs..."
    SONG_NUM=1
fi

SONGS=(
    "https://www.youtube.com/watch?v=UZtMKpvksvE"  # 1. Test Artist - Test Song
)

if [ "$1" ]; then
    if [ $SONG_NUM -le 1 ] && [ $SONG_NUM -ge 1 ]; then
        echo "Playing: ${SONGS[$SONG_NUM-1]}"
        mpv --ytdl-format=best "${SONGS[$SONG_NUM-1]}"
    else
        echo "Invalid song number. Choose 1-1"
    fi
else
    # Play all songs
    for url in "${SONGS[@]}"; do
        echo "Playing: $url"
        mpv --ytdl-format=best "$url"
    done
fi
