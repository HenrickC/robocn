import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Parâmetros do robô
r = 2.0  # raio da roda (cm)
R = 7.0  # metade da distância entre rodas (base / 2) (cm)
dt = 0.05  # passo de tempo (s)

# Raio ideal da curva (para cada lóbulo do 8)
r_nominal = 20.0  # cm
erro_raio_max = 2.0  # cm

# Estado inicial
x, y = 0.0, -r_nominal
theta = math.pi / 2
t = 0.0
trajetoria = []
raio_atual = []
voltas_completas = 0
raios_medidos = []
em_cima = False
parar = False
fase = 0  # 0 = curva à esquerda, 1 = curva à direita

# Modelo cinemático diferencial
def modelo_cinematico_diferencial(r, R, omega_L, omega_R, theta):
    v = (r / 2.0) * (omega_L + omega_R)
    omega = (r / (2.0 * R)) * (omega_R - omega_L)

    dx = v * math.cos(theta)
    dy = v * math.sin(theta)
    dtheta = omega

    return dx, dy, dtheta



def taylor():
    fact[16]
    for i in range(fact):
        aux = 1
        if(aux = 1):
            fact[i] = 1
        while i != 1:
            aux2 = i
            aux2 *= (aux2-1)
            


    for 


# Cálculo do raio médio com base nos pontos
def calcula_raio(pontos):
    if len(pontos) < 3:
        return 0
    pontos = np.array(pontos)
    centro = np.mean(pontos, axis=0)
    raios = np.linalg.norm(pontos - centro, axis=1)
    return np.mean(raios)

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(6, 6))
line, = ax.plot([], [], lw=2, label="Trajetória")
point, = ax.plot([], [], 'ro', label="Robô")
text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')
ax.grid()
ax.legend()

# Função de atualização da animação
def update(frame):
    global x, y, theta, t, em_cima, raio_atual, voltas_completas, parar, fase

    if parar:
        return line, point, text

    # Alterna a direção para formar o 8
    if fase == 0:
        omega_L = 1.5  # roda esquerda
        omega_R = 0.5  # roda direita
    else:
        omega_L = 0.5
        omega_R = 1.5

    # Movimento com modelo diferencial
    dx, dy, dtheta = modelo_cinematico_diferencial(r, R, omega_L, omega_R, theta)
    x += dx * dt
    y += dy * dt
    theta += dtheta * dt
    t += dt

    trajetoria.append((x, y))
    raio_atual.append((x, y))

    # Troca de lóbulo e verificação do raio
    if not em_cima and y > 0:
        r_medido = calcula_raio(raio_atual)
        raios_medidos.append(r_medido)
        if abs(r_medido - r_nominal) >= erro_raio_max:
            parar = True
        raio_atual = []
        em_cima = True
        fase = 1
    elif em_cima and y < 0:
        r_medido = calcula_raio(raio_atual)
        raios_medidos.append(r_medido)
        if abs(r_medido - r_nominal) >= erro_raio_max:
            parar = True
        raio_atual = []
        em_cima = False
        voltas_completas += 1
        fase = 0

    # Atualiza o gráfico
    dados = np.array(trajetoria)
    line.set_data(dados[:, 0], dados[:, 1])
    point.set_data(x, y)
    text.set_text(f'Voltas: {voltas_completas}')

    return line, point, text

# Criação da animação
ani = animation.FuncAnimation(fig, update, frames=1000, interval=30, blit=True)
plt.title("Trajetória em 8 com Modelo Cinemático Diferencial")
plt.show()

print(f"Voltas completas até atingir erro de 2 cm: {voltas_completas}")
