import os
import time
import os
import time

def delete():
    try:
        print("Deleting Files...")
        os.remove("trimmed_video.mp4")
        os.remove("audio.mp3")
        time.sleep(60)
        os.remove("upload.mp4")
        print("Files were successfully deleted")
    except Exception as e:
        print(f"An error occurred while deleting files: {e}")