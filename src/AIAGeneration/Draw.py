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
font = ImageFont.truetype("arial.ttf", 35)
# Options:
text_enable = True
text_border_enable = False

def getCoords(component):
    x_center = component[2][0]
    y_center = component[2][1]
    width = component[2][2]
    height = component[2][3]

    x0 = int(x_center - (width/2))
    x1 = int(x0 + width)
    y0 = int(y_center - (height/2))
    y1 = int(y0 + height)

    return [(x0, y0), (x1, y1)]


imagePath = os.path.join(os.getcwd(), "src\AIAGeneration\TestDraw")

'''
imagePath = os.path.join(imagePath, "Sketch.jpg")

components = [								
    ('Screen', 0.99, (346.94, 652.94, 609.78, 984.02)), 
    ('Image', 0.99, (351.41, 402.11, 442.75, 378.93)),
    ('TextBox', 0.99, (354.60, 696.46, 462.97, 109.71)), 
    ('TextBox', 0.99, (351.11, 815.46, 446.67, 106.20)), 
    ('Button', 0.99, (351.11, 967.97, 438.89, 106.28)), 
    ('Label', 0.99, (343.09, 1108.15, 270.10, 43.34))
]
'''

'''
imagePath = os.path.join(imagePath, "EcoPet - AlterarUmLocal2.jpg")

components = [
    ('Label', 0.9999958276748657, (212.43682861328125, 830.213134765625, 266.3381652832031, 50.52324676513672)), 
    ('Button', 0.9999911785125732, (134.59671020507812, 973.1155395507812, 164.02291870117188, 85.60356903076172)), 
    ('Button', 0.9999886751174927, (503.1837463378906, 666.7462158203125, 202.7159881591797, 80.74561309814453)), 
    ('Button', 0.9999877214431763, (136.8546142578125, 446.7038269042969, 156.98666381835938, 75.93196868896484)), 
    ('Button', 0.9999874830245972, (136.9950714111328, 711.47216796875, 162.83706665039062, 85.09457397460938)), 
    ('Label', 0.9999839067459106, (311.95599365234375, 678.4013671875, 111.79367065429688, 52.05448532104492)), 
    ('Button', 0.9999816417694092, (486.1203918457031, 415.1546630859375, 204.9807891845703, 78.33289337158203)), 
    ('Button', 0.9999803304672241, (523.2733764648438, 931.951171875, 183.9571533203125, 88.88633728027344)), 
    ('CheckBox', 0.9999761581420898, (258.3872375488281, 614.9593505859375, 409.1573486328125, 58.257789611816406)), 
    ('CheckBox', 0.9999754428863525, (237.61273193359375, 354.63775634765625, 352.4445495605469, 66.80245208740234)), 
    ('Label', 0.9999663829803467, (312.820556640625, 425.4028015136719, 77.72132873535156, 37.52653503417969)), 
    ('CheckBox', 0.9999462366104126, (521.1689453125, 812.0708618164062, 274.8893737792969, 45.524627685546875)), 
    ('Label', 0.9999405145645142, (234.4567413330078, 1087.6085205078125, 278.49810791015625, 83.171142578125)), 
    ('CheckBox', 0.999921441078186, (556.3511962890625, 269.0412292480469, 255.0456085205078, 55.24817657470703)), 
    ('Button', 0.9998469352722168, (56.864166259765625, 104.03385925292969, 76.1850814819336, 49.91840744018555)), 
    ('Label', 0.9997959136962891, (312.88140869140625, 97.338623046875, 382.8526306152344, 66.16636657714844)), 
    ('Label', 0.9997828006744385, (316.6494445800781, 940.2069702148438, 105.67227935791016, 53.299102783203125)),
    ('CheckBox', 0.9997601509094238, (267.5901184082031, 885.0139770507812, 388.629638671875, 69.70620727539062)), 
    ('CheckBox', 0.9996817708015442, (524.6470947265625, 539.3546752929688, 302.14385986328125, 56.19817352294922)), 
    ('Label', 0.9994997382164001, (219.10025024414062, 293.5255126953125, 341.52911376953125, 57.201210021972656)), 
    ('Label', 0.9991592168807983, (372.60345458984375, 190.32945251464844, 612.820556640625, 82.71978759765625)), 
    ('Label', 0.9968624114990234, (176.82998657226562, 568.8114013671875, 196.75421142578125, 41.77849578857422)), 
    ('TextBox', 0.9943249225616455, (347.1435852050781, 1174.62744140625, 496.14715576171875, 68.71861267089844)), 
    ('Button', 0.989172101020813, (648.965087890625, 90.55532836914062, 36.7580451965332, 53.2119140625)), 
    ('Screen', 0.9999985694885254, (356.4589538574219, 637.5841674804688, 719.811279296875, 1226.2314453125))
]
'''

imagePath = os.path.join(imagePath, "img003.jpg")

components = [
    ('Button', 0.999962329864502, (593.8041381835938, 111.48466491699219, 110.57611846923828, 104.03353881835938)), 
    ('TextBox', 0.9991134405136108, (202.4046630859375, 119.50770568847656, 298.2958068847656, 121.96676635742188)), 
    ('Button', 0.9997801780700684, (449.9340515136719, 121.67877960205078, 141.02940368652344, 107.51930236816406)), 
    ('TextBox', 0.9990062117576599, (209.05319213867188, 257.5668029785156, 294.6927185058594, 110.01659393310547)), 
    ('TextBox', 0.9586394429206848, (212.54368591308594, 395.3681945800781, 276.6354064941406, 120.87919616699219)), 
    ('Map', 0.9586394429206848, (515.5091247558594, 330.3681945800781, 276.6354064941406, 250.87919616699219)), 
    ('Image', 0.9998816251754761, (610.1162719726562, 538.2230224609375, 136.70437622070312, 111.59983825683594)), 
    ('Image', 0.9996281266212463, (459.5091247558594, 544.6812744140625, 138.01068115234375, 110.1566390991211)), 
    ('Image', 0.9979813098907471, (219.8675994873047, 554.17822265625, 297.6863708496094, 106.84182739257812)), 
    ('Screen', 0.9999974966049194, (350.3127136230469, 648.3035278320312, 690.0288696289062, 1250.39306640625)),
    ('Label', 0.9565469622612, (372.5961608886719, 678.6742553710938, 687.706298828125, 39.973365783691406)), 
    ('Slider', 0.7774834632873535, (379.6529235839844, 760.2062377929688, 507.5635986328125, 56.51338195800781)), 
    ('ListPicker', 0.5094987154006958, (560.0575561523438, 882.6653442382812, 185.8892059326172, 89.92568969726562)), 
    ('CheckBox', 0.9986904263496399, (257.4203186035156, 896.9129028320312, 304.2779541015625, 77.9148178100586)), 
    ('CheckBox', 0.9999973773956299, (263.3631286621094, 998.8782958984375, 316.2840881347656, 74.91189575195312)),
    ('ListPicker', 0.44274625182151794, (558.7077026367188, 1002.3857421875, 175.06619262695312, 101.78318786621094)), 
    ('Switch', 0.833458662033081, (278.7547302246094, 1109.2235107421875, 349.650390625, 56.834625244140625)), 
    ('Switch', 0.60493004322052, (275.4377746582031, 1191.821044921875, 335.73291015625, 63.245018005371094)), 
    ('ListPicker', 0.560918390750885, (560.1752319335938, 1118.6690673828125, 174.2657012939453, 88.55982971191406)) 
]



image = Image.open(imagePath)
image = image.resize((720, 1280))
image = image.convert('RGB')


draw = ImageDraw.Draw(image)

for component in components:
    [(x0, y0), (x1, y1)] = getCoords(component=component)
    draw.rectangle([(x0, y0), (x1, y1)], fill=None,
                   outline=colorDict[component[0]])
    for delta in [0, 1, -1, 2, -2]:
        draw.rectangle([(x0 - delta, y0 - delta), (x1 + delta, y1 + delta)],
                       fill=None, outline=colorDict[component[0]])

    text_y_compensation = -37
    text_x_compensation = 0

    text_color = (255, 255, 255, 255)
    text_color = colorDict[component[0]]

    text_border_color = (255, 255, 255, 255)
    #text_border_color = (0, 0, 0, 255)

    if text_enable:
        if text_border_enable:
            for delta in [1, -1, ]:
                draw.text((x0 + text_x_compensation + delta, y0 + text_y_compensation),
                          component[0], font=font, fill=text_border_color)
                draw.text((x0 + text_x_compensation, y0 + text_y_compensation +
                           delta), component[0], font=font, fill=text_border_color)
                draw.text((x0 + text_x_compensation + delta, y0 + text_y_compensation +
                           delta), component[0], font=font, fill=text_border_color)
        draw.text((x0 + text_x_compensation, y0 + text_y_compensation),
                  component[0], font=font, fill=text_color)

image.show()
