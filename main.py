from PIL import Image
import sys
import shlex
import struct
import platform
import subprocess 
import numpy as np
 
def get_terminal_size():
	current_os = platform.system()
	tuple_xy = None
    	if current_os == 'Windows':
        	tuple_xy = _get_terminal_size_windows()
        	if tuple_xy is None:
            		tuple_xy = _get_terminal_size_tput()
    	if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        	tuple_xy = _get_terminal_size_linux()
    	if tuple_xy is None:
        	tuple_xy = (80, 25) 
    	return tuple_xy
 
 
def _get_terminal_size_windows():
    	try:
        	from ctypes import windll, create_string_buffer
        	h = windll.kernel32.GetStdHandle(-12)
        	csbi = create_string_buffer(22)
        	res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        	if res:
            		(bufx, bufy, curx, cury, wattr,
             		left, top, right, bottom,
             		maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            	sizex = right - left + 1
            	sizey = bottom - top + 1
            	return sizex, sizey
    	except:
        	pass
 

def _get_terminal_size_tput():
    	try:
        	cols = int(subprocess.check_call(shlex.split('tput cols')))
        	rows = int(subprocess.check_call(shlex.split('tput lines')))
        	return (cols, rows)
    	except:
        	pass
 
 
def _get_terminal_size_linux():
    	def ioctl_GWINSZ(fd):
        	try:
           		import fcntl
            		import termios
            		cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            		return cr
        	except:
            		pass
    	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    	if not cr:
        	try:
            		fd = os.open(os.ctermid(), os.O_RDONLY)
            		cr = ioctl_GWINSZ(fd)
            		os.close(fd)
        	except:
            		pass
    	if not cr:
        	try:
            		cr = (os.environ['LINES'], os.environ['COLUMNS'])
       		except:
        		return None
   	return int(cr[1]), int(cr[0])


def apply_kernel(x, y, img, kernel):
	sum = 0
	count = 0
	
	left = 0 if x < 3 else x - 2
	right = len(img[0]) if x > len(img[0]) - 3 else x + 3	
	top = 0 if y < 3 else y - 2
	bottom = len(img) if y > len(img) - 3 else y + 3
	
	for i in xrange(left, right):
		for j in xrange(top, bottom):
			count += 1
			sum += img[j][i] * 
	return float(sum) / count

def blur(img, kernel):
	temp = np.array([[0 for p in xrange(len(img[w]`))] for w in xrange(len(img))], np.float64)
	for i in xrange(len(img)):
		for j in xrange(len(matrix[i])):
			temp[i][j] = apply_kernel(j, i, img, kernel)	
	return temp
 
if __name__ == "__main__":
	# load image as greyscale
	sizex, sizey = get_terminal_size()
	img = Image.open(sys.argv[1], 'r')
	img = img.convert('L')

	# make gaussian kernel with standard deviation of 1.2
	gaussian = np.matrix('2 4 5 4 2;4 9 12 9 4;5 12 15 12 5;4 9 12 9 4;2 4 5 4 2')
	gaussian = np.divide(gaussian, 159.0)

	# get img data 
	matrix = np.asarray(img.getdata(), dtype=np.float64).reshape((img.size[1], img.size[0]))
	
	# use the gaussian kernel to blur the image
	new_img = Image.new('L', (img.size[0], img.sixe[1]))
	data = blur(matrix, gaussian)
	data.flatten()

	# find largest greyscale value gradients

	# 
	






	output = ''
	for i in xrange(len(matrix)):
		for j in xrange(len(matrix[i])):
			if matrix[i][j] < 120: output += '#'
			else: output += '.'
		output += '\n'
	print output
