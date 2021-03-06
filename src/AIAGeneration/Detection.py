from src.AIAGeneration.Darknet import darknet
from src.AIAGeneration.Component import Component
from src.AIAGeneration import Alignment
from src.AIAGeneration.AIA import AIAProject, GenerateAIA

import os
from PIL import Image

from src.AIAGeneration.Draw import save_preview

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DARKNET_ROOT = os.path.join(APP_ROOT, 'Darknet')

configPath = os.path.join(DARKNET_ROOT, 'NewDatasetYolov3.cfg')
weightPath = os.path.join(DARKNET_ROOT, 'NewDatasetYolov3_18000.weights')
metaPath = os.path.join(DARKNET_ROOT, 'obj.data')


def generateArrangement(alignment: tuple, curProj: AIAProject.Project, depth=0, listType=0) -> AIAProject.Arrangement:
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
            curArrangement.addComponent(generateArrangement(curComponent, curProj, depth + 1, listType))
        elif curComponent.label == 'Label':
            curArrangement.addComponent(AIAProject.Label(Name=(defaultNames['Label'] + str(countDict['Label']))))
            countDict['Label'] += 1
        elif curComponent.label == 'Button':
            curArrangement.addComponent(AIAProject.Button(Name=(defaultNames['Button'] + str(countDict['Button']))))
            countDict['Button'] += 1
        elif curComponent.label == 'TextBox':
            curArrangement.addComponent(AIAProject.TextBox(Name=(defaultNames['TextBox'] + str(countDict['TextBox']))))
            countDict['TextBox'] += 1
        elif curComponent.label == 'CheckBox':
            curArrangement.addComponent(
                AIAProject.CheckBox(Name=(defaultNames['CheckBox'] + str(countDict['CheckBox']))))
            countDict['CheckBox'] += 1
        elif curComponent.label == 'Image':
            curArrangement.addComponent(AIAProject.Image(Name=(defaultNames['Image'] + str(countDict['Image']))))
            countDict['Image'] += 1
        elif curComponent.label == 'Switch':
            curArrangement.addComponent(AIAProject.Switch(Name=(defaultNames['Switch'] + str(countDict['Switch']))))
            countDict['Switch'] += 1
        elif curComponent.label == 'Slider':
            curArrangement.addComponent(AIAProject.Slider(Name=(defaultNames['Slider'] + str(countDict['Slider']))))
            countDict['Slider'] += 1
        elif curComponent.label == 'Map':
            curArrangement.addComponent(AIAProject.Map(Name=(defaultNames['Map'] + str(countDict['Map']))))
            countDict['Map'] += 1
        elif curComponent.label == 'ListPicker':
            if listType == 0:
                curArrangement.addComponent(
                    AIAProject.ListPicker(Name=(defaultNames['ListPicker'] + str(countDict['ListPicker']))))
                countDict['ListPicker'] += 1
            else:
                curArrangement.addComponent(
                    AIAProject.Spinner(Name=(defaultNames['Spinner'] + str(countDict['ListPicker']))))
                countDict['Spinner'] += 1
    return curArrangement


def detect(projectPath, sketchList, mainScreen=0, projectName='MyProject',listType=0):

    project = AIAProject.Project(AppName=projectName)

    for sketchIndex in range(len(sketchList)):

        imagePath   = os.path.join(projectPath, 'original', sketchList[sketchIndex])
        previewPath = os.path.join(projectPath, 'preview', sketchList[sketchIndex])

        result = darknet.performDetect(
            imagePath=imagePath,
            thresh=0.25,
            configPath=configPath,
            weightPath=weightPath,
            metaPath=metaPath,
            showImage=False,
            makeImageOnly=True,
            initOnly=False)

        '''
        Image.fromarray(result['image']).save(previewPath)
        result = result['detections']
        '''

        componentList = list()

        for component in result:
            if component[0] == 'Screen':
                screen = Component(component[0], component[1], component[2][0], component[2][1], component[2][2], component[2][3])
            else:
                componentList.append(Component(component[0], component[1], component[2][0], component[2][1], component[2][2], component[2][3]))

        # Remove overlaps
        i = 0
        while i < (len(componentList) - 1):
            j = i + 1

            while j < len(componentList):
                if componentList[i].overlaps(componentList[j]):
                    if componentList[i].confidence < componentList[j].confidence:
                        componentList.pop(i)
                        i -= 1
                        break
                    else:
                        componentList.pop(j)
                else:
                    j += 1    
                        
            i += 1

        # Generate and save preview
        save_preview(imagePath, componentList + [screen], previewPath)

        #print(str(Alignment.align(componentList)))

        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(Alignment.align(componentList))

        alignedComponents = Alignment.align(componentList)

        screen = AIAProject.Screen('Screen' + str(sketchIndex + 1), project)
        project.addScreen(screen)
        if sketchIndex == mainScreen:
            project.main = 'Screen' + str(sketchIndex + 1)
        screen.addComponent(generateArrangement(alignedComponents, project, listType=listType))

    GenerateAIA.saveFile(projectPath, project)


