'''
arif.darmawan@riflab.com

20200211 first version
20200906 update batch and separate processing
'''

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from glob import glob as list_image
import textwrap
import os
import random
from webcolors import name_to_rgb
from docx import Document


def writeText(text, image, font_size=30, line_spacing=1.5, xo=265, yo=200, padx=10, pady=10,  
		lineswidth=30, font='BRLNSR.ttf', transparancy=100, colortext='black', colorbackground='white'):
	
	image = image.convert("RGBA")

	font_type = ImageFont.truetype('../font/'+font, font_size)

	draw = ImageDraw.Draw(image)
	lines = textwrap.wrap(text, lineswidth)

	list_w = []
	list_h = []
	i=0
	for line in lines:
		x, y = (xo,yo+(i*font_size*line_spacing))
		w, h = font_type.getsize(line)
		list_w.append(w)
		list_h.append(h)
		i+=1

	# lx, ly = imglogo.size
	ix, iy = image.size
	tmp = Image.new('RGBA', image.size, name_to_rgb('black')+(0,))
	draw = ImageDraw.Draw(tmp)
	draw.rectangle((xo-padx, yo-pady, max(list_w)+x+padx, max(list_h)+y+pady), fill=name_to_rgb(colorbackground)+(int((100-transparancy)/100*255),))
	image = Image.alpha_composite(image, tmp)
	image = image.convert("RGB")
	draw = ImageDraw.Draw(image)

	i=0
	for line in lines:
		x, y = (xo,yo+(i*font_size*line_spacing))
		w, h = font_type.getsize(line)
		draw.multiline_text(xy=(x,y), text=line, fill=colortext, font=font_type, align='right')
		i+=1

	return image


def imFilter(im, blur=0, xsize=1024, ysize=1024):
	size = (xsize, ysize)

	image = Image.open(im)
	image = image.resize(size, Image.ANTIALIAS)
	# image = image.filter(ImageFilter.GaussianBlur(blur))

	return image

def read_docx(workdir):
	ftext = workdir+'/text.docx'
	document = Document(ftext)
	texts=[]
	i=0
	for para in document.paragraphs:
		if para.text != '':
			texts.append(para.text)
			i+=1
	return texts

def save_im(path):
	
	if not os.path.exists(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	im.save(path)
	print(path)
if __name__ == "__main__":

	workdir = 'madu'
	path_image = '../data/' + workdir + '/images/*.JPG'
	path_saved = '../data/' + workdir + '/saved/'
	path_docx = '../data/' + workdir
	batch = False
	list_image = list_image(path_image)
	list_docx = path_docx

	texts = read_docx(path_docx)

	if batch == False:
		for i in range(len(texts)):
			text = texts[i].split('. ')
			for j in range(len(text)+1):
				if j < len(text):
					imP = list_image[random.randint(0, len(list_image)-2)]
					im = imFilter(imP)
					im = writeText(text[j], im, xo=60, yo=250, font_size=50, transparancy=20)
					new_file = path_saved + str(i+1).zfill(2) + '/im_' + str(j+1).zfill(2) + '.JPG'
					save_im(new_file)
				else:
					imP = list_image[26]
					im = imFilter(imP)
					im = writeText('Ayo Minum Madu Asli Murni Alami Hanya Di:', im, xo=60, yo=250, font_size=50, transparancy=20, lineswidth=18)
					new_file = path_saved + str(i+1).zfill(2) + '/im_' + str(j+1).zfill(2) + '.JPG'
					save_im(new_file)
	else:
		for i in range(len(texts)):
			text = texts[i]

			imP = list_image[random.randint(0, len(list_image)-2)]
			im = imFilter(imP)
			im = writeText(text, im, xo=60, yo=250, font_size=40, transparancy=20, lineswidth=40)
			new_file = path_saved + str(i+1).zfill(2) + '/im_' + str(1).zfill(2) + '.JPG'
			# im = add_images(im, logo, xo=40, yo=40)
			save_im(new_file)

			imP = list_image[26]
			im = imFilter(imP)
			im = writeText('Ayo Minum Madu Asli Murni Alami Hanya Di:', im, xo=60, yo=250, font_size=50, transparancy=20, lineswidth=18)
			new_file = path_saved + str(i+1).zfill(2) + '/im_' + str(2).zfill(2) + '.JPG'
			save_im(new_file)
		

		
