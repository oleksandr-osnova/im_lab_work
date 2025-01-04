import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import plotly.graph_objects as go
import plotly.io as pio

# Root variables
dataset_folder = pathlib.Path('../../data/lab_2')
output_data_folder = dataset_folder / "output"

# Явно задані діапазони для X1, X2, X3
x1_ranges = [(0, 24, 0), (25, 59, 1), (60, 77, 2), (78, 87, 3), (88, 95, 4), (96, 99, 5)]
x2_ranges = [(0, 74, "Yes"), (75, 99, "No")]
x3_ranges = [(0, 39, 2), (40, 84, 4), (85, 99, 6)]

# Функція для генерації випадкових чисел експоненціального розподілу
def generate_random_number(size=100):
    lambda_param = 0.01 # Параметр λ для експоненціального розподілу
    return (np.random.exponential(scale=1/lambda_param, size=size) % 100).astype(int)

# Функція для генерації значення на основі діапазонів
def generate_from_ranges(random_numbers, ranges):
    results = []
    for num in random_numbers:
        for low, high, value in ranges:
            if low <= num <= high:
                results.append(value)
                break
    return results

def analyze(passers_by_count = 100):
    # Генерація випадкових чисел для X1, X2, X3 на базі експоненціального розподілу
    random_numbers_x1 = generate_random_number(passers_by_count)
    random_numbers_x2 = generate_random_number(passers_by_count)
    random_numbers_x3 = generate_random_number(passers_by_count)

    # Генерація значень для X1, X2, X3 на основі діапазонів
    time_intervals = generate_from_ranges(random_numbers_x1, x1_ranges)
    agreement_status = generate_from_ranges(random_numbers_x2, x2_ranges)
    durations = generate_from_ranges(random_numbers_x3, x3_ranges)

    # Розрахунок часу початку та закінчення інтерв'ю
    arrival_times = []
    start_times = []
    end_times = []
    current_time = 0

    for passers_by_index in range(passers_by_count):
        current_time += time_intervals[passers_by_index]  # Додаємо час між появами перехожого
        arrival_times.append(current_time)  # Час появи перехожого
        last_end_time = max([t for t in end_times if t is not None], default=0)
        if current_time < last_end_time:
            agreement_status[passers_by_index] = "Busy"
            start_times.append(None)
            end_times.append(None)
            continue

        if agreement_status[passers_by_index] == "Yes":
            start_time = current_time  # Час початку інтерв'ю
            end_time = start_time + durations[passers_by_index]  # Час завершення інтерв'ю
            start_times.append(start_time)
            end_times.append(end_time)
        else:
            start_times.append(None)
            end_times.append(None)

    return list(range(1, passers_by_count + 1)), random_numbers_x1, time_intervals, arrival_times, random_numbers_x2, agreement_status, random_numbers_x3, durations, start_times, end_times

def save_table(table, title = "table", annotation = None):
    file_name = output_data_folder / (title + ".html")
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(table.columns),
            font=dict(size=16),
        ),
        cells=dict(
            values=[table[col] for col in table.columns],
            font=dict(size=16),
            height=35,
        )
    )])
    if annotation:
        font_size = 18
        line_height = font_size * 1.15
        margin_top = (annotation.count("<br>") + 2) * line_height
        fig.add_annotation(
            text=annotation,
            xref="paper", yref="paper", x=0.5, y=1, showarrow=False,
            font=dict(size=font_size),
            xanchor='center', align='left',
            yanchor='bottom',
        )
        fig.update_layout(margin=dict(t=margin_top))
    html_content = pio.to_html(fig, full_html=True, include_plotlyjs='cdn')
    # write table
    with open(file_name, "w") as file:
        file.write(html_content)

def save_analyzed_table(passers_by_indexes, random_numbers_x1, time_intervals, arrival_times, random_numbers_x2, agreement_status, random_numbers_x3, durations, start_times, end_times):
    df = pd.DataFrame(list(zip(
        passers_by_indexes,
        random_numbers_x1,
        time_intervals,
        arrival_times,
        random_numbers_x2,
        agreement_status,
        random_numbers_x3,
        durations,
        start_times,
        end_times
    )), columns=["№", "Х1", "ІНТ(хв)", "ЧП(хв)", "Х2", "СТТС", "Х3", "ТРВ(хв)", "П(хв)", "К(хв)"])
    save_table(df, f"{len(passers_by_indexes)}_results", (
        f"Результати опитування {len(passers_by_indexes)} перехожих.<br>"
        "Пояснення:<br>"
        "- ІНТ(хв): Інтервал для Х1<br>"
        "- ЧП(хв): Час появи<br>"
        "- СТТС: Статус згоди перехожого для Х2 або зайнятості оператора<br>"
        "- ТРВ(хв): Тривалість анкетування для Х3<br>"
        "- П(хв): Час початку анкетування<br>"
        "- К(хв): Час кінця анкетування<br>"
    ))

def show_formal_system_model(passers_by_indexes, random_numbers_x1, time_intervals, arrival_times, random_numbers_x2, agreement_status, random_numbers_x3, durations, start_times, end_times):
    fig_time_allocation = plt.figure('TimeAllocation')
    plt.hist(time_intervals, bins=range(max(time_intervals)+1), alpha=0.7, color='skyblue', edgecolor='black')
    plt.title("Розподіл часу між появами перехожих (X₁) -> Приклад формальної системи моделі")
    plt.xlabel("Час між появами (хвилини)")
    plt.ylabel("Кількість перехожих")
    plt.grid(True)
    plt.show()
    fig_time_allocation.savefig(output_data_folder / 'TimeAllocation.png')

    fig_duration_allocation = plt.figure('DurationAllocation')
    plt.hist(durations, bins=range(min(durations), max(durations)+2), alpha=0.7, color='green', edgecolor='black')
    plt.title("Розподіл тривалості інтерв'ю (X₃) -> Приклад формальної системи моделі")
    plt.xlabel("Тривалість інтерв'ю (хвилини)")
    plt.ylabel("Кількість інтерв'ю")
    plt.grid(True)
    plt.show()
    fig_duration_allocation.savefig(output_data_folder / 'DurationAllocation.png')

def show_simulation_results(passers_by_indexes, random_numbers_x1, time_intervals, arrival_times, random_numbers_x2, agreement_status, random_numbers_x3, durations, start_times, end_times):
    # Розрахунок загальної тривалості та вартості
    cost_per_minute = 2  # Вартість за хвилину
    costs = [
        duration * cost_per_minute if agreement == "Yes" else 0
        for duration, agreement in zip(durations, agreement_status)
    ]
    total_cost = sum(costs)
    total_interview_time = sum([end - start for start, end in zip(start_times, end_times) if start is not None])

    print(f"Загальна тривалість анкетування: {total_interview_time} хвилин")
    print(f"Загальна вартість анкетування: {total_cost} грн")

    # Візуалізація результатів
    fig_simulation_results = plt.figure('SimulationResults', figsize=(10, 6))

    for i in range(len(passers_by_indexes)):
        if start_times[i] is not None:
            plt.hlines(i + 1, start_times[i], end_times[i], colors='blue', linewidth=5)

    plt.title(f"Временная шкала анкетирования\nЗагальна тривалість: {total_interview_time} хвилин, Загальна вартість: {total_cost} грн")
    plt.xlabel("Час (хвилини)")
    plt.ylabel("Перехожі")
    plt.grid(True)
    plt.show()
    fig_simulation_results.savefig(output_data_folder / 'SimulationResults.png')


def show_passers_by_dependency():
    passers_by_cunts = range(10, 101, 10)
    total_times = []

    for count in passers_by_cunts:
        _, _, _, _, _, _, _, _, start_times, end_times = analyze(count)
        total_time = sum([end - start for start, end in zip(start_times, end_times) if start is not None])
        total_times.append(total_time)

    fig_passers_by_dependency = plt.figure('PassersByDependency')
    plt.plot(passers_by_cunts, total_times, marker='o', linestyle='-')
    plt.title("Залежність загального часу від кількості перехожих")
    plt.xlabel("Кількість перехожих")
    plt.ylabel("Загальний час анкетування (хвилини)")
    plt.grid(True)
    plt.show()
    fig_passers_by_dependency.savefig(output_data_folder / 'PassersByDependency.png')

