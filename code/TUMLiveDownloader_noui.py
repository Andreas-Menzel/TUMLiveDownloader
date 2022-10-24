import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from signal import signal, SIGINT


# {
#     <url>: <filename>, ...
# }
lectures = {}

browser = None


def terminal_ui():
    global browser
    global lectures

    browser = webdriver.Firefox()
    browser.get('https://live.rbg.tum.de')

    print('You can now log into your TUM account to unlock your lectures.')
    print()
    print('Click on a lecture you would like to download and choose the configuration (presenter, camera, combined).')

    while True:
        print()
        user_select = input('(A)dd current lecture to list OR (D)ownload lectures in list?: ')
        if user_select.lower() == 'a':
            try:
                video = browser.find_element(By.CSS_SELECTOR, '#watchContent video source')
                lecture_info = browser.find_element(By.CSS_SELECTOR, 'h1')

                title = lecture_info.text
                print(f'TITLE: {title}')
                url = video.get_attribute("src")
                print(f'URL: {url}')
                filename = input('filename (without extension): ')
                filename = filename + '.mp4'
                lectures[url] = filename

                print('Added lecture.')
            except NoSuchElementException:
                print('No video found! Open a lecture first (pretend you want to watch it now).')
        elif user_select.lower() == 'd':
            print('Downloading lectures.')
            break
        else:
            print('Input not recognized.')

    browser.close()
    browser = None
    download_lectures()


# download_lectures
#
# @param    dict    _lectures       Dictionary that maps lecture urls
#                                       (m3u8 urls) to the filename it should be
#                                       saved to.
def download_lectures():
    global lectures

    print('Downloading...')
    for lecture_id, filename in lectures.items():
        subprocess.run(['ffmpeg', '-y', '-i', lecture_id, '-c', 'copy', '-f', 'mpegts', filename])


def end(signal_received, frame):
    global browser

    if not browser is None:
        print('Closing browser')
        browser.close()
        browser = None

    print('Goodbye!')
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, end)
    terminal_ui()
    input()
