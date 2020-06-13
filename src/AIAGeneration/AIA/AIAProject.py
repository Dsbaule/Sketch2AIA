import uuid
import random

class Project:
    def __init__(self, AppName):
        self.authURL = ["ai2.appinventor.mit.edu"]
        self.YaVersion = 206
        self.Source = "Form"
        self.AppName = AppName
        self.main = None
        self.Screens = list()

        self.countDict = {
            'VerticalArrangement':      1,
            'HorizontalArrangement':    1,
            'Label':        1,
            'Button':       1,
            'TextBox':      1,
            'CheckBox':     1,
            'Image':        1,
            'Switch':       1,
            'Slider':       1,
            'Map':          1,
            'ListPicker':   1,
            'Spinner':      1
        }

        self.defaultNames = {
            'VerticalArrangement':      'OrganizacaoVertical',
            'HorizontalArrangement':    'OrganizacaoHorizontal',
            'Label':        'Legenda',
            'Button':       'Botao',
            'TextBox':      'CaixaDeTexto',
            'CheckBox':     'CaixaDeSelecao',
            'Image':        'Imagem',
            'Switch':       'Interruptor',
            'Slider':       'Deslizador',
            'Map':          'Mapa',
            'ListPicker':   'EscolheLista',
            'Spinner':      'ListaSuspensa'
        }

    def addScreen(self, screen):
        if self.main is None:
            self.main = screen.Name
        self.Screens.append(screen)

    def genProperties(self):
        return 'main=appinventor.ai_sketch2AIA.' + self.AppName + '.' + self.main + '\n' +\
               'name=' + self.AppName + '\n' +\
               'assets=../assets\n' +\
               'source=../src\n' +\
               'build=../build\n' +\
               'versioncode=1\n' +\
               'versionname=1.0\n' +\
               'useslocation=False\n' +\
               'aname=' + self.AppName + '\n' +\
               'sizing=Responsive\n' +\
               'showlistsasjson=True\n' +\
               'actionbar=False\n' +\
               'theme=Classic\n' +\
               'color.primary=&HFF3F51B5\n' +\
               'color.primary.dark=&HFF303F9F\n' +\
               'color.accent=&HFFFF4081'

class Screen:
    def __init__(self, Name, project):
        self.project = project
        self.Name = Name
        self.Type = "Form"
        self.Version = "27"
        self.Title = Name
        self.Uuid = 0
        self.Components = list()

    def addComponent(self, Component):
        self.Components.append(Component)

    def toDict(self):
        return {
            "authURL": self.project.authURL,
            "YaVersion": str(self.project.YaVersion),
            "Source": self.project.Source,
            "Properties": {
                "$Name": self.Name,
                "$Type": self.Type,
                "$Version": str(self.Version),
                "AppName": self.project.AppName,
                "Title": self.Title,
                "Uuid": str(self.Uuid),
                "$Components": [x.toDict() for x in self.Components]
            }
        }


class Component:
    def __init__(self, Name, Type, Version, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1):
        self.Name = Name
        self.Type = Type
        self.Version = Version
        self.AlignHorizontal = AlignHorizontal
        self.AlignVertical = AlignVertical
        self.Height = Height
        self.Width = Width
        self.Uuid = random.randint(-9999999999, 9999999999)

    def toDict(self):
        return {
            "$Name": self.Name,
            "$Type": self.Type,
            "$Version": str(self.Version),
            "AlignHorizontal": str(self.AlignHorizontal),
            "AlignVertical": str(self.AlignVertical),
            "Height": str(self.Height),
            "Width": str(self.Width),
            "Uuid": str(self.Uuid)
        }

class TextComponent(Component):
    def __init__(self, Name, Type, Version, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Text=""):
        self.Text = Text
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)

    def toDict(self):
        return {
            "$Name": self.Name,
            "$Type": self.Type,
            "$Version": str(self.Version),
            "AlignHorizontal": str(self.AlignHorizontal),
            "AlignVertical": str(self.AlignVertical),
            "Height": str(self.Height),
            "Width": str(self.Width),
            "Uuid": str(self.Uuid),
            "Text": self.Text
        }

class HintComponent(Component):
    def __init__(self, Name, Type, Version, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Hint=""):
        self.Hint = Hint
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)

    def toDict(self):
        return {
            "$Name": self.Name,
            "$Type": self.Type,
            "$Version": str(self.Version),
            "AlignHorizontal": str(self.AlignHorizontal),
            "AlignVertical": str(self.AlignVertical),
            "Height": str(self.Height),
            "Width": str(self.Width),
            "Uuid": str(self.Uuid),
            "Hint": self.Hint
        }


class Arrangement(Component):
    def __init__(self, Name, Type, Version, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Components=None):
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)
        self.Components = list() if Components is None else Components

    def addComponent(self, component):
        self.Components.append(component)

    def toDict(self):
        return {
            "$Name": self.Name,
            "$Type": self.Type,
            "$Version": str(self.Version),
            "AlignHorizontal": str(self.AlignHorizontal),
            "AlignVertical": str(self.AlignVertical),
            "Height": str(self.Height),
            "Width": str(self.Width),
            "Uuid": str(self.Uuid),
            "$Components": [x.toDict() for x in self.Components]
        }

class HorizontalArrangement(Arrangement):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Components=None):
        Type = "HorizontalArrangement"
        Version = "3"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Components)


class VerticalArrangement(Arrangement):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Components=None):
        Type = "VerticalArrangement"
        Version = "3"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Components)


class Button(TextComponent):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Text="Button"):
        Type = "Button"
        Version = "6"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Text)


class TextBox(HintComponent):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Hint="TextBox"):
        Type = "TextBox"
        Version = "6"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Hint)


class Label(TextComponent):
    def __init__(self, Name: str, AlignHorizontal: int = 1, AlignVertical: int = 1, Height: int = -1, Width: int = -1, Text="Label") -> Component:
        Type = "Label"
        Version = "5"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Text)


class Switch(TextComponent):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Text="Switch"):
        Type = "Switch"
        Version = "1"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Text)


class Slider(Component):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1):
        Type = "Slider"
        Version = "2"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)


class Map(Component):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1):
        Type = "Map"
        Version = "5"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)


class CheckBox(TextComponent):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Text='CheckBox'):
        Type = "CheckBox"
        Version = "2"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Text)


class Image(Component):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1):
        Type = "Image"
        Version = "4"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)


class Spinner(Component):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1):
        Type = "Spinner"
        Version = "1"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width)


class ListPicker(TextComponent):
    def __init__(self, Name, AlignHorizontal=1, AlignVertical=1, Height=-1, Width=-1, Text="ListPicker"):
        Type = "ListPicker"
        Version = "9"
        super().__init__(Name, Type, Version, AlignHorizontal, AlignVertical, Height, Width, Text)