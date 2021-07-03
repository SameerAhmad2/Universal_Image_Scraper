import os
import sys
import subprocess
import httplib2
import pathlib

from random import choice
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from argparse import ArgumentParser
from string import ascii_uppercase as au, ascii_lowercase as al, digits


def get_link_meta(url):
    if not url:
        return 'template'
    return urlparse(url).hostname


def generate_filename():
    random_chars = [choice(au + al + digits) for _ in range(16)]
    filename = ''.join(random_chars)
    return '{}.txt'.format(filename)


default_image_attributes = [
    'src', 'data-wood_src', 'data-large_image',
    'data-srcset', 'srcset', 'data-src', 'content'
]
default_link_tags = ['img', 'source', 'meta']

argParser = ArgumentParser()
argParser.add_argument('-w',
                       nargs='?',
                       metavar='website',
                       help='Website url to fetch images from.')

argParser.add_argument('-f',
                       metavar='filter_tags',
                       nargs='+',
                       default=[],
                       help='HTML filter tag to locate on (default is "html").')

argParser.add_argument('-tags',
                       metavar='image_tags',
                       nargs='+',
                       default=default_link_tags,
                       help='HTML tags to find image links through.')

argParser.add_argument('-a',
                       metavar='image_attributes',
                       nargs='+',
                       default=default_image_attributes,
                       help='HTML image attribute to parse for links.')

argParser.add_argument('output_dir',
                       metavar='output_dir',
                       type=pathlib.Path,
                       help='Output directory for fetched images.')

argParser.add_argument('-u',
                       metavar='url_length',
                       default='long',
                       help='URL length (["short" - no query params, "long" - full url (default)]).')

argParser.add_argument('-e',
                       metavar='extension',
                       default='png',
                       help='Output image extension (default is "png").')

argParser.add_argument('-l',
                       metavar='log_file',
                       default=generate_filename(),
                       help="Log file to flush stdout.")

args = argParser.parse_args()
http_client = httplib2.Http()
current_dir = os.getcwd()
output_dir = args.output_dir
filter_tags = args.f
image_attributes = args.a
url_length = args.u
file_extension = args.e
link_tags = args.tags
hostname = get_link_meta(args.w)
log_file = '{}__{}'.format(hostname, args.l)


def fetch_images(html_text):
    try:
        print('Starting Image Fetch...')
        if not filter_tags:
            filters = ['html']
        else:
            filters = filter_tags
        print('Breaking Down Site Information...')
        soup_tree = BeautifulSoup(html_text, 'html.parser')
        print('Locating All Images...')
        all_images = []
        for html_filter in filters:
            filter_images = []
            sub_tags = soup_tree.findAll(html_filter)
            for component in sub_tags:
                for link_tag in link_tags:
                    filter_images.extend(component.findAll(link_tag))
            for image_index in range(len(filter_images)):
                extracted_images = []
                image_tag = filter_images[image_index]
                for attr in image_attributes:
                    long_image_string = image_tag.get(attr, '')
                    spaced_strings = long_image_string.split(' ')
                    for string in spaced_strings:
                        if 'https' in string or 'http' in string:
                            extracted_images += [(string, attr)]
                all_images += extracted_images
        return all_images
    except ():
        print('Image Fetch Failed! Aborted!\n')


def get_html_contents():
    if not args.w:
        html_file_path = 'template.html'
        absolute_html_path = '{}/{}'.format(current_dir, html_file_path)
        with open(absolute_html_path) as html_file:
            return html_file.read()
    status, response = http_client.request(args.w)
    return response


def image_has_extension(image_path):
    image_extensions = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg')
    return image_path\
        .lower()\
        .endswith(image_extensions)


def progress_bar(fill, total):
    return '=' * fill + '-' * (total - fill)


def get_short_image_link(image_link):
    question_index = image_link.find('?')
    if question_index < 0:
        return image_link
    return image_link[:question_index]


def inline_progress(count, total, status=''):
    bar_len = 100
    filled_len = int(round(bar_len * count / float(total)))
    percent = round(100.0 * count / float(total), 1)
    bar = progress_bar(filled_len, bar_len)
    sys.stdout.write('[{}] {}{} ...{}\r'.format(bar, percent, '%', status))
    sys.stdout.flush()


def setup_fetcher():
    html_information = get_html_contents()
    fetched_images = fetch_images(html_information)
    stdout_file = '{}/logs/{}'.format(current_dir, log_file)
    frontier = []
    print('Fetching Images...')

    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('{}/{}'.format('images', output_dir)):
        os.makedirs('{}/{}'.format('images', output_dir))

    count = 0
    total = len(fetched_images)
    for (img, attr_type) in fetched_images:
        inline_progress(count, total, 'FETCH IN PROGRESS')
        long_img = img
        short_img = get_short_image_link(img)
        if img not in frontier:
            fetch_img = long_img
            frontier += [img]
            if url_length == 'short':
                fetch_img = short_img
            image_names = short_img.split("/")
            image_name = image_names[-1]
            if not image_name:
                image_name = image_names[-2]
            if not image_has_extension(image_name):
                image_name = '{}.{}'.format(image_name, file_extension)
            image_path = '{}/images/{}/{}'.format(current_dir, output_dir, image_name)
            subprocess.call(['wget', fetch_img, '-O', image_path],
                            stdout=open(stdout_file, 'a'),
                            stderr=subprocess.STDOUT)
        count += 1
    total_bar = progress_bar(100, 100)
    sys.stdout.flush()
    sys.stdout.write('[{}] {}{} ...{}\n'.format(total_bar, 100.0, '%', 'IMAGES SAVED! (SUCCESS)'))
    return


setup_fetcher()
