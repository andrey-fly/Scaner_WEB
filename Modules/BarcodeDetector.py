from pyzbar import pyzbar
import cv2


class BarcodeDetector:
    def detect(self, filepath):
        image = cv2.imread(filepath)
        barcodes = pyzbar.decode(image)
        response = []
        # print(barcodes)
        for barcode in barcodes:
            # print(barcode.data.decode('ascii'))
            item = {'barcode': barcode.data.decode('ascii'),
                    'rect': {
                        'x': barcode.rect.left,
                        'y': barcode.rect.top,
                        'width': barcode.rect.width,
                        'height': barcode.rect.height
                        }
                    }
            response.append(item)

        return response