import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import PySimpleGUI as sg

sg.theme('DarkAmber')

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


def graphical_ui():
    driver = webdriver.Firefox()
    driver.get('https://live.rbg.tum.de')

    filenames_list = 'The selected lectures will be listed here...'

    layout_main = [
        [sg.Text(filenames_list, key='_LECTURES_LIST_')],
        [sg.Button('Add lecture'), sg.Button('Download lectures')]
    ]

    window_main = sg.Window('TUMLiveDownloader', layout_main)

    while True:
        event_main, values_main = window_main.read()
        if event_main == sg.WIN_CLOSED:
            exit()
        elif event_main == 'Add lecture':
            try:
                video = driver.find_element(By.CSS_SELECTOR, '#watchContent video source')

                url = video.get_attribute("src")
                print(f'URL: {url}')

                filename = None
                layout_filename = [
                    [sg.Text(f'URL: {url}')],
                    [sg.Text('filename (without extension)'), sg.Input(key='_FILENAME_')],
                    [sg.Button('Add lecture'), sg.Button('Cancel')]
                ]
                window_filename = sg.Window('Specify filename', layout_filename)
                while True:
                    event_filename, values_filename = window_filename.read()
                    if event_filename == sg.WIN_CLOSED or event_filename == 'Cancel':
                        break
                    elif event_filename == 'Add lecture':
                        filename = values_filename['_FILENAME_']
                        break
                window_filename.close()

                if filename is None:
                    print('Canceled.')
                    continue

                filename = filename + '.mp4'
                print(f'filename: {filename}')
                lectures[url] = filename

                if len(lectures) > 0:
                    filenames_list += '\n' + filename
                else:
                    filenames_list = filename
                window_main['_LECTURES_LIST_'].update(filenames_list)

                print('Added lecture.')
            except NoSuchElementException:
                print('No video found! Open a lecture first (pretend you want to watch it now).')
        elif event_main == "Download lectures":
            break

    driver.close()
    window_main.close()
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
    #terminal_ui()
    graphical_ui()
    input()
    print('Goodbye!')
