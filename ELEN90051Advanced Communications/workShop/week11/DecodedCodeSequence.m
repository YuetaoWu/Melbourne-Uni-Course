function [DecodedCodeSequence]=ConvDecoder(ReceivedSequence,Type)

	tbl = 5*3;
	if(Type == 'hard')
		DecodedCodeSequence = vitdec(ReceivedSequence,Trellis,tbl,'cont','hard')
	end
	else
		DecodedCodeSequence = vitdec(ReceivedSequence,Trellis,tbl,'cont','unquant')
	end