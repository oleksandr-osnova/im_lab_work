import random

# Вхідні параметри
K = 2  # Кількість консультантів дорівнює M згідно з умовою
M = K  # Початкова кількість заявок (дорівнює K згідно з умовою)
a = random.choice([1, 2])  # Випадковий вибір значення a
h = a  # Тривалість часу обслуговування у годинах
N = K + a  # Загальна кількість консультантів згідно з умовою
arrival_intervals = [0.1, 0.2, 0.3, 0.4, 0.5]  # Інтервали між заявками у секундах
service_times = [1, 2, 3, 4, 5]  # Час обслуговування у секундах

# Початок моделювання
time = K  # Початковий час у секундах
queue = []  # Черга заявок

# Генерація заявок у зазначений часовий період
while time < K + h:  # h переведено в секунди
    time += random.choice(arrival_intervals)
    queue.append(time)

# Стан консультантів
consultants = [0] * N  # Початковий час звільнення кожного консультанта
wait_times = []  # Список часу очікування для кожної заявки

print(f"\nМоделювання роботи віртуального вузла обслуговування з {N} консультантами:\n")

# Обробка черги заявок
for i, arrival in enumerate(queue):
    # Знаходимо вільного консультанта
    free_consultant = consultants.index(min(consultants))

    # Обчислюємо час очікування заявки
    wait_time = max(0, consultants[free_consultant] - arrival)

    print(f"Заявка {i+1}:")
    print(f"  Час приходу: {arrival:.2f} сек.")
    print(f"  Час очікування в черзі: {wait_time:.2f} сек.")

    # Оновлюємо час завершення обслуговування для обраного консультанта
    consultants[free_consultant] = arrival + wait_time + random.choice(service_times)

    print(f"  Консультант {free_consultant+1} звільниться о {consultants[free_consultant]:.2f} сек.\n")

    wait_times.append(wait_time)

# Обчислення середнього часу очікування і часу закриття вузла
average_wait_time = sum(wait_times) / len(wait_times) if wait_times else 0
closure_time = max(consultants)

print(f"\nПідсумки:")
print(f"  Загальна кількість обслуговуваних клієнтів: {len(queue)}")
print(f"  Середній час очікування: {average_wait_time:.2f} сек.")
print(f"  Час закриття вузла: {closure_time:.2f} сек.")
