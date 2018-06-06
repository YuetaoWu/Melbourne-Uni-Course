i_array2 = imread('Perth_640.bmp', 'bmp');
% read the image.
bmp_size2 = size(i_array2);

imwrite(i_array2, 'Perth_Q100.jpg', 'jpg', 'quality', 100);
imwrite(i_array2, 'Perth_Q20.jpg', 'jpg', 'quality', 20);
imwrite(i_array2, 'Perth_Q10.jpg', 'jpg', 'quality', 10);
imwrite(i_array2, 'Perth_Q1.jpg', 'jpg', 'quality', 1);
% rewrite the image in different quality (100,20,10,1)

i_array3 = imread('Stinson_640.bmp', 'bmp');
bmp_size3 = size(i_array3);
% load the image
imwrite(i_array3, 'Stinson_Q100.jpg', 'jpg', 'quality', 100);
imwrite(i_array3, 'Stinson_Q20.jpg', 'jpg', 'quality', 20);
imwrite(i_array3, 'Stinson_Q10.jpg', 'jpg', 'quality', 10);
imwrite(i_array3, 'Stinson_Q1.jpg', 'jpg', 'quality', 1);
% rewrite the image in different quality (100,20,10,1)

i_array4 = imread('BowlCrowd_640.bmp', 'bmp');
bmp_size4 = size(i_array4);
% load the image

imwrite(i_array4, 'BowlCrowd_Q100.jpg', 'jpg', 'quality', 100);
imwrite(i_array4, 'BowlCrowd_Q20.jpg', 'jpg', 'quality', 20);
imwrite(i_array4, 'BowlCrowd_Q10.jpg', 'jpg', 'quality', 10);
imwrite(i_array4, 'BowlCrowd_Q1.jpg', 'jpg', 'quality', 1);

% rewrite the image in different quality (100,20,10,1)