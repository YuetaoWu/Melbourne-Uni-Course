% T = 8;
% t = 1:1:10000;
% i = 1;
% A = 1;
% u(10000) = 0;
% N=128;
% while(1)
%     u(i) = 1/sqrt(2);
%     u(i+8) = -1/sqrt(2);
%     i=i+16;
%     if (i>10000)
%         break
%     end
% end
% %plot(u)
% y = fft(u);
% mag =abs(y);
% %f = 10000*(1/8)/N;
% plot(mag);
clf;
T = 8
fs=100;N=128;   %采样频率和数据点数
n=0:N-1;t=n/fs;   %时间序列
x1=sqrt(2)*sin(pi*t/T); %信号
y1=fft(x1,N);    %对信号进行快速Fourier变换
mag1=abs(y1);     %求得Fourier变换后的振幅
f1=n*fs/N;    %频率序列
   %绘出随频率变化的振幅

figure(2)
x2=sqrt(2); %信号
y2=fft(x2,N);    %对信号进行快速Fourier变换
mag2=abs(y2);     %求得Fourier变换后的振幅
f2=n*fs/N;    %频率序列
plot(f1,mag1,f2,mag2);   %绘出随频率变化的振幅



    