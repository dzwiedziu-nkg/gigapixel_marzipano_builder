# Gigapixel panorama splitter

This script do:

1. Open large TIFF file.
2. Split to tiles with various zoom.
3. Build Marzipano.js flat project. 

See: https://www.marzipano.net/demos/flat/

How to use:

Prerequisites: install python 3.x (tested on 3.11) and dependency libraries from `requirements.txt`.

1. Please run `python gui.py`.
2. Clicks `Select` button in **Source file** line.
3. Select your large TIFF file.
4. Clicks `Process` button.
5. In `destination` dir you should have website with `index.html` file.
6. Upload website to your hosting.