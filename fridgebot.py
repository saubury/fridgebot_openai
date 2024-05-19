import argparse
import json
import sys
from pathlib import Path
from video_util import extract_images_from_video
from openai_util import image_diff
from todoist_util import add_task

def get_item_from_dict(image_diff_dict):  
    message_item = image_diff_dict['choices'][0]['message']['content']
    return message_item

def save_dict_to_file(json_file, image_diff_dict):
    with open(json_file, 'w') as fp:
        json.dump(image_diff_dict, fp)

def read_dict_to_file(json_file):
    with open(json_file) as json_file:
        image_diff_dict = json.load(json_file)
    return image_diff_dict


if __name__=='__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--video', help='path to video', required=True)
    argp.add_argument("--openai", action="store_true", help="enable API call to OpenAI")
    argp.add_argument("--todoist", action="store_true", help="enable API call to Todoist")

    args = argp.parse_args()

    video_file = args.video
    image_1 = str(Path(video_file).with_suffix('.1.jpg'))
    image_2 = str(Path(video_file).with_suffix('.2.jpg'))
    json_file = str(Path(video_file).with_suffix('.json'))
    extract_images_from_video(video_file, image_1, image_2)
    print(f'Extracting images {image_1} and {image_2}')

    if not args.openai:
        # Have not enabled OpenAP call - exit
        sys.exit()
    
    image_diff_dict = image_diff(image_1, image_2)
    save_dict_to_file(json_file, image_diff_dict)
    removed_item = get_item_from_dict(image_diff_dict)
    print(f'Removed item {removed_item}')


    if not args.todoist:
        # Have not enabled Todoist call - exit
        sys.exit()

    add_task(removed_item)
    print(f'Adding todoist item {removed_item}')
