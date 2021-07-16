import os
import httplib2
from argument_parser import argParser
from urllib.parse import urlparse


def get_link_meta(url):
    if not url:
        return 'template'
    return urlparse(url).hostname


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
html_path = '{}/html'.format(current_dir)
