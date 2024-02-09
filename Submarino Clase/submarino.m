% Declaración de variables
a = zeros(200, 200); % Matriz de 200x200 pixeles
a(1:30,:,3) = 255;
a(1:30,:,2) = 100;
a(31:200,:,3)= 255;
imshow(a) % Muestra la matriz en la ventana
g = 9.8; % Aceleración de la gravedad
b = 0.43; % Coeficiente de fricción
vy(1) = 0; % Velocidad vertical inicial
p = 1000; % Densidad del agua
posicionver = 40; % Posición vertical inicial
posicionhor = 100; % Posición horizontal inicial
m = 1000; % Masa inicial del submarino
v = 1; % Volumen del submarino
datoDeseado = 120; % Posición deseada
dt = 100; % Paso de tiempo
rangomax = 0;
aux = 0.00025;
% Dibuja una linea representando el inicio del mar
a(30, :) = 255;

% Dibuja una línea horizontal de puntos en la posición deseada
for j = 1:70
  a(datoDeseado, j) = 255;
end

% Muestra la matriz en la ventanaa
imshow(a)
% Calcula la energía cinética
E = -(p * g * v);
% Ciclo principal
for i = 1:300

  % Calcula la velocidad vertical actual
  vy(i + 1) = dt * ((E / m) + g - (b * vy(i)) / m) + vy(i);

  % Calcula la posición vertical actual
  posicionver(i + 1) = posicionver(i) + dt * vy(i + 1)+ 1-0.5*(rand(1,1));


  % Calcula la diferencia entre la posición deseada y la posición actual
  d = datoDeseado - posicionver(i + 1);

  % Actualiza la masa del submarino

  %SISTEMA DE CONTROL ON - OF
  if d < 0
    m = 1000 - aux;
  elseif d > 0
    m = 1000 + aux;
  else
    m = 1000;
  end

  %SISTEMA DE CONTROL PROPORCIONAL
  %m = 0.00008 * d + 1000;

  % Limita la posición vertical a 200 y 30
  if posicionver(i + 1) >= 200
    posicionver(i + 1) = 200;
  end
  if posicionver(i + 1) <= 30
    posicionver(i + 1) = 29;
  end

  if posicionver(i + 1) > rangomax
      rangomax = posicionver(i + 1);
  end
% Dibuja el submarino
r = 12; % Radio del submarino
r1 = 7; % Radio de la hélice
for theta = 0:0.1:2 * pi
  a(floor(posicionver(i + 1) + r * cos(theta)), floor(100 + r * sin(theta))) = 255;
  a(floor(posicionver(i + 1) - 1 + r1 * cos(theta)), floor(100 + 4 + r1 * sin(theta))) = 255;
end

  % Muestra la matriz en la ventana
  imshow(a)

  % Borra el submarino
  for theta = 0:0.1:2 * pi
    a(floor(posicionver(i + 1) + r * cos(theta)), floor(100 + r * sin(theta))) = 0;
    a(floor(posicionver(i + 1) - 1 + r1 * cos(theta)), floor(100 + 4 + r1 * sin(theta))) = 0;
  end
  
  % Pausa la ejecución del programa durante 1 milisegundo
  pause(0.00000001);
end

% Grafica la posición vertical del submarino a lo largo del tiempo
plot(posicionver)
xlabel("Tiempo")
ylabel("Comportamiento del submarino")
grid on