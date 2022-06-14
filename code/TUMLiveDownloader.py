import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import PySimpleGUI as sg
from signal import signal, SIGINT

sg.theme('DarkAmber')

# {
#     <url>: <filename>, ...
# }
lectures = {}

browser = None

window_main = None
window_main_thread = None


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
                lecture_info = browser.find_element(By.CSS_SELECTOR, '#streamInfo h1')

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


def graphical_ui():
    global browser
    global window_main
    global lectures

    browser = webdriver.Firefox()
    browser.get('https://live.rbg.tum.de')

    lecture_list = 'The lectures you selected will be listed here:\n'
    layout_main = [
        [sg.Text(lecture_list, key='_LECTURES_LIST_')],
        [sg.HorizontalSeparator()],
        [sg.Button('Select lecture'), sg.Button('Download lectures', disabled=True)],
        [sg.HorizontalSeparator()],
        [sg.Text(f'TITLE: ?', key='_TITLE_')],
        [sg.Text(f'URL: ?', key='_URL_')],
        [sg.Text('filename (without extension)'), sg.Input(key='_FILENAME_')],
        [sg.Button('Add lecture', disabled=True), sg.Button('Deselect lecture', disabled=True)]
    ]

    window_main = sg.Window('TUMLiveDownloader', layout_main)

    url = None
    while True:
        event, values = window_main.read()
        if event == sg.WIN_CLOSED:
            # TODO: check if lectures are currently downloaded or in queue and
            #       ask for confirmation
            window_main.close()
            window_main = None
            end(None, None)
        elif event == 'Select lecture':
            print('Selecting lecture.')
            try:
                video = browser.find_element(By.CSS_SELECTOR, '#watchContent video source')
                lecture_info = browser.find_element(By.CSS_SELECTOR, '#streamInfo h1')

                url = video.get_attribute("src")
                title = lecture_info.text
                print(f'URL: {url}')

                window_main['_TITLE_'].update(f'TITLE: {title}')
                window_main['_URL_'].update(f'URL: {url}')
                window_main['_FILENAME_'].update(title)

                window_main['Add lecture'].update(disabled=False)
                window_main['Deselect lecture'].update(disabled=False)
            except NoSuchElementException:
                print('No video found! Open a lecture first (pretend you want to watch it now).')
        elif event == 'Add lecture':
            if url is None:
                print('Nothing to add. Select a lecture first.')
                continue

            # TODO: check if filename is valid
            filename = values['_FILENAME_']
            filename += '.mp4'

            lecture_list += f'\n{filename}'
            window_main['_LECTURES_LIST_'].update(lecture_list)

            lectures[url] = filename

            window_main['_TITLE_'].update('TITLE: ?')
            window_main['_URL_'].update('URL: ?')
            window_main['_FILENAME_'].update('')

            window_main['Download lectures'].update(disabled=False)
            window_main['Add lecture'].update(disabled=True)
            window_main['Deselect lecture'].update(disabled=True)

            url = None
            print('Lecture added')
        elif event == 'Deselect lecture':
            window_main['_TITLE_'].update('TITLE: ?')
            window_main['_URL_'].update('URL: ?')
            window_main['_FILENAME_'].update('')

            window_main['Add lecture'].update(disabled=True)
            window_main['Deselect lecture'].update(disabled=True)

            url = None
            print('Lecture deselected')
        elif event == "Download lectures":
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
    global window_main

    if not browser is None:
        print('Closing browser')
        browser.close()
        browser = None

    if not window_main is None:
        window_main.close()
        window_main = None

    print('Goodbye!')
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, end)
    terminal_ui()
    #graphical_ui()
    input()
