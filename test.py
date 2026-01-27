def binarySearch(arr, targetVal):
  left = 0
  count = 0
  right = len(arr) - 1

  while left <= right:
    count +=1
    mid = (left + right) // 2

    if arr[mid] == targetVal:
      print(count)
      return mid

    if arr[mid] < targetVal:
      left = mid + 1
    else:
      right = mid - 1

  print(count)  
  return -1

mylist = [2,9,42,76,79,80,81,82,99,180]
x = 77

result = binarySearch(mylist, x)

if result != -1:
  print("Found at index", result)
else:
  print("Not found")