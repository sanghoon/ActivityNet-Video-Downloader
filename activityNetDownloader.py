import os
import json
import pafy
import autoarg


def download_vids(json_path='activity_net.v1-3.min.json', download_dir='./downloaded/', trimmed_dir='./trimmed/'):
    videoCounter = 0

    # open json file
    with open(json_path) as data_file:
        data = json.load(data_file)

    # take only video informations from database object
    videos = data['database']

    # iterate through dictionary of videos
    for key in videos:
        # take video
        video = videos[key]

        # find video subset
        subset = video['subset']

        # find video label
        annotations = video['annotations']
        label = ''
        if len(annotations) != 0:
            label = annotations[0]['label']
            label = '/' + label.replace(' ', '_')

        # create folder named as <label> if does not exist
        label_dir = download_dir + subset + label
        if not os.path.exists(label_dir):
            os.makedirs(label_dir)

        # take url of video
        url = video['url']

        # start to download
        try:
            video = pafy.new(url)
            best = video.getbest(preftype="flv")
            filename = best.download(filepath=label_dir + '/' + key)
            print('Downloading... ' + str(videoCounter) + '\n')
            videoCounter += 1
        except Exception as inst:
            print('Error!')


if __name__ == '__main__':
    autoarg.run(download_vids)