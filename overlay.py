import subprocess
import random

def overlay():
    # Get the duration of your audio (replace 'audio.mp3' with your audio file)
    audio_duration = float(subprocess.check_output([
        'ffprobe', '-i', 'audio.mp3', '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'
    ]))

    # Define the path to your input video
    input_video_path = 'subway.mp4'
    totalVideoDuration = float(subprocess.check_output([
        'ffprobe', '-i', 'subway.mp4', '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'
    ])) 

    # Calculate a random start time within the valid range
    valid_range = totalVideoDuration - audio_duration  # 1800 seconds is 30 minutes
    start_time = random.uniform(0, valid_range)

    # Define the path for the output video with the random interval
    random_interval_output_path = 'trimmed_video.mp4'

    # Run FFmpeg command to select a random interval and save it as 'random_interval_video.mp4'
    ffmpeg_command_random_interval = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', input_video_path,
        '-t', str(audio_duration),
        '-c:v', 'copy',
        '-c:a', 'copy',
        random_interval_output_path
    ]

    subprocess.run(ffmpeg_command_random_interval)

    # Overlay the trimmed video with the audio
    # Define the path for the final output video
    final_output_path = 'upload.mp4'

    # Run FFmpeg command to overlay the trimmed video with the audio and save it as 'final_output_video.mp4'
    ffmpeg_command_overlay_audio = [
        'ffmpeg',
        '-i', random_interval_output_path,
        '-i', 'audio.mp3',
        '-map', '0:v',
        '-map', '1:a',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        final_output_path
    ]

    subprocess.run(ffmpeg_command_overlay_audio)

    print(f"Final output saved as {final_output_path}")