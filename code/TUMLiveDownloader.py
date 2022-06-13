import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# {
#     <url>: <filename>, ...
# }
lectures = {}


def terminal_ui():
    global lectures

    driver = webdriver.Firefox()
    driver.get('https://live.rbg.tum.de')

    print('You can now log into your TUM account to unlock your lectures.')
    print()
    print('Click on a lecture you would like to download and choose the configuration (presenter, camera, combined).')

    while True:
        print()
        user_select = input('(A)dd current lecture to list OR (D)ownload lectures in list?: ')
        if user_select.lower() == 'a':
            try:
                video = driver.find_element(By.CSS_SELECTOR, '#watchContent video source')

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

    driver.close()
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


if __name__ == '__main__':
    terminal_ui()
    input()
    print('Goodbye!')
