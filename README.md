# ActivityNet-Video-Downloader

A modified version of [ActivityNet-Video-Downloader](https://github.com/ozgyal/ActivityNet-Video-Downloader)

## Major differences
- Python 3.X support
- Trim videos into labeled segments
- Download videos in '.mp4' format

## Using activityNetDownloader

1. Install the prerequisites.
    ```bash
    pip install -r requirements.txt
    ```
    
2. Download the ActivityNet annotation file
   ```bash
   wget http://ec2-52-11-11-89.us-west-2.compute.amazonaws.com/files/activity_net.v1-3.min.json
   ```
   - if this url doesn't work, please visit [the official ActivityNet website](http://activity-net.org/index.html)
   
3. Run the script.
	``` bash
	python activityNetDownloader.py
	```

  - if you use a different json file (not `activity_net.v1-3.min.json`), please specify its filename as an argument
    ```bash
    python activityNetDownloader.py ./another.file.name.json
    ```

4. All the videos will be downloaded into two directories
   - `downloaded`: Full-length original videos
   - `trimmed`: Trimmed videos (train & validation only) 
