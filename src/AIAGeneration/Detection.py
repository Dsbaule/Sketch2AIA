from src.AIAGeneration.Darknet import darknet
from src.AIAGeneration.Component import Component
from src.AIAGeneration import Alignment
from src.AIAGeneration.AIA import AIAProject, GenerateAIA

import os
from PIL import Image

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DARKNET_ROOT = os.path.join(APP_ROOT, 'Darknet')

configPath = os.path.join(DARKNET_ROOT, 'NewDatasetYolov3.cfg')
weightPath = os.path.join(DARKNET_ROOT, 'NewDatasetYolov3_18000.weights')
metaPath = os.path.join(DARKNET_ROOT, 'obj.data')


def generateArrangement(alignment: tuple, curProj: AIAProject.Project, depth=0) -> AIAProject.Arrangement:
    defaultNames = curProj.defaultNames
    countDict = curProj.countDict

    (alignment, components) = alignment
    if alignment == 'vertical':
        curArrangement = AIAProject.VerticalArrangement(
            Name=(defaultNames['VerticalArrangement'] + str(countDict['VerticalArrangement'])),
            Height=(-2 if depth is 0 else -1), Width=(-2 if depth is 0 else -1),
            AlignHorizontal=(3 if depth is 0 else 1), )
        countDict['VerticalArrangement'] += 1
    elif alignment == 'horizontal':
        curArrangement = AIAProject.HorizontalArrangement(
            Name=(defaultNames['HorizontalArrangement'] + str(countDict['HorizontalArrangement'])))
        countDict['HorizontalArrangement'] += 1
    else:
        raise Exception('Invalid alignment')

    for curComponent in components:
        if type(curComponent) == tuple:
            curArrangement.addComponent(generateArrangement(curComponent, curProj, depth + 1))
        elif curComponent.label == 'Label':
            curArrangement.addComponent(AIAProject.Label(Name=(defaultNames['Label'] + str(countDict['Label']))))
        elif curComponent.label == 'Button':
            curArrangement.addComponent(AIAProject.Button(Name=(defaultNames['Button'] + str(countDict['Button']))))
        elif curComponent.label == 'TextBox':
            curArrangement.addComponent(AIAProject.TextBox(Name=(defaultNames['TextBox'] + str(countDict['TextBox']))))
        elif curComponent.label == 'CheckBox':
            curArrangement.addComponent(
                AIAProject.CheckBox(Name=(defaultNames['CheckBox'] + str(countDict['CheckBox']))))
        elif curComponent.label == 'Image':
            curArrangement.addComponent(AIAProject.Image(Name=(defaultNames['Image'] + str(countDict['Image']))))
        elif curComponent.label == 'Switch':
            curArrangement.addComponent(AIAProject.Switch(Name=(defaultNames['Switch'] + str(countDict['Switch']))))
        elif curComponent.label == 'Slider':
            curArrangement.addComponent(AIAProject.Slider(Name=(defaultNames['Slider'] + str(countDict['Slider']))))
        elif curComponent.label == 'Map':
            curArrangement.addComponent(AIAProject.Map(Name=(defaultNames['Map'] + str(countDict['Map']))))
        elif curComponent.label == 'ListPicker':
            curArrangement.addComponent(
                AIAProject.ListPicker(Name=(defaultNames['ListPicker'] + str(countDict['ListPicker']))))
        elif curComponent.label == 'Spinner':
            curArrangement.addComponent(AIAProject.Spinner(Name=(defaultNames['Spinner'] + str(countDict['Spinner']))))
    return curArrangement


def detect(projectPath, sketchList, mainScreen=0, projectName='MyProject'):

    project = AIAProject.Project(AppName=projectName)

    for sketchIndex in range(len(sketchList)):

        result = darknet.performDetect(
            imagePath=os.path.join(projectPath, 'original', sketchList[sketchIndex]),
            thresh=0.25,
            configPath=configPath,
            weightPath=weightPath,
            metaPath=metaPath,
            showImage=True,
            makeImageOnly=True,
            initOnly=False)

        previewPath = os.path.join(projectPath, 'preview', sketchList[sketchIndex])
        Image.fromarray(result['image']).save(previewPath)

        result = result['detections']

        componentList = list()

        for component in result:
            print(component[0])
            if component[0] == 'Screen':
                screen = Component(component[0], component[1], component[2][0], component[2][1], component[2][2], component[2][3])
            else:
                componentList.append(Component(component[0], component[1], component[2][0], component[2][1], component[2][2], component[2][3]))

        # Remove overlaps
        for i in range(len(componentList) - 1):
            for j in range(i + 1, len(componentList)):
                if componentList[i].overlaps(componentList[j]):
                    componentList.pop(i if (componentList[i].confidence < componentList[j].confidence) else j)


        # Check what components are aligned in each axis
        componentList.sort(key=lambda x: x.y1)
        for i in range(len(componentList)):
            print(componentList[i].label + '(' + str(componentList[i].x1) + ',' + str(componentList[i].y1) + ')')
            componentList[i].getInLineComponents(componentList[i+1:])

        #print(str(Alignment.align(componentList)))

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(Alignment.align(componentList))

        alignedComponents = Alignment.align(componentList)

        screen = AIAProject.Screen('Screen' + str(sketchIndex + 1), project)
        project.addScreen(screen)
        if sketchIndex == mainScreen:
            project.main = 'Screen' + str(sketchIndex + 1)
        screen.addComponent(generateArrangement(alignedComponents, project))

    print('\nJSON:\n')
    import json
    print(json.dumps(screen.toDict()))

    GenerateAIA.saveFile(projectPath, project)


