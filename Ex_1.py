from math import floor

def Interpolation_Search(arr, target):
    low = 0
    high = len(arr) -1
    while low <= high and target >= arr[low] and target <= arr[high]:
        if arr[low] == target:
            return low
        else:
            pos = floor(low + ((target - arr[low]) * (high - low))/ (arr [high] - arr[low] ))
            if arr[pos] == target:
                return pos
            elif arr[pos] < target :
                low = pos + 1
            else: 
                high = pos - 1
            return -1

arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
target = int(input("Enter a target to search: "))

search = Interpolation_Search(arr,target)

if search != -1:
    print("The Target is found in", search ,)
else:
    print("Element not Found ...")


