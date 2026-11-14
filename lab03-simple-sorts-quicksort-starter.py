#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations
import matplotlib.pyplot as plt
import argparse
import random
import statistics
import time

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: TODO (обосновать в отчёте).

    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    a = a.copy()
    counter = 0
    swaps = 0

    for i in range(len(a)):
        has_swapped = False
        for j in range(0, len(a) - 1 - i):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                counter += 1
                swaps += 1
                has_swapped = True
            else:
                counter += 1
        if has_swapped == False:
            break
    return a, counter, swaps

    # TODO: реализовать; считать сравнения и обмены


def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO (лучший/худший случаи)."""
    a = a.copy()
    counter = 0
    swaps = 0
    for i in range(1,len(a)):
        j=i
        while j>0:
            counter += 1
            if a[j]<a[j-1]:
                a[j], a[j-1] = a[j-1], a[j]
                swaps += 1
                j=j-1
            else:
                break
    return a, counter, swaps
    # TODO: реализовать; считать сравнения и перемещения (сдвиги)



def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO (почему не зависит от входа?)."""
    a = a.copy()
    counter = 0
    swaps = 0
    for i in range(len(a)):
        first = i
        for j in range(i+1, len(a)):
            counter += 1
            if a[j] < a[first]:
                first = j
        if first != i:
            a[i], a[first] = a[first], a[i]
            swaps += 1
    return a, counter, swaps

    # TODO: реализовать; считать сравнения и обмены



# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность: в среднем TODO, в худшем случае TODO (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    a = a.copy()
    smaller, larger , equal =[],[],[]
    if rng is None:
        rng = random.Random()
    if len(a) <= 1:
        return a.copy()
    pivot = a[rng.randrange(0, len(a))]
    for i in range(len(a)):
        if a[i] < pivot:
            smaller.append(a[i])
        if a[i] > pivot:
            larger.append(a[i])
        if a[i] == pivot:
            equal .append(a[i])
    return quick_sort(smaller, rng)+equal+quick_sort(larger, rng)
    # TODO: реализовать (рекурсивно или циклом со стеком);
    # TODO: опорный элемент — a[rng.randrange(lo, hi)], не первый и не последний.


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.
    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """

    pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    print("Исходный список:", pairs)

    print("Bubble Sort:", bubble_sort(pairs)[0])
    print("Insertion Sort:", insertion_sort(pairs)[0])
    print("Selection Sort:", selection_sort(pairs)[0])
    print("Quick Sort:", quick_sort(pairs, random.Random(42)))




# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)



def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов; результат — таблица в stdout."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]

    for name, fn, sizes in plans:
        print(f"\n{name}:")
        results = {}

        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                t = bench(fn, data)
                print(f"  n={n:>7}  вход={cls:<13} t={t:.6f} c")

                # TODO: таблица счётчиков сравнений и обменов
                if name != "quick_sort":
                    _, comparisons, swaps = globals()[name](data.copy())
                    print(f"    сравнений={comparisons}, обменов/перемещений={swaps}")

                if cls not in results:
                    results[cls] = ([], [])
                results[cls][0].append(n)
                results[cls][1].append(t)

        # TODO: построить log-log графики
        for cls, (ns, times) in results.items():
            plt.loglog(ns, times, marker="o", label=cls)

        plt.xlabel("Размер массива n")
        plt.ylabel("Время (с)")
        plt.title(name)
        plt.legend()
        plt.grid(True)
        plt.show()

        # TODO: сопоставить наклоны с O(n^2) и O(n log n)
        print("\nТеоретическая сложность:")
        if name == "quick_sort":
            print("O(n log n) — средний случай")
        else:
            print("O(n²) — общий случай")

        if name == "insertion_sort":
            print("На отсортированном входе O(n): элементы не сдвигаются.")

        if name == "bubble_sort":
            print("На отсортированном входе O(n), если реализован досрочный выход.")

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
