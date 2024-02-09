from moviepy.editor import VideoFileClip, CompositeVideoClip


def watermark(uid):
    clip = VideoFileClip(f'output{uid}.mp4')
    watermark = (VideoFileClip(r"g.gif", has_mask=True)
                         .loop()  # loop gif
                         .set_duration(clip.duration)  # Продолжительность водяного знака
                         .resize(height=275)  # Высота водяного знака будет пропорционально масштабирована.
                         .margin(left=500, top=600, opacity=0)  # Поля водяных знаков и прозрачность
                         .set_pos(("left", "top")))  # Расположение водяного знака

    watermark_video = CompositeVideoClip([clip, watermark])
    watermark_video.write_videofile(f'output{uid}_f.mp4')
