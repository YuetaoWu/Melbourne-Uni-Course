f1int8_array = imread('MonashRd1_640.bmp', 'bmp');
f2int8_array = imread('MonashRd2_640.bmp', 'bmp');
% load the image

int16_array1=int16(f1int8_array);
int16_array2=int16(f2int8_array);

int16_diff = int16_array2 - int16_array1 + 0;

uint8_diff = uint8(int16_diff);
% change it to 16bits to avoid negetive value
%imwrite(uint8_diff,'DiffImage.bmp','bmp');

imwrite(uint8_diff, 'DiffImage_Q100.jpg', 'jpg', 'quality', 100);
diffint8_array =  imread('DiffImage_Q10.jpg', 'jpg');
int16_arraydiff=int16(diffint8_array);
int16_combine = int16_arraydiff + int16_array1;
uint8_combine = uint8(int16_combine);
imwrite(uint8_combine,'CombImage.bmp','bmp');


