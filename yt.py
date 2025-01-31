from cc import SONG_DICT
import subprocess


def split_audio(input_file, timestamp_dict, output_format='mp3'):

    split_times = [(x, y) for x, y in timestamp_dict.items() ]
    duration = get_duration(input_file)
    
    split_times.append((duration, "end"))

    output_dir = 'songs'

    for i in range(len(split_times) - 1):

        song = split_times[i]
        
        song_start = time_to_ms(song[0])
        song_name = song[1]
        song_end = time_to_ms(split_times[i + 1][0]) - 1

        output_filename = f"{output_dir}/{song_name}.{output_format}"

        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(song_start),
            "-to", str(song_end),
            "-c", "copy",
            "-y",  # Overwrite output file if it exists
            output_filename
        ]
        

        print(f"Splitting segment {i+1}...")
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Exported: {output_filename}")


def get_duration(input_file):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return float(result.stdout)


def time_to_ms(time_str):
    h, m, s = map(float, time_str.split(':'))
    return h * 3600 + m * 60 + s

if __name__ == "__main__":
    split_audio("songs/main.mp3", SONG_DICT)