#coding: utf8
import cv2 #Importa OpenCV
import numpy as np
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk #Para usar combobox
from functools import partial #Para passar widgets como parâmetro nas funções
import math
import threading
from datetime import datetime








#Para detecção de faces e olhos
arqCasc = 'haarcascade_frontalface_default.xml' #Face
#arqCasc = 'haarcascade_eye.xml' #Olhos
faceCascade = cv2.CascadeClassifier(arqCasc)

arqCascOlho = 'haarcascade_eye.xml' #Olhos
olhoCascade = cv2.CascadeClassifier(arqCascOlho)

#Faces

janela = Tk()

def capturarVideo():


    ckGrava["state"] = DISABLED
    e["state"] = DISABLED

    cap = cv2.VideoCapture(0) #Captura da webCam

    cap2 = cv2.VideoCapture('C:\\Users\\jcarl\\Desktop\\Saida.avi') #Captura do arquivo

    #Para gravar em disco
    if (grava.get() == 1):
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        now = datetime.now()  # Pega data e hora e coloca em now
        nome = str(now.minute + now.second)
        out = cv2.VideoWriter('C:\\Users\\jcarl\\Desktop\\Saida_'+nome+'.avi', fourcc, 5.0, (640, 480))

    while True:
        frase = ""  # Texto que apareccerá na tela

        ret, img=cap.read() #Faz a leitura do quadro e guarda em img

        ret2, img2=cap2.read() #Lê do arquivo

        #img2 = cv2.imread('Foto.jpg') #Lê foto tirada pela aplicação

        #Detecção de objetos
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Para usar o Template Map
        template = cv2.imread('C:\\Users\\jcarl\\Desktop\\Modelo.jpg', 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = float(e.get()) #Sensibilidade (depende da qualidade do modelo, mas entre 0.5 e 0.7 já fica razoável)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            if (objeto.get()==1):
                cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 1)  # tenho q contar os retangulos
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "Objeto encontrado", (5,  30), font, 1, (0, 255, 255), 3, cv2.LINE_AA)  # Escreve na tela

        #Fim detecção de objetos

        rows, cols = img.shape[:2] #Pega as dimensões do vídeo

        #img2 = cv2.imread('C:/Users/jcarl/Documents/1 PDI IMG/1 lena.pgm')

        #Detecção de Face
        faces = faceCascade.detectMultiScale(
            img,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(200, 200)
        )

        # Desenha um retângulo nas faces detectadas
        if (face.get() == 1):
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frase = "Deteccao faces"

        # Detecção de Olhos
        olhos = olhoCascade.detectMultiScale(
             img,
             minNeighbors=5,
             minSize=(30, 30),
             maxSize=(200, 200)
         )

        # Desenha um retângulo nos olhos detectadas
        if (olho.get() == 1):
            for (x, y, w, h) in olhos:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            frase = "Deteccao olhos"


        #Executa as oeprações na saida do vídeo conforme a opção selecionada

        #Aritméticas e Lógicas (Estou usando uma imagem capturada no momento da exibição)
        if (soma.get()==1):
            img = img + img2 #soma
            frase = "soma"


        if (sub.get()==1):
            img = img - img2 #subtração
            frase = "subtracao"

        if (mul.get()==1):
            img = img * img2 #multiplicação
            frase = "Multiplicacao"

        if (AND.get() == 1):
            img = img & img2  # AND
            frase = "AND"

        if (OR.get() == 1):
            img = img | img2  # OR
            frase = "OR"

        if (XOR.get() == 1):
            img = img ^ img2  # XOR
            frase = "XOR"

        # Transformação Affine - Geométricas

        # Rotação
        if (rotacao.get() == 1 and lbAngulo["text"] != ""):
            ponto = (rows / 2, cols / 2)  # ponto no centro da figura
            rot = cv2.getRotationMatrix2D(ponto, lbAngulo["text"],
                                          1.0)  # Cria a matriz de rotação (ponto, angulo, amplia ou reduz)
            img = cv2.warpAffine(img, rot, (rows, cols))  # Aplica a rotação
            frase = "Rotacao em  "+str(- lbAngulo["text"])+" graus"

        # Translação
        if (translacao.get() == 1 and lbX["text"] != "" and lbY["text"] != ""):
            M = np.float32([[1, 0, lbX["text"]], [0, 1, lbY["text"]]])  # Cria um kernel {1,0,x,0,1,y}
            img = cv2.warpAffine(img, M, (cols, rows))  # Aplica a transformação
            frase = "Translacao: x = "+str(lbX["text"])+" e Y = "+str(lbY["text"])

        # Reflexão
        if (reflexao.get() == 1 and lbXY["text"] != ""):
            if (lbXY["text"] == 1):
                img = cv2.flip(img, 1)  # 0 para vertical e 1 para horizontal
                frase = "Reflexao horizontal"
            elif (lbXY["text"] == 0):  # Nas duas direções
                img = cv2.flip(img, 0)  # 0 para vertical e 1 para horizontal
                frase = "Reflexao vertical"
            elif (lbXY["text"] == 2):  # Nas duas direções
                img = cv2.flip(img, 0)  # 0 para vertical e 1 para horizontal
                img = cv2.flip(img, 1)  # 0 para vertical e 1 para horizontal
                frase = "Reflexao vertical e horizaontal"


        #Transformações Lineares

       #if (negativo.get() == 1):
        #    img = 255 - img #Negativo
         #   frase = "Negativo"

        if (quadrado.get()==1):
            img = img**2 #Quadrado
            frase = "Quadrado"



        #Filtros

        #Média
        if (media.get() == 1 and lbMedia["text"] != ""):
            img = cv2.blur(img, (int(lbMedia["text"]), int(lbMedia["text"])))  # Aplica filtros
            frase = "Media"

        #Mediana
        if (mediana.get() == 1 and lbMediana["text"] != ""):
            img = cv2.medianBlur(img, int(lbMediana["text"]), img)
            frase = "Mediana"

        if (h1.get() == 1 ):
            M = np.float32([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])  # h1
            img = cv2.filter2D(img, 0, M, img)
            frase = "h1"

        if (h2.get() == 1 ):
            M = np.float32([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])  # h2
            img = cv2.filter2D(img, 0, M, img)
            frase = "h2"

        if (M1.get() == 1 ):
            M = np.float32([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])  # M1
            img = cv2.filter2D(img, 0, M, img)
            frase = "M1"

        if (M2.get() == 1 ):
            M = np.float32([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])  # M2
            img = cv2.filter2D(img, 0, M, img)
            frase = "M2"

        if (M3.get() == 1):
            M = np.float32([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # M3
            img = cv2.filter2D(img, 0, M, img)
            frase = "M3"

        #Detecção de retas

        if (horizontal.get() == 1 ):
            M = np.float32([[-1,-1,-1], [2,2,2], [-1,-1,-1]])  # Horizontal
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Retas horizontais"

        if (vertical.get() == 1 ):
            M = np.float32([[-1,2,-1], [-1,2,-1], [-1,2,-1]])  # Vertical
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Retas verticais"

        if (graus45.get() == 1):
            M = np.float32([[-1,-1,2], [-1,2,-1], [2,-1,-1]])  # 45 Graus
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Retas em 45 Graus"

        if (graus135.get() == 1 ):
            M = np.float32([[2,-1,-1], [-1,2,-1], [-1,-1,2]])  # 135 Graus
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Retas em 135 Graus"



        # Detecção de bordas
        if (robertX.get() == 1):
            M = np.float32([[1,0],[0,-1]])  # Roberts X
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Bordas - Roberts X"

        if (robertY.get() == 1):
            M = np.float32([[0, 1], [-1, 0]])  # Roberts Y
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Bordas - Roberts Y"

        if (robCruzado.get() == 1):
            Mask1 = np.float32([[1, 0], [0, -1]])  # Roberts X
            Mask2 = np.float32([[0, 1], [-1, 0]])  # Roberts Y
            img = cv2.filter2D(img, 0, Mask1, img) + cv2.filter2D(img, 0, Mask2, img)  # Aplica convolução
            frase = "Deteccao de Bordas - Roberts Cruzado"
            #M2 = np.float32([[0, 1], [-1, 0]])  # Roberts Y
            #M = np.float32([[1, 1], [-1, -1]])  # Roberts Cruzado
            #img = cv2.filter2D(img, 0, M, img)  # Aplica convolução

        if (prewittY.get() == 1):
            M = np.float32([[-1,0,1],[-1,0,1],[-1,0,1]])  # Prewitt X
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Bordas - Prewitt Y"

        if (prewittX.get() == 1):
            M = np.float32([[-1,-1,-1],[0,0,0],[1,1,1]])  # Prewitt Y
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Bordas - Prewitt X"


        if (H1.get() == 1 ):
            M = np.float32([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])  # H1
            img = cv2.filter2D(img, 0, M, img)
            frase = "Deteccao de Bordas - H1"

        if (H2.get() == 1 ):
            M = np.float32([[-1, -4,-1], [-4, 20, -4], [-1, -4, -1]])  # H2
            img = cv2.filter2D(img, 0, M, img)  # Aplica convolução
            frase = "Deteccao de Bordas - H2"

        if (laplaciano.get() == 1):
             img = cv2.Laplacian(img,0, img) #Laplaciano
             frase = "Deteccao de Bordas - Laplaciano"

        if (sobelX.get() == 1):
            img  = cv2.Sobel(img,0,0,1,img) #Sobel X
            frase = "Deteccao de Bordas - Sobel X"

        if (sobelY.get() == 1):
            img  = cv2.Sobel(img,0,1,0,img) #Sobel y
            frase = "Deteccao de Bordas - Sobel Y"

        if (canny.get() == 1):
             img = cv2.Canny(img,100,200) #Canny - bordas
             frase = "Deteccao de Bordas - Canny "

        if (negativo.get() == 1):
            img = 255 - img  # Negativo
            frase = "Negativo"

        #Limiarização
        '''
         cv2.THRESH_BINARY
         cv2.THRESH_BINARY_INV
         cv2.THRESH_TRUNC
         cv2.THRESH_TOZERO
         cv2.THRESH_TOZERO_INV
        '''
        if (limiar.get() == 1):
            ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            frase="Limiarizacao Global"


        # Escreve texto na tela
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, frase, (5, 30), font, 1, (0, 255, 255), 3, cv2.LINE_AA)  # Escreve na tela

        if (grava.get() == 1):
            out.write(img) #Escreve a captura da camera no arquivo de saida

        cv2.imshow("Video", img) #Exibe imagem


        k = cv2.waitKey(30) & 0xff #Aguarda

        if (k == 32):
            now = datetime.now() #Pega data e hora e coloca em now
            x = str(now.minute + now.second)
            cv2.imwrite("C:\\Users\\jcarl\\Desktop\\Foto_"+x+".jpg", img)

        if k == 27:
            ckGrava["state"] = NORMAL
            e["state"] = NORMAL
            break

    cap.release()

    if (grava.get() == 1):
        out.release()

    cv2.destroyAllWindows()

    #cropped = img[70:170, 440:540] #Recorta parte da imagem


    cv2.waitKey(0)




video = threading.Thread( target=capturarVideo)


def pegaAngulo():
    if(rotacao.get()==1):
        lbAngulo["text"] =""
        lbAngulo["text"] = - simpledialog.askfloat("Rotação", "Informe o ângulo")

def pegaTranslacao():
    if(translacao.get()==1):
        lbX["text"] =""
        lbY["text"] = ""
        lbX["text"] =  simpledialog.askfloat("Translação", "Informe X")
        lbY["text"] =  simpledialog.askfloat("Rotação", "Informe Y")

def pegaReflexao():
    if(reflexao.get()==1):
        lbXY["text"] =""
        lbXY["text"] = simpledialog.askfloat("Reflexão", "Informe a direção [ 0 - V   1 - H  2 - VH ]")

def pegaMedia():
    if(media.get()==1):
        lbMedia["text"] =""
        lbMedia["text"] = simpledialog.askfloat("Média", "Informe o tamanho da máscara (ex: 3)")

def pegaMediana():
    if(mediana.get()==1):
        lbMediana["text"] =""
        lbMediana["text"] = simpledialog.askfloat("Mediana", "Informe o tamanho da máscara (ex: 3)")

def mensagem():
    if (objeto.get() == 1):
        texto = "Para usar essa função você deve abrir o vídeo, mostrar o objeto que deseja identificar e salvar a imagem como Modelo.jpg"
        simpledialog.messagebox.showinfo("Atenção!", texto)
        e["state"] = NORMAL
    else:
        e["state"] = DISABLED
    if (grava.get() == 1):
        texto = "O arquivo será salvo em: Desktop"
        simpledialog.messagebox.showinfo("Atenção!", texto)


#Desenha componentes da janela e define as variáveis que serão usadas para as funções de manipulação de imagens
janela.geometry("700x450+350+10")  # Tamanho da janela principal da aplicação
janela.title("Processamento de Vídeos com Pytohn e Opencv")
Label(janela, text="Marque as opções que deseja processar", bg="silver").pack()

#Labels para pegar valores
lbAngulo = Label(janela, text="") #Rotação
#translação
lbX = Label(janela, text="")
lbY = Label(janela, text="")
#Reflexão
lbXY = Label(janela, text="")
#Media
lbMedia = Label(janela, text="")
#Mediana
lbMediana = Label(janela, text="")
#Sensibilidade
lbsensibilidade = Label(janela, text="")

#Fim Labels para pegar valores


#Botão para abertura do vídeo
btVideo = Button(janela, text="Abrir vídeo", command=video.start) #Botão chama a Thread
#btVideo["command"] = partial(capturarVideo, btVideo)
btVideo.place(x=10, y=5)


#Checkbox Gravação
grava = IntVar()
ckGrava = Checkbutton(janela, text="Gravar Resultado", variable=grava, command=mensagem)
ckGrava.place(x=100, y=5)

#Checkbuttons com as opções de manipulação

#Aritméticas
lbArt = Label(janela, text="Operações Aritméicas e Lógicas", bg="yellow")
lbArt.place(x=10, y=30)

#soma
soma = IntVar()
ckSoma = Checkbutton(janela, text="Soma", variable=soma)
ckSoma.place(x=10, y=50)

#subtração
sub = IntVar()
ckSub = Checkbutton(janela, text="Subração", variable=sub)
ckSub.place(x=10, y=70)

#Multiplicação
mul = IntVar()
ckMul = Checkbutton(janela, text="Multiplicação", variable=mul)
ckMul.place(x=10, y=90)

#AND
AND = IntVar()
ckAnd = Checkbutton(janela, text="AND", variable=AND)
ckAnd.place(x=10, y=110)

#OR
OR = IntVar()
ckOR = Checkbutton(janela, text="OR", variable=OR)
ckOR.place(x=10, y=130)

#XOR
XOR = IntVar()
ckXor = Checkbutton(janela, text="XOR", variable=XOR)
ckXor.place(x=10, y=150)

#Geométricas
lbArt = Label(janela, text="Transformações Geométricas", bg="yellow")
lbArt.place(x=210, y=30)

#Rotação
rotacao = IntVar()
ckRotacao = Checkbutton(janela, text="Rotação", variable=rotacao, command=pegaAngulo)
ckRotacao.place(x=210, y=50)

#Translação
translacao = IntVar()
ckTrans = Checkbutton(janela, text="Translação", variable=translacao, command=pegaTranslacao)
ckTrans.place(x=210, y=70)

#Reflexão
reflexao = IntVar()
ckRef = Checkbutton(janela, text="Reflexão", variable=reflexao, command=pegaReflexao)
ckRef.place(x=210, y=90)

#Lineares e não-lineares
lbArt = Label(janela, text="Transformações Lineares e não-lineares", bg="yellow")
lbArt.place(x=210, y=110)

#Negativo
negativo  = IntVar()
ckNegativo = Checkbutton(janela, text="Negativo", variable=negativo)
ckNegativo.place(x=210, y=130)

#Quadrado
quadrado = IntVar()
ckQuad = Checkbutton(janela, text="Quadrado", variable=quadrado)
ckQuad.place(x=210, y=150)

#Filtros
lbArt = Label(janela, text="Filtros (passa-baixas e passa-altas)", bg="yellow")
lbArt.place(x=450, y=30)

#média
media = IntVar()
ckMedia = Checkbutton(janela, text="Média", variable=media, command=pegaMedia)
ckMedia.place(x=450, y=50)

#mediana
mediana = IntVar()
ckMediana = Checkbutton(janela, text="Mediana", variable=mediana, command=pegaMediana)
ckMediana.place(x=450, y=70)

#h1
h1 = IntVar()
ckH1 = Checkbutton(janela, text="h1", variable=h1)
ckH1.place(x=550, y=50)

#h2
h2 = IntVar()
ckH2 = Checkbutton(janela, text="h2", variable=h2)
ckH2.place(x=550, y=70)

#M1
M1 = IntVar()
ckM1 = Checkbutton(janela, text="M1", variable=M1)
ckM1.place(x=600, y=50)

#M2
M2 = IntVar()
ckM2 = Checkbutton(janela, text="M2", variable=M2)
ckM2.place(x=600, y=70)

#M3
M3 = IntVar()
ckM3 = Checkbutton(janela, text="M3", variable=M3)
ckM3.place(x=650, y=50)

#Detecção de Retas
lbArt = Label(janela, text="Detecção de Retas", bg="yellow")
lbArt.place(x=450, y=90)

#Horizontal
horizontal = IntVar()
ckHorizontal = Checkbutton(janela, text="Horizontal", variable=horizontal)
ckHorizontal.place(x=450, y=110)

#Vertical
vertical = IntVar()
ckVertical = Checkbutton(janela, text="Vertical", variable=vertical)
ckVertical.place(x=450, y=130)

#45 Graus
graus45 = IntVar()
ck45Graus = Checkbutton(janela, text="45 Graus", variable=graus45)
ck45Graus.place(x=450, y=150)

#135 Graus
graus135 = IntVar()
ck135Graus = Checkbutton(janela, text="135 Graus", variable=graus135)
ck135Graus.place(x=550, y=110)


#Detecção de Brodas
lbArt = Label(janela, text="Detecção de Bordas", bg="yellow")
lbArt.place(x=10, y=180)

#Roberts X
robertX = IntVar()
ckRobX = Checkbutton(janela, text="Roberts X", variable=robertX)
ckRobX.place(x=10, y=200)

#Roberts Y
robertY = IntVar()
ckRobY = Checkbutton(janela, text="Roberts Y", variable=robertY)
ckRobY.place(x=10, y=220)

#Roberts Cruzado
robCruzado = IntVar()
ckRbCruzado = Checkbutton(janela, text="Roberts Cruzado", variable=robCruzado)
ckRbCruzado.place(x=10, y=240)

#Prewitt X
prewittX = IntVar()
ckPwX = Checkbutton(janela, text="Prewitt X", variable=prewittX)
ckPwX.place(x=10, y=260)

#Prewitt Y
prewittY = IntVar()
ckPwY = Checkbutton(janela, text="Prewitt Y", variable=prewittY)
ckPwY.place(x=10, y=280)

#H1
H1 = IntVar()
ck_H1 = Checkbutton(janela, text="H1", variable=H1)
ck_H1.place(x=10, y=300)

#H2
H2 = IntVar()
ck_H2 = Checkbutton(janela, text="H2", variable=H2)
ck_H2.place(x=10, y=320)

#Laplacianno
laplaciano = IntVar()
ck_Lap = Checkbutton(janela, text="Laplaciano", variable=laplaciano)
ck_Lap.place(x=10, y=340)

#SobelX
sobelX = IntVar()
ck_SBX = Checkbutton(janela, text="Sobel X", variable=sobelX)
ck_SBX.place(x=10, y=360)

#SobelY
sobelY = IntVar()
ck_SBY = Checkbutton(janela, text="Sobel Y", variable=sobelY)
ck_SBY.place(x=10, y=380)

#Canny
canny= IntVar()
ck_CNY = Checkbutton(janela, text="Canny", variable=canny)
ck_CNY.place(x=10, y=400)

#Detecção de face e olhos
lbArt = Label(janela, text="Detecção e Reconhecimento", bg="yellow")
lbArt.place(x=210, y=180)

#Face
face = IntVar()
ckFace = Checkbutton(janela, text="Faces", variable=face)
ckFace.place(x=210, y=200)

#Olho
olho = IntVar()
ckOlho = Checkbutton(janela, text="Olhos", variable=olho)
ckOlho.place(x=210, y=220)

#Objeto (o ojbeto deve estar contido na imagem Modelo.jpg) - Tirar print do objeto e salvar a imagem modelo
objeto = IntVar()
ckObjeto = Checkbutton(janela, text="Objeto", variable=objeto, command=mensagem)
ckObjeto.place(x=210, y=240)

lbEdt = Label(janela, text="-> Sensibilidade", bg="silver")
lbEdt.place(x=280, y=240)

#Campo de entrada para a sensibilidade
v = StringVar(janela, value='0.6')
e = Entry(janela, width=5, state=DISABLED, textvariable=v)
e.place(x=380, y=240)

#Segmentação
lbArt = Label(janela, text="Segmentação", bg="yellow")
lbArt.place(x=450, y=180)

#Limiarização
limiar = IntVar()
ckLimiar= Checkbutton(janela, text="Limiarização Global", variable=limiar)
ckLimiar.place(x=450, y=200)


#Créditos
lbCredito1 = Label(janela, text="UFERSA - Universidade Rural Federal do Semi-Árido ")
lbCredito2 = Label(janela, text="Disciplina: Processamento Digital de Imagens - PDI ")
lbCredito3 = Label(janela, text="Aluno: José Carlos da Silva")
lbCredito1.place(x=400, y=360)
lbCredito2.place(x=400, y=380)
lbCredito3.place(x=400, y=400)



janela.mainloop()


