import csv

# Path to the CSV file
csv_file_path = 'dataset/real_songs.csv'

# Path to the output .txt file
output_txt_path = 'dataset/all_real_songs.txt'

# Process each row in the CSV and write to the .txt file
with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile, \
     open(output_txt_path, 'w', encoding='utf-8') as txtfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract required fields
        filename = row['filename']
        title = row['title']
        artist = row['artist']
        youtube_id = row['youtube_id']
        
        # Create the YouTube URL
        youtube_url = f"https://www.youtube.com/watch?v={youtube_id}"
        
        # Write the data to the .txt file as a single line separated by spaces
        txtfile.write(f"{filename} {title} {artist} {youtube_url}\n")

print(f"Processing complete. All data written to {output_txt_path}.")