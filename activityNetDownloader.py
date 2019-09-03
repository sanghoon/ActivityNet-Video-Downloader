import os
import json
import subprocess

import pafy
import autoarg


def download_vids(json_path='activity_net.v1-3.min.json', download_base='./downloaded/', trimmed_base='./trimmed/'):
    n_downloaded = 0
    n_trimmed = 0

    # open json file
    with open(json_path) as data_file:
        data = json.load(data_file)

    # take only video informations from database object
    videos = data['database']
    n_videos = len(videos)

    # iterate through dictionary of videos
    for i, (key, video) in enumerate(videos.items()):
        print_header = '[{:06d}/{:06d}] '.format(i, n_videos)

        # find video subset (training, testing, validation)
        subset = video['subset']

        # find video label
        annotations = video['annotations']
        dft_label = ''
        if len(annotations) != 0:
            dft_label = annotations[0]['label'].replace(' ', '_')
        else:
            print(print_header + 'Skip. (no annotations)')
            continue

        # create folder named as <label> if does not exist
        download_dir = os.path.join(download_base, subset, dft_label)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # take url of video
        url = video['url']

        # start to download
        try:
            video = pafy.new(url)
            best = video.getbest(preftype="mp4")
            filename = best.download(filepath=os.path.join(download_dir, '{}.mp4'.format(key)))
            print(print_header + 'Success! {} => {}'.format(url, filename))
            n_downloaded += 1
        except Exception as e:
            print(print_header + 'Failed! {} : '.format(url, e))
            continue

        # Extract labeled segments
        for ann_id, ann in enumerate(annotations):
            t_start = ann['segment'][0]
            t_duration = ann['segment'][1] - ann['segment'][0]

            out_filename = os.path.join(trimmed_base,
                                        subset,
                                        ann['label'].replace(' ', '_'),
                                        '{}_{}.mp4'.format(key, ann_id))

            if not os.path.exists(os.path.dirname(out_filename)):
                os.makedirs(os.path.dirname(out_filename))

            ret_val = subprocess.run(
                ['ffmpeg',
                 '-y',  # Allow overwrite
                 '-ss', str(t_start),
                 '-i', filename,
                 '-c', 'copy',
                 '-t', str(t_duration),
                 out_filename],
                stdin=None, stdout=None, stderr=None,
            )

            if ret_val.returncode == 0:
                n_trimmed += 1

    print('Downloaded: {}'.format(n_downloaded))
    print('Trimmed: {}'.format(n_trimmed))


if __name__ == '__main__':
    autoarg.run(download_vids)
