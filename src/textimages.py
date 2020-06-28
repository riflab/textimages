'''
arif.darmawan@riflab.com

20200211 first version
'''

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from glob import glob as list_image
import textwrap
import os
from webcolors import name_to_rgb
from docx import Document

def writeText(text, image, font_size=30, line_spacing=1.5, xo=265, yo=200, padx=10, pady=10,  
		lineswidth=45, font='BRLNSR.ttf', transparancy=30, colortext='black', colorbackground='white'):
	
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


def imFilter(im, blur=1, xsize=1024, ysize=1024):
	size = (xsize, ysize)

	image = Image.open(im)
	image = image.resize(size,Image.ANTIALIAS)
	image = image.filter(ImageFilter.GaussianBlur(blur))

	return image

def add_images(image, logo, xo=0, yo=0):
	imglogo = Image.open(logo)
	lx, ly = imglogo.size
	ix, iy = image.size
	image.paste(imglogo, (xo, yo), imglogo)

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

def save_im(workdir, im, imDir, Saved=False):
	if not os.path.exists(workdir+'/saved'):
		os.makedirs(workdir+'/saved')

	if Saved == True:
		im.save(imDir.replace("/images", "/saved"))
	
	print(imDir.replace("/images", "/saved"))

if __name__ == "__main__":

	workdir = '../data/'+'kurma'
	logo = workdir+'/images/'+'logo.png'
	images = list_image(workdir+'/images/'+'ig*.png')
	tagline = 'Ada banyak sekali manfaat Madu jadi jangan tunggu lama lagi dan segera jadikan Madu sebagai suplemen wajib harian anda.'
	contact = 'Pemesanan hubungi Arif >>> WA 0811-220-9194, IG @tokoalhaf, www.alhaf.com '
	texts = read_docx(workdir)
	
	j=0
	for i in range(len(texts)):
		if j == len(images):
			j=0
		a = texts[i].split(': ')
		im = imFilter(images[j])
		im = writeText(a[0], im, xo=265, yo=200, font_size=35, transparancy=20)
		im = writeText(a[1], im, xo=265, yo=300, font_size=28, transparancy=20)
		im = writeText(tagline, im, xo=265, yo=800, font_size=24, transparancy=20)
		im = writeText(contact, im, xo=60, yo=950, font_size=24, transparancy=20, lineswidth=110, colortext='darkgreen')
		im = add_images(im, logo, xo=40, yo=40)
		
		new_file = images[j].split('_')[0]+str(i)+'.png'

		save_im(workdir, im, new_file, True)
		j+=1

		# im.show()
		