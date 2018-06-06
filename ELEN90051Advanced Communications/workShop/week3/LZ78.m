clc;
clear;

%LZ78 encoder
source_str = ['00010010000100100001001000010010000100100001001000010010000100'];
%Dictionary
dict = [ ];
codeword = [ ];
i = 1;                                                                                   %source code bit index
dict_index = 1;
while i <= length(source_str)
    temp_str = source_str(i);
    searchresult = find(ismember(dict, temp_str));       %look up phrase in dictionary
    if(~isempty(searchresult))                                                  %if phrase in dictionary
        %Inner Loop to Check if Consecutive Characters Match
        loop_flag = true;
        j = 1;                                                                              %phrase bit index
        while loop_flag && ((i+j-1) < length(source_str))
            temp_str = strcat(temp_str, source_str(i+j));   %append phrase with following bit
            searchresult = find(ismember(dict, temp_str), 1);     %look up phrase in dictionary
            if(~isempty(searchresult))                                                   %if phrase in dictionary
                loop_flag = true;
                j = j+1;
            else
                loop_flag = false;
            end
        end
        %Process the Matched String
        compare_string1 = temp_str(1:end-1);                      %phrase without last bit that exists in the dictionary
        compare_string2 = temp_str;                                   %new phrase
        compare_string2 = strcat('''', compare_string2, '''');
        if((i+j-1) >= length(source_str))                                           %check if phrase exceed source length
            compare_string1 = temp_str;
            compare_string2 = 'EOF';
        end
        
        searchresult = find(ismember(dict, compare_string1));           %look up location of phrase without last bit 
    else
        searchresult = 0;
    end
    dict{dict_index} = temp_str;                  %put phrase into dictionary
    codeword{dict_index} = strcat(dec2bin(searchresult, 5), temp_str(end));
    i = i + length(temp_str);                         %jump to first bit of next phrase
    dict_index = dict_index + 1;
end

encoded_index = 1;
encoded_sequence = [];
for encoded_index = 1:(dict_index-1)
    encoded_sequence = strcat(encoded_sequence, codeword(encoded_index));
end
encoded_sequence

%LZ78 decoder
decoded_index = 1;
decoded_sequence = [];
for decoded_index = 1:(dict_index-1)
    decoded_sequence = strcat(decoded_sequence, dict(decoded_index));
end

decoded_sequence

