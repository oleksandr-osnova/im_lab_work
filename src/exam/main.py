# Імпорт необхідних бібліотек
from utils import *

def main():
    results_for_100_passers_by = analyze(100)
    save_analyzed_table(*results_for_100_passers_by)

    show_formal_system_model(*results_for_100_passers_by)
    show_simulation_results(*results_for_100_passers_by)
    show_passers_by_dependency()

    results_for_1000_passers_by = analyze(1000)
    results_for_10000_passers_by = analyze(10000)
    save_analyzed_table(*results_for_1000_passers_by)
    save_analyzed_table(*results_for_10000_passers_by)

if __name__ == "__main__":
    main()