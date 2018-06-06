
from scipy.stats import bernoulli
def huffman(p = 0.99):
	print('For p = {},the result of 10 times trials are: '.format(p))
	for i in range(10):
		r = bernoulli.rvs(p, size=1000)
		key = ['11','10','01','00']
		value = ['0','10','110','111']
		Hdic = dict(zip(key,value))
		# Creat the codig for encoding and decoding
		source = [str(r[x]) + str(r[x + 1]) for x in range(0,len(r),2)]
		coding = ''
		for item in source:
			coding += Hdic[item]
		print('The length of coding in {0}th trilas is {1}'.format(i+1,len(coding)))
		Hdic_reverse = dict(zip(value,key))
		curStr = ''
		decodedStr = ''
		for item in coding:
			curStr += item
			if curStr in Hdic_reverse.keys():
				decodedStr += Hdic_reverse[curStr]
				curStr = ''

		if ''.join(source) == decodedStr:
			print('Decoding Successfully' )

if __name__=='__main__':
	huffman(p=0.99)
	
   #huffman(p=0.7)
			
		

