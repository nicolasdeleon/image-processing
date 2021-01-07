clear; home;
im=imread('ninia_y_rosa.jpg');
figure(1);
subplot(2,3,1);
imshow(im);title('1. Imagen RGB original');


gris=rgb2gray(im);
subplot(2,3,2);
imshow(gris);title('2. Transformación a escala de grises');


imR=double(im(:,:,1));
imG=double(im(:,:,2));
imB=double(im(:,:,3));
subplot(2,3,3);
imshow(imR,gray);title('3. Visualización de Banda ROJA original');


imR2=(imR-imG-imB);
masc=(imR2>20);
imR2=imR2.*masc;
subplot(2,3,4);
imR2=medfilt2(imR2);
imshow(imR2,gray);title('4. Filtro de mediana sobre banda ROJA');



imR2=imR2/255;
imR3=imadjust(imR2,[],[],1.8);
subplot(2,3,5);
imshow(imR3,[]);title('5. Corrección GAMMA factor 1.8');


disp('En la imagen 5 haga click en el centro de la rosa...');
[x y]=ginput(1);
y=round(y);x=round(x);

masc=0*imR3;
T=28;
masc(y-T:y+T,x-T:x+T)=masc(y-T:y+T,x-T:x+T)+1;

imR4=(double(imR3>0.01)).*masc;
subplot(2,3,6);
imshow(imR4,[]);title('6. Binarización "mascara" rosa');

masc2=1-(imR4);
imR=double(gris)/255;
imG=double(gris).*masc2/255;
imB=double(gris).*masc2/255;
figure(2);
imFinal=cat(3,imR,imG,imB);
imshow(imFinal);title('Efecto publicitario buscado...');








