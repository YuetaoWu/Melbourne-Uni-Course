import numpy as np
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

stateTrs = {'0to0':[0,[0,0]],'0to2':[1,[1,1]],'1to0':[0,[1,0]],
            '1to2':[1,[0,1]],'2to1':[0,[1,1]],'2to3':[1,[0,0]],'3to1':[0,[0,1]],'3to3':[1,[1,0]]}

def Distance(m1,m2,Type):
	if Type == 'Hard':
	    return np.sum(np.abs(m1-m2))
	    # The hamming distance that calculate the # of different bits
	if Type == 'Soft':
	    return np.sqrt(np.sum(np.square(m1-m2)))
	    # The Euclidean distance that d = sqrt[ \sum (xi-yi)^2 ]
# implement the encoder
def ConvEncoder(SourceSequence,GenPoly):
	# The SourceSequence is a stream of bits with {0,1} in string type
	# The GenPoly is the matrix.In this case GenPoly[0] = g1 = [1,1,1]  GenPoly[1] = g2 = [1,1,0]
	# matrix multiply are using for calculation efficiency
	EncodedCodeSequence = list()
	reg = np.zeros((1,3)) # The initial state of register are [0,0,0]
	#print(reg.shape)
	for curBit in SourceSequence:# for every bit in the sequency
	    # Insert the curBit into the reg
	    reg = np.array([[curBit,reg[0][0],reg[0][1]]])
	    #print(reg.shape)
	    y = np.dot(reg,GenPoly)  # y = [x0+x1+x2,x0+x1]
	    y = np.mod(y,2)
	    EncodedCodeSequence = EncodedCodeSequence + [int(y[0][0]),int(y[0][1])]
	return np.array(EncodedCodeSequence)
def bpskModulator(SourceSequence):
    # for bandpass bpsk the output are just the same bits with [0,1]
	return SourceSequence

def ChanneloverNosie(ModSeq,Var):
	#output = np.zeros(ModSeq.shape[0])
	# initial the output sequency
	Noise = np.random.normal(loc=0, scale=Var,size = ModSeq.shape[0])
	#Noise = np.random.normal(loc=0, scale=Var)
	return ModSeq + Noise

def bpskDemodulator(rxSig,Type):
	output = np.zeros(rxSig.shape[0])
	Dis2Zero = np.abs(rxSig-0)
	Dis2One  = np.abs(rxSig-1)

	if Type == 'Hard':
	    return (Dis2One<Dis2Zero).astype(np.int8)  # a bool array with True(1) & False(0)  if Dis2One < Dis2Zero then 1 chosen(True).
	if Type == 'Soft':
		return rxSig
		
		return output     
def findCode(G,state,i,ans):
	if i==0:
		return
	ans.append(int(G[state,i][0]))
	findCode(G,G[state,i][1],i-1,ans)

def ConvDecoder(ReceivedSequence,Type):
	# Vertib Algorithm is just a dynamic programming algorithm.
	F = np.ones([4,ReceivedSequence.shape[0]//2+2])*0xFFFF # for state's F[00] F[01] F[10]  F[11] set the large value for init;
	G = np.zeros([4,ReceivedSequence.shape[0]//2+2,2])  # to store the decision make. to recover the path to get the decode code.
	#Reg = np.zeros(4)
	F[0,0] = 0
	for i in range(1,(ReceivedSequence.shape[0]//2)+1,1):
		for cur_state in range(4):
			for pre_state in range(4): # find the min value for previous state to current state
				trans = str(pre_state)+'to'+str(cur_state)
				if(trans in stateTrs.keys()):
				#if the state transform is exists()
					predOut = np.array(stateTrs[trans][1])
					realOut = ReceivedSequence[(i-1)*2:((i-1)*2+1)+1] 
					# The state diagram are stored in a stateTrs dictionary
					dis = Distance(predOut,realOut,Type) 
					# determine the distance between  predict sequence and received sequence 
					
					if dis+F[pre_state,i-1]<=F[cur_state,i]:
						F[cur_state,i] = dis+F[pre_state,i-1]
					# update the min Value.
						G[cur_state,i][1] = pre_state
						G[cur_state,i][0] = stateTrs[trans][0] 
						# store the cur_state is from pre_state and input. 

	# Find the min values of the final node.
	minState = 0
	minVal = 0xFFFF
	for item in range(4):
		if(F[item,i]<minVal):
			minState = item
			minVal = F[item,i]
	        
	EncodedCodeSequence = list()
	# use a recursive function to generate the predicted input sequence using G array
	findCode(G,minState,i,EncodedCodeSequence)

	return np.array(EncodedCodeSequence[::-1])

def simulate(SeqLen=1000,TransmitNum = 20,NoiseStep = 0.01):
	VarRange = list()
	GenPoly  = np.array([[1,1],[1,1],[1,0]])
	NoiseRange = 1-0.1
	BER = np.zeros([3,NoiseRange//NoiseStep]) # uncoded ,hard,soft
	
	source = np.random.randint(0,2,SeqLen) # Generate the random sequence of {0,1} with length  SeqLen
	
	unChannelcoded = source
	Channelcoded = ConvEncoder(source,GenPoly)
	for Variance in range(int(NoiseRange//NoiseStep)):
		Var = 0.1 + Variance*NoiseStep
		VarRange.append(Var)
  
		for i in range(TransmitNum):

			BPSKencod_unChannelcoded ,BPSKencod_Channelcoded =bpskModulator(unChannelcoded) , bpskModulator(Channelcoded)

		# noise over channel:

			Rec_BPSKencod_unChannelcoded = ChanneloverNosie(BPSKencod_unChannelcoded,Var*2)
			Rec_BPSKencod_Channelcoded =  ChanneloverNosie(BPSKencod_Channelcoded,Var)

			Rec_BPSKdecod_unChannelcoded = bpskDemodulator(Rec_BPSKencod_unChannelcoded,'Hard')
			Rec_BPSKhardDecod_Channelcoded  = bpskDemodulator(Rec_BPSKencod_Channelcoded,'Hard')
			Rec_BPSKsoftDecod_Channelcoded = bpskDemodulator(Rec_BPSKencod_Channelcoded,'Soft')

			RecSeq_un = Rec_BPSKdecod_unChannelcoded
			RecSeq_hard = ConvDecoder(Rec_BPSKhardDecod_Channelcoded,'Hard')
			RecSeq_soft = ConvDecoder(Rec_BPSKsoftDecod_Channelcoded,'Soft')

			Error_un = np.sum(np.abs(Rec_BPSKdecod_unChannelcoded-source))
			Error_hard = np.sum(np.abs(RecSeq_hard-source))
			Error_soft = np.sum(np.abs(RecSeq_soft-source))

			BER[0][Variance] += Error_un/SeqLen
			BER[1][Variance] += Error_hard/SeqLen
			BER[2][Variance] += Error_soft/SeqLen


		BER = BER/TransmitNum # get the average bit error rate.

	return BER,np.array(VarRange)


if __name__ == '__main__':
    
	'''source = np.array([1,1,0,0,0])#'110110001'
	GenPoly  = np.array([[1,1],[1,1],[1,0]])
	cov = ConvEncoder(source,GenPoly)
	print(cov)
	#bpsk_en = bpskModulator(cov)
	#rec = ChanneloverNosie(bpsk_en,0.7)

	#rec_un = ChanneloverNosie(source,0.7)
 
	#bpsk_de = bpskDemodulator(rec,'Hard')
	#bpsk_de_un = bpskDemodulator(rec_un,'Hard')

	
	#ans = ConvDecoder(np.array([1,1,0,1,0,1,1,0,0,0]),'Hard')
	#print('cov ans is {}'.format(ans))
     '''
 
	
	BER,VarRange = simulate(1000,2,0.1)
	SNR  = 10*np.log10(1/VarRange)
	plt.figure(figsize = (14,8))
	plt.plot(SNR,BER[2],'r',SNR,BER[1],'g',SNR,BER[0],'b')
	plt.xlabel('SNR')
	plt.ylabel('Bit Error Rate')
	plt.grid()
	plt.legend(['Soft Decision','Hard Decision','UnChannel coded'])


     
     


