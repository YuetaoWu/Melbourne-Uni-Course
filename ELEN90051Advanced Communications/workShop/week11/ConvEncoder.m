function [EncodedCodeSequence] = ConvEncoder(SourceSequence,GenPoly)
	
	Trellis = poly2trellis(GenPoly);
	
	EncodedCodeSequence = convenc(SourceSequence,Trellis);
	
end