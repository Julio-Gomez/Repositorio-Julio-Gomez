# -*- coding: utf-8 -*-
# Una vez corregidos los problemas de la carga de la página se procederá a actualizar el scroll down en la carga para que cargue todos los elementos.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from os.path import basename
from random import randint

import argparse
import os
import sys
import datetime
import time
import json

def setDriver(address, wait_time):
			
	chrome_options = Options()
	chrome_options.add_argument("--incognito")
	# chrome_options.add_argument("--headless")

	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_argument("--no-sandbox")
	 # chrome_options.add_argument('window-size=2560,1440')

	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--allow-insecure-localhost")
	chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
	chrome_options.add_argument("--ignore-certificate-errors")


	print("Iniciando driver")
	if os.name == "nt":
		driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:\\chromedriver.exe')
	else:
		driver = webdriver.Chrome(chrome_options=chrome_options)
		
		# driver = webdriver.Chrome(executable_path='C:\\chromedriver.exe', chrome_options=chrome_options)
	#driver.set_window_size(1024, 768)  # optional
	print("Accediendo a {}".format(address))
	# driver.get('https://super.walmart.com.mx')
	print("Esperando " + str(wait_time) + " segundos.")
	driver.implicitly_wait(10)
	driver.get(address)
	time.sleep(wait_time)

	return driver		

# def cargar_pagina(driver):
	###############################################AQUI INTENTABA CERRAR LOS ERRORES Y RECARGAR A PÀGINA
	# try:
	# 	cerrar = driver.find_element_by_xpath('//button[@class="button_btn__14_JE button_primary__3LAOq button_block__370Pe"]').click()
	# 	driver.refresh()
	# 	time.sleep(3)
	# except:
	# 	pass

	# target = driver.find_element_by_class_name('footer_container__3Dc53')

	# while(True):
		
	# 	try:
	# 		cerrar = driver.find_element_by_xpath('//button[@class="button_btn__14_JE button_primary__3LAOq button_block__370Pe"]').click()
	# 		# print('cerrando1')
	# 		time.sleep(3)
	# 	except:
	# 		pass

	# 	# actions = ActionChains(driver)
	# 	# actions.move_to_element(target)
	# 	# actions.perform()
	# 	# time.sleep(5)
	
	# 	try:
	# 		sel = driver.find_element_by_class_name('grid_loader__2VUr8')
	# 		# print(sel)
	# 		# print('sel')
	# 		# print(sel.text)
	# 		if 'No hay' in sel.text:
	# 			print(sel.text)
	# 			break
	# 		elif sel.text == 'Cargando...':
	# 			# print(sel.text)
	# 			try:
	# 				cerrar = driver.find_element_by_xpath('//button[@class="button_btn__14_JE button_primary__3LAOq button_block__370Pe"]').click()
	# 				time.sleep(3)
	# 				sel = driver.find_element_by_class_name('grid_loader__2VUr8')
	# 				sel.text
	# 			except:
	# 				time.sleep(5)
	# 				sel = driver.find_element_by_class_name('grid_loader__2VUr8')
	# 				sel.text
	# 		# print('-----------------')
	# 		# print(sel.text)
	# 		if sel.text == 'Cargando...':
	# 			# medir altura de la pàgina, recargar y bajar a la misma altura
	# 			# height = driver.execute_script("return document.body.scrollHeight")
	# 			# print(height)

	# 			# time.sleep(5)
	# 			# driver.execute_script("window.scrollTo(0, 0);")
	# 			break		
	# 	except:
	# 		break
		
	# return driver

def extraer_datos(driver, f_out, url, wait_time):
	# print('extrayendo')

	try:
				
		try:
			breadcrumb = driver.find_element_by_class_name('bread-crumbs_container__2zB_0')
			_breadcrumb = ''
			for li in breadcrumb.find_elements_by_tag_name('p'):
				_breadcrumb += li.text + '>'
			_breadcrumb = _breadcrumb[:-1].replace(',', '').upper()
		except:
			_breadcrumb = ''

		if _breadcrumb =='':
			try:
				_breadcrumb = driver.find_element_by_xpath('//*[@id="root"]/div/div/main/div[1]/section/div[1]/div[2]/div[1]/h1').text.upper()
			except:
				_breadcrumb = ''

		_fecha = str(time.strftime('%Y%m%d%H%M%S'))

		repetidos =[]
		a_escribir =''
		contador = 0
				
		productos =driver.find_element_by_xpath('//div[@class="infinite-scroll-component grid_container__1uFPC"]').find_elements_by_xpath('//div[@class="product_container__1Z_GP grid_productBox__2MtRC"]')

		# print(len(productos))
			
		for j, item in enumerate(productos):
		
			# try:
			code = BeautifulSoup(item.get_attribute('innerHTML'), "html.parser")
			_id_item = item.find_element_by_tag_name('a').get_attribute('href').split('/')[-1]
			

			name_item = code.find('div', {'class': 'product_name__1669g'}).find('a').text.replace(',', '').upper()
			# .text.replace(',', '').upper()

			try:
				_price = code.find('p', {'class': 'text_text__1DYNl text_inline__2pX2N text_bold__1nsB7'}).text.replace('/kg','').replace('\n','').split('$')[-1]					
			except:
				_price = ''
			try:
				oferta = code.find('div', {'class': 'price-and-promotions_promotionsContainer__3XvPF'}).text
				if oferta != '':
					_oferta = 'SI'
				else:
					_oferta ='NO'
			except:
				_oferta = 'NA'

			if _oferta == 'NA':
				try:
					oferta = code.find('p', {'class': 'price-and-promotions_oldPrice__qjnGK text_text__1DYNl text_inline__2pX2N'})
					if oferta.text != '':
						_oferta = 'SI'
					else:
						_oferta ='NO'
				except:
					_oferta = 'NA'

			if _oferta == 'NA':
				try:
					oferta = code.find('div', {'class': 'price-and-promotions_price__2imJs'}).find('p', {'class': 'price-and-promotions_oldPrice__qjnGK text_text__1DYNl text_inline__2pX2N'})
					if oferta.text != '':
						_oferta = 'SI'
					else:
						_oferta ='NO'
				except:
					_oferta = 'NA'

			_link = item.find_element_by_tag_name('a').get_attribute('href')

			# print(contador + j)
			# print(_breadcrumb)
			# print(_fecha)
			# print(_id_item)
			# print(_name_item)
			# print(_price)
			# print(_oferta)
			# print(_link)

			if _id_item not in repetidos:
				a_escribir += str(contador) + ',' + str(_breadcrumb) + ',' + str(_fecha) + ',WALMART_MX,WALMART_MX,' + str(_id_item) + ',' + str(_name_item) + ',' + str(_price.replace('--','')) + ',' + str(_oferta) + ',NA,NA,' + str(_link) + ',' + str(url) + '\n'
				contador += 1
				repetidos.append(_id_item)
			# except:
			# 	pass
		
	except:
		pass

	f_out.write('CONTROL,' + _breadcrumb + ',' + _fecha + ',WALMART_MX,WALMART_MX,NA,' + str(contador) + ',PRICE,NA,NA,NA,NA,' + url + '\n')
	f_out.write(a_escribir)

		
def main():


	parser = argparse.ArgumentParser()
	parser.add_argument("-url", help="URL original de la descarga", required=False)
	parser.add_argument("-url_file", help="URL original de la descarga", required=False)
	parser.add_argument("-wait_time", help="Tiempo de espera para carga de pagina", required=True)
	args = parser.parse_args()

	wait_time = randint(3, 3 + int(args.wait_time))

	if args.url:
		list_url = [args.url]
	elif args.url_file:
		list_url = [i.strip() for i in open(args.url_file).readlines()]
	else:
		print('Se necesitan al menos una URL')
		sys.exit(0)

	f_out = open('WALMART_MX_LVL2.csv', 'w')

	for url in list_url:
		driver = setDriver(url, int(wait_time))
		# driver = cargar_pagina(driver)
		extraer_datos(driver, f_out, url, wait_time)
		driver.close()

	f_out.close()

if __name__ == "__main__":
	main()
