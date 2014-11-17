import os
from django.conf import settings
from subprocess import Popen, PIPE
from selenium import webdriver
import selenium.webdriver.support.ui as ui

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height):
    print "Capturing screen.."
    driver = webdriver.PhantomJS(
        executable_path=settings.NODE_BINARIES['PHANTOMJS'],
        service_log_path=os.path.join(settings.LOG_DIR, 'ghostdriver.log'))
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(
    #     service_log_path='/var/log/phantomjs/ghostdriver.log')
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)

    wait = ui.WebDriverWait(driver, 10)

    driver.get(url)
    print driver.current_url
    try:
        wait.until(lambda driver: driver.find_element_by_tag_name('svg'))
        driver.save_screenshot(screen_path)
    finally:
        driver.quit()


def do_crop(params):
    print "Croping captured image.."
    command = [
        'convert',
        params['screen_path'],
        '-crop', '%sx%s+0+0' % (params['width'], params['height']),
        params['crop_path']
    ]
    execute_command(' '.join(command))


def do_thumbnail(params):
    print "Generating thumbnail from croped captured image.."
    command = [
        'convert',
        params['crop_path'],
        '-filter', 'Lanczos',
        '-thumbnail', '%sx%s' % (params['width'], params['height']),
        params['thumbnail_path']
    ]
    execute_command(' '.join(command))


def get_screen_shot(**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 650))
    height = int(kwargs.get('height', 600))
    filename = kwargs.get('filename', 'screen.png')

    # directory path to store screen
    path = kwargs.get('path', ROOT)

    # crop the captured screen
    crop = kwargs.get('crop', False)
    crop_width = int(kwargs.get('crop_width', width))
    crop_height = int(kwargs.get('crop_height', height))

    # does crop image replace original screen capture?
    crop_replace = kwargs.get('crop_replace', False)

    # generate thumbnail from screen, requires crop=True
    thumbnail = kwargs.get('thumbnail', False)
    thumbnail_width = int(kwargs.get('thumbnail_width', width))
    thumbnail_height = int(kwargs.get('thumbnail_height', height))

    # does thumbnail image replace crop image?
    thumbnail_replace = kwargs.get('thumbnail_replace', False)

    screen_path = abspath(path, filename)
    crop_path = thumbnail_path = screen_path

    if thumbnail and not crop:
        raise Exception, 'Thumnail generation requires crop image, set crop=True'

    do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, 'crop_'+filename)
        params = {
            'width': crop_width, 'height': crop_height,
            'crop_path': crop_path, 'screen_path': screen_path}
        do_crop(params)

        if thumbnail:
            if not thumbnail_replace:
                thumbnail_path = abspath(path, 'thumbnail_'+filename)
            params = {
                'width': thumbnail_width, 'height': thumbnail_height,
                'thumbnail_path': thumbnail_path, 'crop_path': crop_path}
            do_thumbnail(params)
    return screen_path, crop_path, thumbnail_path
