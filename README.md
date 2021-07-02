# UNIVERSAL IMAGE FETCHER #

Image scraper built with Python 3.9 and Beautiful Soup. Fetches remote image assets accessed by any website...

    usage: image_fetcher.py [-h] [-w [website]] [-f filter_tags [filter_tags ...]] [-tags image_tags [image_tags ...]] [-a image_attributes [image_attributes ...]] -o output_dir [-u url_length] [-e extension]
                            [-l log_file]
    
    optional arguments:
      -h, --help            show this help message and exit
      -w [website]          Website url to fetch images from.
      -f filter_tags [filter_tags ...]
                            HTML filter tag to locate on.
      -tags image_tags [image_tags ...]
                            HTML tags to find image links through.
      -a image_attributes [image_attributes ...]
                            HTML image attribute to parse for links.
      -o output_dir         Output directory for fetched images.
      -u url_length         URL length of remote asset.
      -e extension          Output image extension.
      -l log_file           Log file to flush stdout.

### DEFAULT_VALUES ###
    default_output_extension    = 'png'    
    default_url_length          = 'long'
    default_filter_tag          = 'html'
    default_log_file            = 'logs/logger.txt'
    default_image_tags          = ['img', 'source', 'meta']
    default_image_attributes    = [ 'src', 'data-wood_src', 'data-large_image', 'data-srcset', 
                                    'srcset', 'data-src', 'content']
    
### REQUIREMENTS ###
Requires _Python 3.9_ and _BeautifulSoup 4_

### USAGE INSTRUCTIONS ###
* Set up python environment _(default environment manager from pycharm)_
* Start virtual environment ``` source <ENVIRONMENT_NAME>/bin/activate ```  
* Run ``` pip install < requirements.txt```

* Call function ```python image_fetcher.py [-args]```
