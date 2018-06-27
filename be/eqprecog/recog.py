# -*- coding:utf-8 -*-
from __future__ import print_function
import cv2
from functools import partial
import math
import base64
import json
import random


def main(file_path, debug=0):
    # pic_filename = 'bg1.jpg'
    image_src = cv2.imread(file_path)
    image = cv2.cvtColor(image_src.copy(), cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图像
    canny = cv2.Canny(image, 50, 150)
    # cv2.imshow("canny", canny)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    img, contours, hierarchy = cv2.findContours(canny, 1, 2)
    _cell = []
    cell_points = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w in range(40, 70) and h in range(40, 70) and abs(w - h) < 10:
            _cell.append((x + w / 2, y + h / 2))
            cell_points.append(rotate_point((x + w / 2, y + h / 2), image, 45))
            debug > 1 and cv2.rectangle(image_src, (x, y), (x + w, y + h), (0, 255, 0), 2)

    print('cell_points length', len(cell_points))
    center_x, center_y = rotate_point(calc_center_point(cell_points), image, -45, 0)
    print('center', center_x, center_y)
    debug and cv2.rectangle(image_src, (center_x - 50, center_y - 50), (center_x + 50, center_y + 50), (255, 255, 0), 2)
    debug and cv2.imshow("contours ", image_src)

    _margin = 188
    _radius = 31

    cells = [
        {
            'name': 't',
            'x_center': center_x,
            'y_center': center_y - _margin
        },
        {
            'name': 'tl',
            'x_center': center_x - _margin / 2,
            'y_center': center_y - _margin / 2
        },
        {
            'name': 'tr',
            'x_center': center_x + _margin / 2,
            'y_center': center_y - _margin / 2
        },
        {
            'name': 'l',
            'x_center': center_x - _margin,
            'y_center': center_y
        },
        {
            'name': 'c',
            'x_center': center_x,
            'y_center': center_y
        },
        {
            'name': 'r',
            'x_center': center_x + _margin,
            'y_center': center_y
        },
        {
            'name': 'bl',
            'x_center': center_x - _margin / 2,
            'y_center': center_y + _margin / 2
        },
        {
            'name': 'br',
            'x_center': center_x + _margin / 2,
            'y_center': center_y + _margin / 2
        },
        {
            'name': 'b',
            'x_center': center_x,
            'y_center': center_y + _margin
        },
    ]

    cells = [collect_cell(image_src, _radius, cell) for cell in cells]
    # f = open('cells.json', 'w')
    # f.write(json.dumps(cells))

    debug and cv2.waitKey()
    debug and cv2.destroyAllWindows()
    return cells or json.dumps(cells)


def collect_cell(image, radius, cell):
    w = 20
    h = 4
    core_padding = 10
    ret = dict({
        'tl': image[int(cell['y_center'] - 19 - w / 2):int(cell['y_center'] - 19 + w / 2),
              int(cell['x_center'] - radius - h / 2):int(cell['x_center'] - radius + h / 2)],
        'tr': image[int(cell['y_center'] - 19 - w / 2):int(cell['y_center'] - 19 + w / 2),
              int(cell['x_center'] + radius - h / 2):int(cell['x_center'] + radius + h / 2)],
        'bl': image[int(cell['y_center'] + 19 - w / 2):int(cell['y_center'] + 19 + w / 2),
              int(cell['x_center'] - radius - h / 2):int(cell['x_center'] - radius + h / 2)],
        'br': image[int(cell['y_center'] + 19 - w / 2):int(cell['y_center'] + 19 + w / 2),
              int(cell['x_center'] + radius - h / 2):int(cell['x_center'] + radius + h / 2)],
        'core': image[int(cell['y_center'] - radius + core_padding):int(cell['y_center'] + radius - core_padding),
                int(cell['x_center'] - radius + core_padding):int(cell['x_center'] + radius - core_padding)]
    }, **cell)

    for pos in ['tl', 'tr', 'bl', 'br']:
        ret[pos] = cv2.resize(ret[pos], (int(h * .75), int(w * .75)), cv2.INTER_AREA)
        ret[pos] = color_classify(ret[pos][7, 1])
    ret['core'] = 'data:image/jpeg;base64,' + str(base64.b64encode(cv2.imencode('.jpg', ret['core'])[1]), 'utf-8')
    return ret


def calc_center_point(cell_centers):
    points = []
    for point in cell_centers:
        if find_index(partial(is_similar, point), points) < 0:
            points.append(point)

    x_centers = []
    y_centers = []
    for point in points:
        x_cells = list(filter(lambda cmp_point: is_similar(point, cmp_point, diff_x=10000, diff_y=3), points))
        if len(x_cells) == 3:
            x_centers.append(sum(map(lambda item: list(item)[0], x_cells)) / 3)

        y_cells = list(filter(lambda cmp_point: is_similar(point, cmp_point, diff_x=3, diff_y=10000), points))
        if len(y_cells) == 3:
            y_centers.append(sum(map(lambda item: list(item)[1], y_cells)) / 3)

    x_center = len(x_centers) and sum(x_centers) / len(x_centers)
    y_center = len(y_centers) and sum(y_centers) / len(y_centers)
    return x_center, y_center


def find_index(test, li):
    for index, item in enumerate(li):
        if test(item, index):
            return index
    return -1


# 黄 120, 220, 244   118, 215, 250   105, 227, 255   111, 216, 255
# 绿 111, 233, 166   102, 233, 167   124, 229, 165   106, 233, 165
# 红 112, 140, 233   102, 139, 254   98, 131, 250    106, 138, 250
# 蓝 242, 213, 106
# 灰 239, 254, 253
def color_classify(px):
    b, g, r = px
    if b > 200 and g > 180 and r < 150:
        return 'blue'
    if b < 140 and g < 170 and r > 200:
        return 'red'
    if b < 150 and g > 190 and r > 200:
        return 'yellow'
    if b < 140 and g > 200 and r < 200:
        return 'green'
    if random.random() < 0.3:
        return 'red'
    return None


def rotate_point(point, image, angle, acc=1):
    (img_h, img_w) = image.shape[:2]
    center = (img_h / 2, img_w / 2)

    angle = math.radians(angle)
    cx, cy = center
    x, y = point
    x0 = (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle) + cx
    y0 = (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle) + cy

    return (round(x0, acc), round(y0, acc)) if acc else (int(round(x0)), int(round(y0)))


def is_similar(p1, p2, diff_x=3, diff_y=3):
    p1x, p1y = p1
    p2x, p2y = p2
    if abs(p1x - p2x) <= diff_x and abs(p1y - p2y) <= diff_y:
        return True


# if __name__ == '__main__':
#     pic_filename = '../pics/dfd5f33e8794a4c2da2a3dd802f41bd5ac6e3992_meitu_1.jpg'
#     base_cells = main(pic_filename, debug=2)
#     print('cells', base_cells)
