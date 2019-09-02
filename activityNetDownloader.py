import os
import json
import pafy
import autoarg


def download_vids(json_path='activity_net.v1-3.min.json', download_base='./downloaded/', trimmed_base='./trimmed/'):
    n_success = 0

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
            n_success += 1
        except Exception as e:
            print(print_header + 'Failed! {} : '.format(url, e))

        # TODO: trim videos


if __name__ == '__main__':
    autoarg.run(download_vids)
