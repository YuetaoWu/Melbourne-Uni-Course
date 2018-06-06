clear;
clc;
x1 = binornd(1, 0.7, 1, 1000);     %source code
source_code_length = length(x1);    %source_code_length
i = 1;      %source code index
j = 1;      %huffman encode index
ENCODE_ERR = 0;  %to check if I include all possible symbols

%Huffman encoding
while i <= source_code_length
    if x1(i)==1 & x1(i+1)==1
        x1_encode(j) = 0;
        j = j+1;
    elseif x1(i)==1 & x1(i+1)==0
        x1_encode(j) =1;
        x1_encode(j+1) =0;
        j = j+2;
    elseif x1(i)==0 & x1(i+1)==1
        x1_encode(j) =1;
        x1_encode(j+1) =1;
        x1_encode(j+2) =0;
        j = j+3;
    elseif x1(i)==0 & x1(i+1)==0
        x1_encode(j) = 1;
        x1_encode(j+1) = 1;
        x1_encode(j+2) = 1;
        j = j+3;
    else
        ENCODE_ERR = 1;
    end
    i = i + 2;      %second extension requires symbol length to be 2
end

%Huffman decoding
k = 1;  %huffman code index
p = 1;  %huffman decode index
huffman_code_length = length(x1_encode);    %length of huffman code
DECODE_ERR = 0;     %to see if I include all possible codes

%huffman decode
while k<=huffman_code_length
    if x1_encode(k)==0
        x1_decode(p) = 1;
        x1_decode(p+1) = 1;
        k = k + 1;
    elseif x1_encode(k)==1
        if x1_encode(k+1)==0
            x1_decode(p) = 1;
            x1_decode(p+1) = 0;
            k = k + 2;
        elseif x1_encode(k+1)==1
            if x1_encode(k+2)==0
                x1_decode(p) = 0;
                x1_decode(p+1) = 1;
                k = k + 3;
            elseif x1_encode(k+2)==1
                x1_decode(p) = 0;
                x1_decode(p+1) = 0;
                k = k + 3;
            else
                DECODE_ERR = 1;
            end
        else
            DECODE_ERR = 1;
        end
    else
        DECODE_ERR = 1;
    end
    p = p + 2;
end

%compare the source code and the decoded code.
COMPARE_ERR = 0;
for q = 1:1000
    if x1(q) ~= x1_decode(q)
        COMPARE_ERR = 1;
    end
end
            