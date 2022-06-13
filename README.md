# TUMLiveDownloader

## Usage

Execute the script and follow the instructions.

```
python TUMLiveDownloader.py
```

Selenium will open `live.rbg.tum.de` in a Firefox browser. You can now log into
your TUM account to unlock your lectures. Select a lecture in the browser and
type A (for 'add') in the terminal and choose a filename. Repeat the last step
until you have selected all lectures you want to download. Type D
(for 'download') in the terminal to download all selected lectures.

## Requirements

We need the python selenium module to be able to control a web-browser.

```
pip install selenium
```

Make sure you also have the appropriate browser driver installed: https://www.selenium.dev/documentation/getting_started/installing_browser_drivers/
