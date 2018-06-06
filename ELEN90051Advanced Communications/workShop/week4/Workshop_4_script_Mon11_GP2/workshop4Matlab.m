i_array = imread('KIsealion_640.bmp', 'bmp');

% read the KIsealion_640.bmp image
bmp_size = size(i_array);
%{
imwrite(i_array, 'KIsealion_Q100.jpg', 'jpg', 'quality', 100);
imwrite(i_array, 'KIsealion_Q50.jpg', 'jpg', 'quality', 50);
imwrite(i_array, 'KIsealion_Q40.jpg', 'jpg', 'quality', 40);
imwrite(i_array, 'KIsealion_Q30.jpg', 'jpg', 'quality', 30);
imwrite(i_array, 'KIsealion_Q20.jpg', 'jpg', 'quality', 20);
imwrite(i_array, 'KIsealion_Q10.jpg', 'jpg', 'quality', 10);
imwrite(i_array, 'KIsealion_Q5.jpg', 'jpg', 'quality', 5);
imwrite(i_array, 'KIsealion_Q1.jpg', 'jpg', 'quality', 1);
%}

figure(1);

% plot the image in R channel
plot(i_array(150,100:300,1), 'r');
grid on;
hold on;
xlabel('the xth pixel of RED in the 150th row');
ylabel('pixel value of RED in the 150th row');
title('compression and pixel values');
jpg_Q1 = imread('KIsealion_Q1.jpg', 'jpg');
% read the jpeg version of the image
plot(jpg_Q1(150,100:300,1), 'm');
jpg_Q30 = imread('KIsealion_Q30.jpg', 'jpg');
plot(jpg_Q30(150,100:300,1), 'k');
legend('bmp','jpg q1','jpg q30');

figure(2);
plot(i_array(150,1:640,1), 'r');
grid on;
hold on;
xlabel('the xth pixel in the 150th row');
ylabel('pixel value in the 150th row');
title('colors and pixel values');
plot(i_array(150,1:640,2), 'g');
plot(i_array(150,1:640,3), 'b');
legend('REG','GREEN','BLUE');
% plot the R G B channel of the image

figure(3);
imshow(i_array(145:155,1:640,1:3));

figure(4);
plot(jpg_Q30(150,1:640,1), 'r');
grid on;
hold on;
xlabel('the xth pixel in the 150th row');
ylabel('pixel value in the 150th row');
title('colors, compression and pixel values');
plot(jpg_Q30(150,1:640,2), 'g');
plot(jpg_Q30(150,1:640,3), 'b');
legend('REG','GREEN','BLUE');
