#Ler as informações da mascara, separar por canais.
# IN (Pintotal, Gset e wave) OUT(Gch(Pout - Pin) NF)
#N - linhas temos um laço para os Total de canais com [Ptotal(0)], [Gset(2)], [wave(3 + 3*Tch + curr)], [Pout[3 + Tch + Curr] - Pin[3 + Curr]] e [NF[3 + 2Tch +Curr]]

mascara = open('mascara1.txt', 'r')
escrito = open('testew.txt', 'w')

potencias = mascara.readlines()
canal = []
Total_canais = int(potencias[0])

for i in range(1, len(potencias)):

	canais = potencias[i].split()

	for j in range(0, Total_canais):
						 #Pintotal               Gset					wave									Gch         Pout                     Pin                          						NF
		canal.append(str(canais[0]) + ' ' + str(canais[2]) + ' ' + str(canais[3 + (3*Total_canais) + j]) + ' ' + str(float(canais[3 + Total_canais + j]) - float(canais[3 + j])) + ' ' + str(canais[3 + (2*Total_canais) + j]) + '\n')


escrito.writelines(canal)

mascara.close()
escrito.close()