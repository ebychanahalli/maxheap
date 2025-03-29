import maxHeap

def test_maxheap():

    # Test heappop
    heap = [1, 2, 3, 4, 5]
    maxHeap.heapify(heap)
    assert maxHeap.heappop(heap) == 5
    assert heap == [4, 2, 3, 1]

    # Test heapreplace
    heap = [1, 2, 3, 4, 5]
    maxHeap.heapify(heap)
    assert maxHeap.heapreplace(heap, 6) == 5
    print(heap)
    assert maxHeap.heappop(heap) == 6
    assert maxHeap.heappop(heap) == 4
    assert maxHeap.heappop(heap) == 3
    assert maxHeap.heappop(heap) == 2
    assert maxHeap.heappop(heap) == 1

    # Test heappushpop
    heap = [1, 2, -3, 4, -5]
    maxHeap.heapify(heap)
    assert maxHeap.heappushpop(heap, 0) == 4
    assert maxHeap.heappushpop(heap, 6) == 6
    assert maxHeap.heappushpop(heap, 3) == 3
    assert maxHeap.heappushpop(heap, -1) == 2
    assert maxHeap.heappushpop(heap, -1) == 1
    print(maxHeap.heappop(heap))
    print(maxHeap.heappop(heap))
    print(maxHeap.heappop(heap))
    print(maxHeap.heappop(heap))
    print(maxHeap.heappop(heap))


    print('All tests pass')

test_maxheap()