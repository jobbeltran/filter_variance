import cv2
import numpy as np 
import sys
import matplotlib.pyplot as plt

def umbral_varianza(data):
	arr=data
	corte=0
	while True:
		corte+=1
		intensidades=[]
		pi=[]
		for i in range(256):
			intensidades.append(0)
			pi.append(0)
		n=0
		for i in range(arr.shape[0]):
			for j in range(arr.shape[1]):
				intensidades[arr.item(i,j)]=intensidades[arr.item(i,j)]+1
				n+=1

		pitotal=0.0
		pi_zero=0.000000000001
		for i in range(256):
			if intensidades[i] != 0:
				if i < corte:
					pi_zero+=intensidades[i]
				pi[i]=intensidades[i]/n
				pitotal+=pi[i]

		pi_one=(n-pi_zero)/n
		pi_zero=pi_zero/n

		mean_zero=0.0
		mean_one=0.0
		mean_global=0.0
		for i in range(256):
			if intensidades[i]!=0:
				if i < corte:
					mean_zero+= (i * pi[i])
				else:
					mean_one+= (i * pi[i])
				mean_global+=(i*pi[i])

		mean_zero=mean_zero/pi_zero
		mean_one=mean_one/pi_one

		sigma_zero=pi_zero*((mean_zero-mean_global)**2) + pi_one*((mean_one-mean_global)**2)

		sigma_t=0.000000000001
		for i in range(256):
			if intensidades[i]!=0:
				sigma_t+=pi[i]*((i-mean_global)**2)
		n_final=sigma_zero/sigma_t
		if n_final < 0.6 and n_final > 0.5:
			break
	return corte

def umbral_division(data, corte):
	data_new=np.array([[0 for x in range(data.shape[1])] for y in range(data.shape[0])])
	for i in range(data.shape[0]):
		for j in range(data.shape[1]):
			if data[i][j] < corte:
				data_new[i][j]=0
			else:
				data_new[i][j]=255
	return data_new


img=cv2.imread(sys.argv[1], 0)
umbral=umbral_varianza(img)
umbran_dividido=umbral_division(img, umbral)
print("Matriz escala de grises: ")
for i in img:
	print(i)
print()
print("Valor de corte:", umbral)
print()
print("Matriz de umbral de varianzas: ")
for i in umbran_dividido:
	print(i)

cv2.imwrite("imagenes/foto"+str(umbral)+".jpg", umbran_dividido)
img_um = cv2.imread("imagenes/foto"+str(umbral)+".jpg")
cv2.imshow("Umbral varianza", img_um)
cv2.waitKey()
cv2.destroyAllWindows()

