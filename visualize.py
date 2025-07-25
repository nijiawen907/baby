from PIL import ImageDraw, Image


def draw_box(im, np_boxes, labels, scores, label_names):
    im = Image.fromarray(im)
    draw_thickness = min(im.size) // 160  # 320
    width, height = im.size
    draw = ImageDraw.Draw(im)
    # font = ImageFont.truetype(size=20)
    clsid2color = {}
    color_list = get_color_map_list(len(label_names))
    # expect_boxes = (np_boxes[:, 1] > threshold) & (np_boxes[:, 0] > -1)
    # np_boxes = np_boxes[expect_boxes, :]

    for box, label, score in zip(np_boxes, labels, scores):
        if label not in clsid2color:
            clsid2color[label] = color_list[label]
        color = tuple(clsid2color[label])
        x_min = max(0, box[0])
        y_min = max(0, box[1])
        x_max = min(width, box[2])
        y_max = min(height, box[3])
        text = f"{label_names[label]}-{score:.4f}"
        draw.line(
            [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min),
             (x_min, y_min)],
            width=draw_thickness,
            fill=color)
        # tw, th = draw.textsize(text)
        left, top, right, bottom = draw.textbbox((0, 0), text)
        tw, th = right, bottom
        draw.rectangle(
            [(x_min + 1, y_min), (x_min + tw + 1, y_min + th)], fill=color)
        draw.text((x_min + 1, y_min), text, fill=(255, 255, 255))

    return im


def get_color_map_list(num_classes):
    """
    Args:
        num_classes (int): number of class
    Returns:
        color_map (list): RGB color list
    """
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = [color_map[i:i + 3] for i in range(0, len(color_map), 3)]
    return color_map
