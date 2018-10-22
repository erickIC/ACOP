def calculo_normalizacao(x, min, max, rangea, rangeb):
	
	z = ( (float(rangeb) - float(rangea)) * ( (x - float(min))/(float(max) - float(min)) ) ) + float(rangea)
	return z

mascara = open('mascara1.txt', 'r')
escrito = open('testew.txt', 'w')

potencias = mascara.readlines()

canal = []
canal_float = []

maior_pintotal = -float('inf')
maior_gset = -float('inf')
maior_wave = -float('inf')
maior_gch = -float('inf')
maior_nf = -float('inf')

menor_pintotal = float('inf')
menor_gset = float('inf')
menor_wave = float('inf')
menor_gch = float('inf')
menor_nf = float('inf')

rangea = float(0.15)
rangeb = float(0.85)

total_canais = int(potencias[0])


for i in range(1, len(potencias)):

	canais = potencias[i].split()

	for j in range(0, total_canais):
						 #Pintotal               Gset					wave									Gch         Pout                     Pin                          						NF

		canal_float.append([float(canais[0]), float(canais[2]), float(canais[3 + (3*total_canais) + j]), float(float(canais[3 + total_canais + j]) - float(canais[3 + j])), float(canais[3 + (2*total_canais) + j])])

		if float(canais[0]) > maior_pintotal:
			maior_pintotal = float(canais[0])

		if float(canais[0]) < menor_pintotal:
			menor_pintotal = float(canais[0])

		if 	float(canais[2]) > maior_gset:
			maior_gset = float(canais[2])

		if float(canais[2]) < menor_gset:
			menor_gset = float(canais[2])

		if float(canais[3 + (3*total_canais) + j]) > maior_wave:
			maior_wave = float(canais[3 + (3*total_canais) + j])

		if float(canais[3 + (3*total_canais) + j]) < menor_wave:
			menor_wave = float(canais[3 + (3*total_canais) + j])

		if float(float(canais[3 + total_canais + j]) - float(canais[3 + j])) > maior_gch:
			maior_gch = float(float(canais[3 + total_canais + j]) - float(canais[3 + j]))

		if float(float(canais[3 + total_canais + j]) - float(canais[3 + j])) < menor_gch:
			menor_gch = float(float(canais[3 + total_canais + j]) - float(canais[3 + j]))

		if 	float(canais[3 + (2*total_canais) + j]) > maior_nf:
			maior_nf = float(canais[3 + (2*total_canais) + j])

		if float(canais[3 + (2*total_canais) + j]) < menor_nf:
			menor_nf = float(canais[3 + (2*total_canais) + j])						


#print(maior_pintotal, menor_pintotal, maior_gset, menor_gset, maior_wave, menor_wave, maior_gch, menor_gch, maior_nf, menor_nf)
#print(canal_float[1][1])

maximos = [maior_pintotal, maior_gset, maior_wave, maior_gch, maior_nf]
minimos = [menor_pintotal, menor_gset, menor_wave, menor_gch, menor_nf]
#print(maximos)
#print(minimos)
#print(canal_float[1])
for i in range(0, len(canal_float)):
	atual = canal_float[i]

	for j in range(0, len(atual)):
		atual[j] = calculo_normalizacao(atual[j], minimos[j], maximos[j], rangea, rangeb)

	canal_float[i] = atual	
		

#print(canal_float[1])

for i in range(0, len(canal_float)):

	canal.append(str(canal_float[i][0]) + ' ' + str(canal_float[i][1])  + ' ' + str(canal_float[i][2]) + ' ' + str(canal_float[i][3]) + ' ' + str(canal_float[i][4]) + '\n')

escrito.writelines(canal)

mascara.close()
escrito.close()