#!/usr/bin/python3
import platform

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from config import *
import sys , os
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QApplication
import requests
from bs4 import BeautifulSoup



class Render(QWebPage):
    """Render HTML with PyQt5 WebKit."""

    def __init__(self, html):
        self.html = None
        self.app = QApplication(sys.argv)
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.mainFrame().setHtml(html)
        self.app.exec_()

    def _loadFinished(self, result):
        self.html = self.mainFrame().toHtml()
        self.app.quit()


class Sesion():
	def __init__(self, url):
		# La raw HTML
		source_html = requests.get(url).text
		#retorna el JavaScript renderizado en HTML
		self.render_html = Render(source_html).html
		
		
		self.button = self.render_html.findFirst("button[id=videooverlay]")
		self.button.click()
		# creo un objeto manejable con BeautifulSoup
		self.soup = BeautifulSoup(self.render_html, 'html.parser')
		#overlay_splash = self.soup.find_element_by_id('videooverlay')
        #overlay_splash.click()

	def render(self):
		print(self.button)


	def url_video(self):
		pass




url = 'https://openload.co/embed/oB-rkAWAEiE/'
a = Sesion(url).render()




class Cliente_Chrome(object):

    def __init__(self, url):
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(CHROME, chrome_options=chrome_options)
        #self.browser = webdriver.Chrome()
        self.start = time.time()
        self.browser.get(self.url)
        #self.browser.save_screenshot('screen.png')
        overlay_splash = self.browser.find_element_by_id('videooverlay')
        overlay_splash.click()
        

    def url_video(self):
        pagina = BeautifulSoup(self.browser.page_source, 'lxml')
        url_video = pagina.find('video', {'id': 'olvideo_html5_api'})['src']
        url = 'https://openload.co'+url_video
        fin = time.time() - self.start
        print(url)
        print('Segundos: %.3f' % fin)
        self.browser.quit()        
        #return url


class Cliente_Phantomjs(object):

	def __init__(self, url):
		self.url = url
		#self.browser = webdriver.Chrome()
		self.browser = webdriver.PhantomJS('C://Users//x//Desktop//Repositorio//series//src//bin//phantomjs.exe')
		#self.browser.set_window_size(1000, 700)
		self.start = time.time()
		self.browser.get(self.url)
		self.browser.save_screenshot('screen.png')
		# selecciona el elemento al que se hace click
		overlay_splash = self.browser.find_element_by_id('videooverlay')
		overlay_splash.click()
		
		
	def url_video(self):
		pagina = BeautifulSoup(self.browser.page_source, "html.parser", from_encoding='utf-8')
		pagina1 = self.browser.page_source
		print(pagina1)
		print('-'*100)
		url_video = pagina.find('video', {'id': 'olvideo_html5_api'})['src']
		print('https://openload.co' + url_video)
		fin = time.time() - self.start
		print('phantomjs')
		print('Segundos: %.3f' % fin)
		self.browser.quit()

	def sistema(self):
		if platform.system() == 'Windows':
			PHANTOMJS_PATH = os.path.abspath('phantomjs.exe')
		else:
			PHANTOMJS_PATH = os.path.abspath('phantomjs')			
		return PHANTOMJS_PATH



#url = ('https://openload.co/embed/oB-rkAWAEiE/')
#a = Cliente_Phantomjs(url).url_video()


#a.url_video()

#b = Cliente_Phantomjs(url).url_video()
