from PIL import Image, ImageDraw, ImageFont, ImageFont
import os

colorPalletes = dict()

# From https://sashamaps.net/docs/tools/20-colors/
colorPalletes['original'] = {
    'Button': (255, 255, 25),
    'Label': (60, 180, 75),
    'Screen': (230, 25, 75),
    'TextBox': (0, 130, 200),
    'Image': (145, 30, 180),
    'CheckBox': (245, 130, 48),
    'ListPicker': (250, 190, 212),
    'Switch': (70, 240, 240),
    'Slider': (240, 50, 230),
    'Map': (210, 245, 60)
}

# From https://bookdown.org/hneth/ds4psy/D-2-apx-colors-essentials.html + Sugestao Nathalie
colorPalletes['pal1'] = {
    'Button': "#999999",
    'Label': "#E69F00",
    'Screen': "#56B4E9",
    'TextBox': "#009E73",
    'Image': "#F0E442",
    'CheckBox': "#0072B2",
    'ListPicker': "#D55E00",
    'Switch': "#CC79A7",
    'Slider': "#8C74D2",
    'Map': "#847848"
}
colorPalletes['pal2'] = {
    'Button': "#000000",
    'Label': "#E69F00",
    'Screen': "#56B4E9",
    'TextBox': "#009E73",
    'Image': "#F0E442",
    'CheckBox': "#0072B2",
    'ListPicker': "#D55E00",
    'Switch': "#CC79A7",
    'Slider': "#8C74D2",
    'Map': "#847848"
}

# From https://medialab.github.io/iwanthue/
colorPalletes['iwanthue'] = {
    'Button': "#54de45",
    'Label': "#7320c0",
    'Screen': "#9fe633",
    'TextBox': "#332ebb",
    'Image': "#e7e027",
    'CheckBox': "#6255ea",
    'ListPicker': "#ec3e22",
    'Switch': "#ab4bea",
    'Slider': "#f2279f",
    'Map': "#d43dd3"
}

# From https://mokole.com/palette.html
colorPalletes['mokole'] = {
    'Button': "#006400",
    'Label': "#00008b",
    'Screen': "#b03060",
    'TextBox': "#ff0000",
    'Image': "#ffd700",
    'CheckBox': "#7fff00",
    'ListPicker': "#00ffff",
    'Switch': "#ff00ff",
    'Slider': "#6495ed",
    'Map': "#ffdab9"
}

# https://seaborn.pydata.org/generated/seaborn.color_palette.html
'''
Original code:
    import seaborn as sns
    snsCollorPallete = sns.color_palette("bright")
    newCollorPallete = list()
    for color in snsCollorPallete:
        newColor = tuple(int(value * 255) for value in color)
        newCollorPallete.append(newColor)
    for color in newCollorPallete:
        print(color)
    colorPalletes['seaborn'] = {
        'Button': newCollorPallete[0],
        'Label': newCollorPallete[1],
        'Screen': newCollorPallete[2],
        'TextBox': newCollorPallete[3],
        'Image': newCollorPallete[4],
        'CheckBox': newCollorPallete[5],
        'ListPicker': newCollorPallete[6],
        'Switch': newCollorPallete[7],
        'Slider': newCollorPallete[8],
        'Map': newCollorPallete[9]
    }
'''
colorPalletes['seaborn'] = {
    'Button': (2, 62, 255),
    'Label': (255, 124, 0),
    'Screen': (26, 201, 56),
    'TextBox': (232, 0, 11),
    'Image': (139, 43, 226),
    'CheckBox': (159, 72, 0),
    'ListPicker': (241, 76, 193),
    'Switch': (163, 163, 163),
    'Slider': (255, 196, 0),
    'Map': (0, 215, 255)
}

# Select color pallete
colorDict = colorPalletes['seaborn']
# Get font
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 35)
# Options:
text_enable = True
text_border_enable = False


def getCoords(component):
    return [(component.x1, component.y1), (component.x2, component.y2)]

def get_label(component):
    return component.label

def translate_label(label, language='en'):
    return label
    

def generate_preview(
    image_path,
    components,
    language='en',
    show = False
):
    image = Image.open(image_path)
    image = image.resize((720, 1280))
    image = image.convert('RGB')

    draw = ImageDraw.Draw(image)

    for component in components:
        # Get coordinates and label
        [(x0, y0), (x1, y1)] = getCoords(component=component)
        label = get_label(component)

        # Draw multiple rectangles for thicker borders
        draw.rectangle([(x0, y0), (x1, y1)], fill=None,
                    outline=colorDict[label])
        for delta in [0, 1, -1, 2, -2]:
            draw.rectangle([(x0 - delta, y0 - delta), (x1 + delta, y1 + delta)],
                        fill=None, outline=colorDict[label])

        # Draw text
        
        text_y_compensation = -37
        text_x_compensation = 0
        #text_color = (255, 255, 255, 255)
        text_color = colorDict[label]
        text_border_color = (255, 255, 255, 255)

        label_text = translate_label(label, language='en')
        if text_enable:
            if text_border_enable:
                for delta in [1, -1, ]:
                    draw.text((x0 + text_x_compensation + delta, y0 + text_y_compensation),
                            label_text, font=font, fill=text_border_color)
                    draw.text((x0 + text_x_compensation, y0 + text_y_compensation +
                            delta), label_text, font=font, fill=text_border_color)
                    draw.text((x0 + text_x_compensation + delta, y0 + text_y_compensation +
                            delta), label_text, font=font, fill=text_border_color)
            draw.text((x0 + text_x_compensation, y0 + text_y_compensation),
                    label_text, font=font, fill=text_color)
    if show:
        image.show()
    return image

def save_preview(
    image_path,
    components,
    destination_path,
    language='en',
    show = False
):
    image = generate_preview(image_path=image_path, components=components, language=language, show=show)
    image.save(destination_path)