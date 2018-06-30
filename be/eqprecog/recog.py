# -*- coding:utf-8 -*-
from __future__ import print_function
import cv2
from functools import partial
import math
import base64
import json
import random

debug = 0


def main(file_path):
    # pic_filename = 'bg1.jpg'
    image_src = cv2.imread(file_path)
    image = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图像
    canny = cv2.Canny(image, 50, 150)
    # debug > 2 and cv2.imshow("canny", canny)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    img, contours, hierarchy = cv2.findContours(canny, 1, 2)
    cell_points = calc_valid_cells(contours, image, image_src)
    debug and cv2.imshow("contours ", image_src)
    debug and cv2.waitKey()
    center_x, center_y, margin = calc_center_side(cell_points, image)
    center_x, center_y = rotate_point((center_x, center_y), image, -45, 0)
    print('center', center_x, center_y)
    debug and cv2.rectangle(image_src, (center_x - 50, center_y - 50), (center_x + 50, center_y + 50), (255, 255, 0), 2)

    _margin = int(margin * 1.414)
    _radius = int(margin * 1.414 * 31 / 188)

    cells = [
        {
            'name': 't',
            'x_center': center_x,
            'y_center': center_y - _margin
        },
        {
            'name': 'tl',
            'x_center': int(center_x - _margin / 2),
            'y_center': int(center_y - _margin / 2)
        },
        {
            'name': 'tr',
            'x_center': int(center_x + _margin / 2),
            'y_center': int(center_y - _margin / 2)
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
            'x_center': int(center_x - _margin / 2),
            'y_center': int(center_y + _margin / 2)
        },
        {
            'name': 'br',
            'x_center': int(center_x + _margin / 2),
            'y_center': int(center_y + _margin / 2)
        },
        {
            'name': 'b',
            'x_center': center_x,
            'y_center': center_y + _margin
        },
    ]
    # for cell in cells:
    #     cv2.rectangle(image_src, (cell['x_center'] - _radius, cell['y_center'] - _radius), (cell['x_center'] + _radius, cell['y_center'] + _radius), (255, 255, 0), 2)
    # debug and cv2.imshow("contours ", image_src)
    # debug and cv2.waitKey()
    # debug and cv2.waitKey()
    # debug and cv2.destroyAllWindows()

    cells = [collect_cell(image_src, _radius, cell) for cell in cells]

    debug and cv2.waitKey()
    debug and cv2.destroyAllWindows()
    return cells


def is_in_rect(contours, c):
    x0, y0, w0, h0 = cv2.boundingRect(c)
    counter = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # print('x, y, w, h', x, y, w, h)
        if x in range(x0, x0 + w0) and y in range (y0, y0 + h0):
            counter += 1
    return counter


def calc_valid_cells(contours, image, image_src):
    cell_points = {
        (60, 75): [],
        (50, 60): [],
        (40, 50): [],
        (30, 40): [],
    }
    # blue green red light-blue yellow
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
    # cell_points.append(rotate_point((x + w / 2, y + h / 2), image, 45))
    f = open('./dumps.json', 'w+')
    f.write(str(contours))
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # debug > 1 and w in range(30, 70) and h in range(30, 70) and cv2.rectangle(image_src, (x, y), (x + w, y + h), colors[0], 2)
        color_i = 0
        for rg in cell_points.keys():
            diff = 5
            if rg == (30, 40):
                diff = 3
            if w in range(*rg) and h in range(*rg) and abs(w - h) < diff and is_in_rect(contours, c) > 8:
                cell_points[rg].append(rotate_point((x + w / 2, y + h / 2), image, 45))
                debug > 1 and cv2.rectangle(image_src, (x, y), (x + w, y + h), colors[color_i], 2)
            color_i += 1

    max = -1
    ret = set()
    for key, val in cell_points.items():
        if len(val) > max:
            max = len(val)
            ret = set(val)
    if len(ret) <= 4:
        ret.update(set(cell_points[(60, 75)]))
    if len(ret) <= 4:
        ret.update(set(cell_points[(50, 60)]))
    if len(ret) <= 4:
        ret.update(set(cell_points[(40, 50)]))
    if len(ret) <= 4:
        ret.update(set(cell_points[(30, 40)]))
    # debug > 1 and cv2.imshow("contours ", image_src)
    # debug > 1 and cv2.waitKey()
    # debug > 1 and cv2.destroyAllWindows()
    return list(ret)


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


def similar_uniq(src_list, diff=3):
    sorted_list = sorted(src_list)
    uniq_list = []
    jump_i = 0
    for i in range(0, len(sorted_list)):
        if i < jump_i:
            continue
        similars = [sorted_list[i]]
        for similar_i in range(i + 1, len(sorted_list)):
            if abs(similars[-1] - sorted_list[similar_i]) < diff:
                similars.append(sorted_list[similar_i])
                jump_i = similar_i + 1
            else:
                jump_i = similar_i
                break
        uniq_list.append(sum(similars) / len(similars))
    return uniq_list


def get_div_margin(num_list, diff=3):
    sorted_list = sorted(num_list)
    length = len(sorted_list)
    if length < 2:
        return -1
    margins = []
    for index, num in enumerate(sorted_list):
        if index == 0:
            continue
        margin = num - sorted_list[index - 1]
        find_index(lambda x, i: abs(margin-x) > diff, margins) < 0 and margins.append(num - sorted_list[index - 1])
    if len(margins) == length - 1:
        return sum(margins) / (length - 1)
    return -1


def find_similar(li, cmp):
    min_diff = 10000
    find = None
    for item in li:
        diff = abs(item - cmp)
        if diff < min_diff:
            min_diff = diff
            find = item
    return find


def calc_center_side(cell_centers, image):
    img_h, img_w = image.shape[:2]
    pic_center = list(rotate_point((img_w / 2, img_h / 2), image, 45))
    margin_max_limit = min(img_h, img_w) / 2 / 1.414

    points = []
    for point in cell_centers:
        if find_index(partial(is_similar, point), points) < 0:
            points.append(point)
    print('points', points)

    margin = -1
    x_eqs = similar_uniq([list(cell)[0] for cell in points], diff=10)
    y_eqs = similar_uniq([list(cell)[1] for cell in points], diff=10)
    debug > 1 and print('x_eqs', x_eqs, 'y_eqs', y_eqs)
    x_margin = get_div_margin(x_eqs, diff=10)
    y_margin = get_div_margin(y_eqs, diff=10)
    if x_margin > margin_max_limit:
        x_margin = x_margin / 2
    if y_margin > margin_max_limit:
        y_margin = y_margin / 2

    if x_margin > 0 and y_margin > 0 and abs(x_margin - y_margin) < 3:
        margin = (x_margin + y_margin) / 2

    center_x = -1
    center_y = -1
    if margin > 0:
        if len(x_eqs) == 3:
            center_x = sum(x_eqs) / len(x_eqs)
        if len(y_eqs) == 3:
            center_y = sum(y_eqs) / len(y_eqs)
        if center_x < 0:
            center_x = find_similar(x_eqs + ([sum(x_eqs) / len(x_eqs)]), max(center_y, pic_center[0]))
        if center_y < 0:
            center_y = find_similar(y_eqs + ([sum(y_eqs) / len(y_eqs)]), max(center_y, pic_center[1]))
        return center_x, center_y, margin


def find_index(test, li):
    for index, item in enumerate(li):
        if test(item, index):
            return index
    return -1


# 黄 120, 220, 244   118, 215, 250   105, 227, 255   111, 216, 255
# 绿 111, 233, 166   102, 233, 167   124, 229, 165   106, 233, 165, 140, 197, 175
# 红 112, 140, 233   102, 139, 254   98, 131, 250    106, 138, 250   190,150,132
# 蓝 242, 213, 106
# 灰 239, 254, 253
def color_classify(px):
    b, g, r = px
    ret = None
    if b > 200 and g > 180 and r < 150:
        ret = 'blue'
    if b < 140 and g < 170 and r > 200:
        ret = 'red'
    if b < 150 and g > 190 and r > 200:
        ret = 'yellow'
    if b < 200 and g > 180 and r < 200:
        ret = 'green'
    if ret is None and random.random() < 0.4 and debug == 0:
        ret = 'red'
    # return (ret or 'null') + '({r},{g},{b})'.format(r=r, g=g, b=b)
    return ret


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
#     name = '2018-06-26-141154-60907.jpg'
#     pic_filename = './pics/' + name
#     debug = 0
#     base_cells = main(pic_filename)
#     print('cells', [(cell['tl'], cell['tr'], cell['bl'], cell['br']) for cell in base_cells])
