import os
import random
import subprocess

# Set the FFmpeg binary path BEFORE importing moviepy.editor
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"  # Replace with your actual path
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_music(video_path):
    """
    Adds background music to a video.
    """
    music_dir = "/Users/truman/AIGC/musicResource/clip5s"
    output_dir = "/Users/truman/AIGC/Publication"

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get music files
    music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]
    if not music_files:
        print("Error: No MP3 music files found.")
        return

    # Choose random music
    random_music_file = random.choice(music_files)
    music_path = os.path.join(music_dir, random_music_file)

    try:
        print(f"Using FFmpeg path: {ffmpeg_path}")  # Log the FFmpeg path
        print(f"Loading video: {video_path}")
        video_clip = VideoFileClip(video_path)
        print("Video loaded successfully.")

        print(f"Loading audio: {music_path}")
        audio_clip = AudioFileClip(music_path)
        print("Audio loaded successfully.")


        # Ensure audio and video duration match
        if video_clip.duration > 5:
            video_clip = video_clip.subclip(0, 5)
        elif video_clip.duration < 5:
            n_repeats = int(5 / video_clip.duration)
            video_clip = video_clip.loop(n_repeats)

        # Combine audio and video
        final_audio = CompositeAudioClip([audio_clip])
        video_clip = video_clip.set_audio(final_audio)

        # Build output path
        video_filename = os.path.basename(video_path)
        output_path = os.path.join(output_dir, video_filename)

        # Export video
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print("Successfully added background music.")

    except Exception as e:
        print(f"Error adding background music: {e}")
        if "'VideoFileClip' object has no attribute 'subclip'" in str(e):
          print("Likely cause: MoviePy could not properly decode the video. Check FFmpeg and video file.")
        print(f"Exception Type: {type(e)}")
        print(f"Exception Arguments: {e.args}")
        # Check the video file to ensure that moviepy is able to read it.
        try:
          command = [ffmpeg_path, '-i', video_path]
          result = subprocess.run(command, check = False, capture_output = True, text = True)
          print("FFMPEG Diagnostic command output")
          print(result.stderr)
        except Exception as ffmpeg_check_err:
          print("Could not run FFmpeg diagnostic command")
          print(ffmpeg_check_err)