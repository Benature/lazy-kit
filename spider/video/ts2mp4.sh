ffmpeg -f concat -safe 0 -i ffmpeg.txt -c copy all.ts
ffmpeg -i all.ts -acodec copy -vcodec copy all.mp4 