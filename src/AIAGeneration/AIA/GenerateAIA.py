import json
import os
from zipfile import ZipFile
from . import AIAProject


def generateAIAJson(screen: AIAProject.Screen):
    return convertJson(json.dumps(screen.toDict()))


def convertJson(originalJson):
    return \
        '#|\n' + \
        '$JSON\n' + \
        originalJson + '\n' \
                       '|#'


def saveFile(projectPath: str, project: AIAProject.Project):
    savePath = os.path.join(projectPath, project.AppName + '.aia')

    with ZipFile(savePath, 'w') as myzip:
        with myzip.open("youngandroidproject/project.properties", 'w') as project_properties_file:
            project_properties_file.write(bytes(project.genProperties(), 'utf-8'))
        for Screen in project.Screens:
            with myzip.open('src/appinventor/sketch2aia/' + project.AppName + '/' + Screen.Name + '.scm',
                            'w') as screenScmFile:
                screenScmFile.write(bytes(generateAIAJson(Screen), 'utf-8'))
            with myzip.open('src/appinventor/sketch2aia/' + project.AppName + '/' + Screen.Name + '.bky',
                            'w') as screenBkyFile:
                screenBkyFile.write(bytes('', 'utf-8'))