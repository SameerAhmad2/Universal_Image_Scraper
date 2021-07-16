import os
import sys

from default import args, http_client, current_dir, \
                    url_length, file_extension, \
                    log_file, output_dir

from helpers import get_html_files, get_image_name, inline_progress, \
    get_short_image_link, progress_bar, fetch_images, terminal_fetch_remote_asset


def run_fetcher(contents, stdout_file, output_directory):
    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('images/{}'.format(output_directory)):
        os.makedirs('images/{}'.format(output_directory))

    print('Fetching Images...')
    fetched_images = fetch_images(contents)
    frontier = []

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
            output_filename = get_image_name(short_img, count, file_extension)
            image_path = '{}/images/{}/{}'.format(current_dir, output_directory, output_filename)

            terminal_fetch_remote_asset(fetch_img, stdout_file, image_path)
        count += 1
    total_bar = progress_bar(100, 100)
    sys.stdout.flush()
    sys.stdout.write('[{}] {}% ...{}\n'.format(total_bar, 100.0, 'IMAGES SAVED! (SUCCESS)'))
    return


def setup_fetcher():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    stdout_file = '{}/logs/{}'.format(current_dir, log_file)

    if not args.w:
        files = get_html_files()
        for file_path in files:
            print('Opening File with Path:', file_path)
            with open(file_path) as html_file:
                file_info = html_file.read()
                file_basename = os.path.basename(file_path)
                new_output_dir = file_basename.split('.')[0]
                run_fetcher(file_info, stdout_file, new_output_dir)
        return

    _, response = http_client.request(args.w)
    return run_fetcher(response, stdout_file, output_dir)


setup_fetcher()
