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
fs=100;N=128;   %����Ƶ�ʺ����ݵ���
n=0:N-1;t=n/fs;   %ʱ������
x1=sqrt(2)*sin(pi*t/T); %�ź�
y1=fft(x1,N);    %���źŽ��п���Fourier�任
mag1=abs(y1);     %���Fourier�任������
f1=n*fs/N;    %Ƶ������
   %�����Ƶ�ʱ仯�����

figure(2)
x2=sqrt(2); %�ź�
y2=fft(x2,N);    %���źŽ��п���Fourier�任
mag2=abs(y2);     %���Fourier�任������
f2=n*fs/N;    %Ƶ������
plot(f1,mag1,f2,mag2);   %�����Ƶ�ʱ仯�����



    