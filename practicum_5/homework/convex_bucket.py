from time import perf_counter

import numpy as np
from numpy.typing import NDArray

from src.plotting import plot_points

# определим, слева или справа от вектора AB находится точка С:
# векторное произведение AB и BC больше нуля, если второй вектор направлен влево от первого и меньше нуля, если вправо
def location(a,b,c):
    return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])

# сортировка слиянием точек по степени левизны
def merge_sort(points, arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    left = merge_sort(points, left)
    right = merge_sort(points, right)
    return merge(points, left, right)

def merge(points, left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if (location(p0, points[left[i]], points[right[j]])<=0):
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
    result += left[i:]
    result += right[j:]
    return result

def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""
    clockwise_sorted_ch = []

    # создадим массив с индексами точек в массиве points
    a = [i for i in range(len(points))]

    # найдем стартовую точку и прономеруем ее первой
    temp_minx = points[0][0]
    temp_miny = points[0][1]
    temp_index = 0
    for i in range(1, len(points)):
        if points[i][0] < temp_minx or (points[i][0] == temp_minx and points[i][1] < temp_miny):
            temp_minx = points[i][0]
            temp_miny = points[i][1]
            temp_index = i
    a[0], a[temp_index] = a[temp_index], a[0]

    # отсортируем все точки, кроме стартовой, по степени их левизны относительно стартовой
    global p0
    p0 = points[a[0]]
    a0 = a[0]
    a.pop(0)
    a=merge_sort(points, a)
    a.insert(0, a0)

    # уберем ребра, в которых выполняется правый поворот
    ans = [a[0], a[1]]
    for i in range(2, len(a)):
        while len(ans) > 1 and location(points[ans[-2]], points[ans[-1]], points[a[i]]) <= 0:
            ans.pop()
        ans.append(a[i])

    # найдем конечную точку
    temp_maxx = float('-inf')
    temp_miny = float('inf')
    temp_index = 0
    for i in range(1, len(points)):
        if points[i][0] > temp_maxx or (points[i][0] == temp_maxx and points[i][1] < temp_miny):
            temp_maxx = points[i][0]
            temp_miny = points[i][1]
            temp_index = i


    for i in ans:
        clockwise_sorted_ch.append(points[i])
        if i == temp_index: break

    clockwise_sorted_ch += clockwise_sorted_ch[-2::-1]
    return np.array(clockwise_sorted_ch)


if __name__ == "__main__":
    for i in range(1, 11):
        txtpath = f"practicum_5/points_{i}.txt"
        points = np.loadtxt(txtpath)
        print(f"Processing {txtpath}")
        print("-" * 32)
        t_start = perf_counter()
        ch = convex_bucket(points)
        t_end = perf_counter()
        print(f"Elapsed time: {t_end - t_start} sec")
        plot_points(points, convex_hull=ch, markersize=20)
        print()
