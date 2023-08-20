import os
from pathlib import Path

os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()
import cv2
import math
import shutil


class TiffImage:
    def __init__(self, file):
        self.src = file
        self.image = cv2.imread(file, cv2.IMREAD_COLOR)

    def default_logger(self, text):
        print(text, end=None)

    def make_tiles(self, out_dir, logger=None, tileSizeX=1024, tileSizeY=1024, title='', description=''):

        if logger is None:
            logger = self.default_logger

        image = self.image
        fname = Path(self.src).stem
        p = Path(out_dir).joinpath(fname)
        out_path = str(Path(out_dir).joinpath(fname).joinpath('tiles'))

        logger('Prepare dir: %s\n' % out_path)

        os.makedirs(p, exist_ok=True)
        index_html = str(p.joinpath('index.html'))
        shutil.copyfile('./template/flat/index.html', index_html)
        shutil.copyfile('./template/flat/index.js', str(p.joinpath('index.js')))
        shutil.copyfile('./template/flat/style.css', str(p.joinpath('style.css')))
        f_js = open(str(p.joinpath('index.js')), 'a+')

        with open(index_html, "r+") as file:
            contents = file.read()
            contents = contents.replace('{{title}}', title)
            contents = contents.replace('{{description}}', description)
            file.seek(0)
            file.write(contents)
            file.truncate()

        makeLastPartFull = False

        divs = []
        div = 1
        while True:
            numTilesX = math.ceil(image.shape[1] / div / tileSizeX)
            numTilesY = math.ceil(image.shape[0] / div / tileSizeY)
            divs.append(div)
            if numTilesX == 1 and numTilesY == 1:
                break
            div *= 2

        divs = reversed(divs)

        no = -1
        print('var geometry = new Marzipano.FlatGeometry([', file=f_js)
        for div in divs:
            no += 1
            numTilesX = math.ceil(image.shape[1] / div / tileSizeX)
            numTilesY = math.ceil(image.shape[0] / div / tileSizeY)

            print('  { width: %d, height: %d, tileWidth: %d, tileHeight: %d },' % (math.ceil(image.shape[1]/div), math.ceil(image.shape[0]/div), tileSizeX, tileSizeY), file=f_js)
            logger('Writing %d zoom level...\n' % no)

            for nTileX in range(numTilesX):
                for nTileY in range(numTilesY):
                    startX = nTileX * tileSizeX * div
                    endX = startX + tileSizeX * div
                    startY = nTileY * tileSizeY * div
                    endY = startY + tileSizeY * div

                    if endY > image.shape[0]:
                        endY = image.shape[0]

                    if endX > image.shape[1]:
                        endX = image.shape[1]

                    if makeLastPartFull and (nTileX == numTilesX - 1 or nTileY == numTilesY - 1):
                        startX = endX - tileSizeX * div
                        startY = endY - tileSizeY * div

                    currentTile = image[startY:endY, startX:endX]
                    if currentTile.sum() == 0:
                        continue
                    if div > 1:
                        currentTile = cv2.resize(currentTile, (
                        math.ceil(currentTile.shape[1] / div), math.ceil(currentTile.shape[0] / div)),
                                                 interpolation=cv2.INTER_AREA)
                    out_path_tile = out_path + os.sep + 'z' + str(no) + os.sep + 'x' + str(nTileX) + os.sep
                    os.makedirs(out_path_tile, exist_ok=True)
                    cv2.imwrite(out_path_tile + str(no) + "-" + str(nTileX) + "-" + str(nTileY) + ".jpg", currentTile, [cv2.IMWRITE_JPEG_QUALITY, 80])

        print(']);', file=f_js)
        print('', file=f_js)
        print('var limiter = Marzipano.util.compose(', file=f_js)
        print('  Marzipano.FlatView.limit.resolution(%d),' % image.shape[1], file=f_js)
        print('  Marzipano.FlatView.limit.letterbox()', file=f_js)
        print(');', file=f_js)
        print('var view = new Marzipano.FlatView({ mediaAspectRatio: %d/%d}, limiter);' % (image.shape[1], image.shape[0]), file=f_js)
        with open('./template/flat/index.js2') as ff:
            for l in ff.readlines():
                print(l,end='', file=f_js)
        f_js.close()
        logger('Done\n')


#make_tiles("D:\\foto\\dxo_2023-03-12-kozia_gorka\\g2\\g2-out")
