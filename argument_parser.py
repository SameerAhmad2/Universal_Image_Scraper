import pathlib

from random import choice
from argparse import ArgumentParser
from string import ascii_uppercase as au, \
                    ascii_lowercase as al, \
                    digits


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
