def LZencoder(info):
	table = dict()
	table[''] = 0
    
	curStr = ''
	coding = []
	coding_b = []
# Creat the Dictionary for the Lz78
# The coding_b is binary format and coding is decimal format
	for item in info:
		curStr += item
		if curStr not in table.keys():
			table[curStr] = len(table)
			ss = '{0:b}'.format(table[curStr[0:len(curStr)-1]])
			s = str(ss)
			s = s.zfill(5)
			# Add pre zeors to make the codeward be fixed 5 bits
			coding_b.append(s)
			coding.append(str(table[curStr[0:len(curStr)-1]])+','+item)
			curStr = ''

	table_index = {v: k for k, v in table.items()}
     # change the values and keys for easier decoding 
	return table_index,coding,coding_b
    
def LZdecoder(Dict,coding_source):
	decodeStr = ''
# for decoding ,split the coding into two parts: location + last letter
    # find the value of the location in dictionary and connect last letter to decode


	for item in coding_source:
		index,last_str = item.split(',')
# split it into two parts

		decodeStr += (Dict[int(index)]+last_str)
# Add them 

	return decodeStr
if __name__ == '__main__':
	source = '00010010000100100001001000010010000100100001001000010010000100'
	Dict,codeword,codeword_b = LZencoder(source)
	print('The codeword are :',coding_b)
	print('The Dictionary are:',Dict)
	if LZdecoder(Dict,codeword) == source:
		print('Decoding Successfully')
