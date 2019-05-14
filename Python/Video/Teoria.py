

a=2 #Não foi declarado nenhum tipo para a variável
b=3
c=a+b

print("A variável c é inteira aqui porquê recebeu uma soma de inteiros - TIPAGEM DINÂMICA: %i" %c)

c="a variável c agora recebeu uma string"
print(c)

if (a==2):
    print(c) #A indentação coloca essa instrução dentro do IF
    print("Estou dentro do bloco IF")

print("Sai do bloco IF pois a indentação demarca os blocos de instrução")
