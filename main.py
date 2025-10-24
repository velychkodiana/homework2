import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import sympy as sp

# ================== ПІДКЛЮЧЕННЯ ШРИФТУ ==================
try:
    font_path = "Comfortaa-SemiBold.ttf"
    prop = fm.FontProperties(fname=font_path)
except:
    print("Шрифт Comfortaa не знайдено. Використовую системний шрифт.")
    prop = None

# ================== ПАРАМЕТРИ МОДЕЛІ =====================
N = 6
r = 2 * N
q = 200 * N
a = 10

print("============================================")
print("        МОДЕЛЬ ДИНАМІКИ ПОПУЛЯЦІЇ РИБИ")
print("============================================")
print(f"Варіант студента (N):     {N}")
print(f"Темп росту (r):            {r}")
print(f"Ємність середовища (q):    {q}")
print(f"Додатковий параметр (a):   {a}")
print("--------------------------------------------\n")

# ================== ПРАВА ЧАСТИНА ========================
def f(x, p):
    """dx/dt для популяції риби."""
    return r * x * (1 - x / q) - p

# ================== ВИПАДКИ ЗАВДАННЯ =====================
cases = [
    (r"Випадок 1: $p = \frac{rq}{4}$",               r*q/4, "r·q⁄4"),
    (r"Випадок 2: $p = \frac{rq}{4} - a^2$",         r*q/4 - a**2, "r·q⁄4 − a²"),
    (r"Випадок 3: $p = \frac{rq}{4} + a^2$",         r*q/4 + a**2, "r·q⁄4 + a²"),
]

# ================== ЧАС МОДЕЛЮВАННЯ ======================
T = 80
dt = 0.01
t = np.arange(0, T, dt)

# ================== ВІДТІНКИ РОЖЕВОГО ====================
colors = ['#FF69B4', '#FF1493', '#FF8AAE', '#FFB6C1']

# =========================================================
#                     ОСНОВНИЙ ЦИКЛ
# =========================================================
for idx, (title, p, p_formula) in enumerate(cases):

    # красивий консольний вивід
    case_name = f"ВИПАДОК {idx+1}"
    print("============================================")
    print(case_name)
    print("--------------------------------------------")
    print(f"p = {p_formula}")
    print(f"Числове значення p = {int(p)}")

    # стаціонарні точки
    x = sp.Symbol('x')
    eq = r * x * (1 - x / q) - p
    roots = sp.solve(eq, x)

    real_roots = []
    for root in roots:
        if sp.im(root) == 0:
            real_roots.append(float(root))

    if len(real_roots) == 0:
        print("Рівноважні точки: (немає)")
    else:
        formatted = ", ".join([str(round(r,2)) for r in real_roots])
        print(f"Рівноважні точки: {formatted}")

    print("Характеристика:")

    if len(real_roots) == 2:
        print("• ліва рівновага — нестійка")
        print("• права рівновага — стійка")
    elif len(real_roots) == 1:
        print("• єдина точка рівноваги — стійка")
    else:
        print("• вилов надто великий → популяція зникає")

    print("============================================\n")

    # початкові умови
    if len(real_roots) == 1:
        x1 = real_roots[0]
        x0_list = [x1 * 0.7, x1 * 1.3]

    elif len(real_roots) == 2:
        x1, x2 = sorted(real_roots)
        x0_list = [x1 * 0.7, (x1 + x2) / 2, x2 * 1.1]

    else:
        x0_list = [q * 0.2, q * 0.5, q * 0.9]

    # ================== ПОБУДОВА ГРАФІКА ==================
    plt.figure(figsize=(12, 6))
    plt.title(f"Динаміка популяції при {title}", fontproperties=prop, fontsize=18)

    for i, x0 in enumerate(x0_list):

        xs = np.zeros_like(t)
        xs[0] = x0

        # Рунге-Кутта 4
        for j in range(1, len(t)):
            k1 = f(xs[j-1], p)
            k2 = f(xs[j-1] + 0.5*dt*k1, p)
            k3 = f(xs[j-1] + 0.5*dt*k2, p)
            k4 = f(xs[j-1] + dt*k3, p)
            xs[j] = xs[j-1] + dt*(k1 + 2*k2 + 2*k3 + k4)/6
            xs[j] = max(xs[j], 0)

        plt.plot(t, xs, color=colors[i % len(colors)],
                 linewidth=2,
                 label=f"$x_0 = {x0:.1f}$")

    # стаціонарні рівні
    for rr in real_roots:
        plt.axhline(rr, color='red', linestyle='--', label=f"Стаціонарна: {rr:.0f}")

    plt.xlabel("Час t", fontproperties=prop, fontsize=13)
    plt.ylabel("Кількість риби x(t)", fontproperties=prop, fontsize=13)
    plt.grid(alpha=0.4)
    plt.legend(prop=prop)

    # ================== ТЕКСТОВИЙ БЛОК =====================
    formula = (
        r"$\frac{dx}{dt} = r x \left(1 - \frac{x}{q}\right) - p$"
        "\n"
        rf"$r = {r}, \; q = {q}, \; p = {p:.0f}$"
    )

    description = ""
    if len(real_roots) == 2:
        description = "Ліва рівновага — нестійка\nПрава рівновага — стійка"
    elif len(real_roots) == 1:
        description = "Єдина точка рівноваги — стійка"
    else:
        description = "Популяція зникає (вимирає)"

    # формула
    plt.text(
        1.03, 0.95,
        formula,
        fontproperties=prop,
        fontsize=16,
        transform=plt.gca().transAxes,
        verticalalignment='top'
    )

    # опис
    plt.text(
        1.03, 0.70,
        description,
        fontproperties=prop,
        fontsize=17,
        transform=plt.gca().transAxes,
        verticalalignment='top'
    )

    plt.tight_layout(rect=(0,0,0.8,1))
    plt.show()
