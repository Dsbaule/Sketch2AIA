from src.AIA import AIAProject
from src.AIA import GenerateAIA

project = AIAProject.Project(AppName='TestGeneration')

screen1 = AIAProject.Screen('Screen1', project)
project.addScreen(screen1)

OrganizacaoVertical1 = AIAProject.VerticalArrangement('OrganizacaoVertical', AlignHorizontal=3, Height=-2, Width=-2)
screen1.addComponent(OrganizacaoVertical1)

Legenda1 = AIAProject.Label(Name='Legenda1', Width=-2)
OrganizacaoVertical1.addComponent(Legenda1)

OrganizacaoHorizontal1 = AIAProject.HorizontalArrangement(Name='OrganizaçãoHorizontal1', AlignHorizontal=3, Width=-2)
OrganizacaoVertical1.addComponent(OrganizacaoHorizontal1)

Image1 = AIAProject.Image(Name='Imagem1', Width=-2)
OrganizacaoHorizontal1.addComponent(Image1)

OrganizacaoVertical2 = AIAProject.VerticalArrangement(Name="OrganizacaoVertical2", Width=-2)
OrganizacaoHorizontal1.addComponent(OrganizacaoVertical2)

Map = AIAProject.Map('Map1')
OrganizacaoVertical1.addComponent(Map)

EscolheLista1 = AIAProject.ListPicker('ListaSuspensa1')
OrganizacaoVertical1.addComponent(EscolheLista1)

ListaSuspensa1 = AIAProject.Spinner('ListaSuspensa1')
OrganizacaoVertical1.addComponent(ListaSuspensa1)

Switch1 = AIAProject.Switch('Switch1', Width=-1, Text="TESTE DA STRING")
OrganizacaoVertical1.addComponent(Switch1)

Button1 = AIAProject.Button('Botao1', Text="TEXTO TESTE")
OrganizacaoVertical1.addComponent(Button1)

CheckBox1 = AIAProject.CheckBox('CaixaDeSelecao1', Width=-2, Text="UHU")
OrganizacaoVertical1.addComponent(CheckBox1)

Slider1 = AIAProject.Slider('Slider1', Width=-2)
OrganizacaoVertical1.addComponent(Slider1)

TextBox1 = AIAProject.TextBox('TextBox1', Width=-2, Hint="Hint tambem funciona")
OrganizacaoVertical1.addComponent(TextBox1)

import json
print(json.dumps(screen1.toDict()))
print(project.genProperties())

GenerateAIA.saveFile(project)




