import random
import time

# 퀵 정렬 함수
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    less_arr, equal_arr, greater_arr = [], [], []
    for num in arr:
        if num < pivot:
            less_arr.append(num)
        elif num > pivot:
            greater_arr.append(num)
        else:
            equal_arr.append(num)
    return quick_sort(less_arr) + equal_arr + quick_sort(greater_arr)

# 버블 정렬 함수
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 10개의 랜덤 데이터 생성
data = [random.randint(1, 100) for _ in range(10)]
print("소스 데이터 배열:", data)

# 퀵 정렬 시간 측정
start_time = time.time()
quick_sorted = quick_sort(data)
end_time = time.time()
quick_sort_time = end_time - start_time

# 버블 정렬 시간 측정
start_time = time.time()
bubble_sorted = bubble_sort(data)
end_time = time.time()
bubble_sort_time = end_time - start_time

# 결과 출력
print("\n퀵 정렬 결과:", quick_sorted)
print("퀵 정렬 소요 시간:", quick_sort_time)
print("\n버블 정렬 결과:", bubble_sorted)
print("버블 정렬 소요 시간:", bubble_sort_time)