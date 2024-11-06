from moviepy import editor
from pydub import AudioSegment


def rendering(mp4_path: str, clips: list[tuple[float, float]], output_path: str):
    video_clips = []
    # audio = AudioSegment.from_file(mp4_path, "mp4")
    # a = audio.raw_data

    with editor.VideoFileClip(mp4_path, audio=False) as video:  # 讀取影片
        for start_time, end_time in clips:
            video_clip = video.subclip(start_time, end_time)  # 剪取片段
            video_clips.append(video_clip)

        clip_string = editor.concatenate_videoclips(video_clips)  # 串接片段
        clip_string.write_videofile(
            filename=output_path,
            codec="libx264",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            audio_codec="aac",
            preset="veryslow",
        )
