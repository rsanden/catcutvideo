# catcutvideo
Easily cut and concatenate videos from a text file using ffmpeg

# Example `videolist.txt`:
```
video01.mp4 x
video02.3gp 00:00-00:42
video03.mp4 0:22-1:10, 01:14-end
video04.mp4 all
```

# Usage:
```bash
# Create videolist.txt from videos in ./footage/
./makevideolist.bash > videolist.txt

# Edit videolist.txt and select segments, rearrange order as we desire. See example above for syntax
vim videolist.txt

# Generate script containing ffmpeg commands
./catcutvideo.py

# Run the script to generate output.mp4
./buildvideo.bash
```

# FFMPEG Version
This script is tested using ffmpeg version 2.8.11-0ubuntu0.16.04.1 from the Ubuntu 16.04 repo.
I intend to keep it compatible with the latest Ubuntu LTS release's ffmpeg going forward.
