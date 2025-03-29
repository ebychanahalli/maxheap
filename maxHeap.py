__all__ = ['heappush', 'heappop', 'heapify', 'heapreplace', 'merge',
           'nlargest', 'nsmallest', 'heappushpop']

def heappush(heap, item):
    """Push item onto max-heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown_max(heap, 0, len(heap) - 1)

def heappop(heap):
    """Pop the largest item off the max-heap, maintaining the heap invariant."""
    lastelt = heap.pop()
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup_max(heap, 0)
        return returnitem
    return lastelt

def heapreplace(heap, item):
    """Pop and return the current largest value, and add the new item."""
    returnitem = heap[0]
    heap[0] = item
    _siftup_max(heap, 0)
    return returnitem

def heappushpop(heap, item):
    """Fast version of a heappush followed by a heappop on a max-heap."""
    if heap and heap[0] > item:
        item, heap[0] = heap[0], item
        _siftup_max(heap, 0)
    return item

def heapify(x):
    """Transform list into a max-heap, in-place, in O(len(x)) time."""
    _heapify_max(x)

def _siftdown_max(heap, startpos, pos):
    """Maxheap variant of siftdown"""
    newitem = heap[pos]
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if parent < newitem:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

def _siftup_max(heap, pos):
    """Maxheap variant of siftup"""
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    childpos = 2 * pos + 1
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] > heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2 * pos + 1
    heap[pos] = newitem
    _siftdown_max(heap, startpos, pos)

def _heapify_max(x):
    """Transform list into a maxheap, in-place, in O(len(x)) time."""
    n = len(x)
    for i in reversed(range(n // 2)):
        _siftup_max(x, i)

def merge(*iterables, key=None, reverse=False):
    '''Merge multiple sorted inputs into a single sorted output (for max-heap).'''
    h = []
    h_append = h.append

    if not reverse:
        _heapify = _heapify_max
        _heappop = heappop
        _heapreplace = heapreplace
        direction = 1
    else:
        raise NotImplementedError("reverse=True not supported for max-heap merge")

    if key is None:
        for order, it in enumerate(map(iter, iterables)):
            try:
                next = it.__next__
                h_append([next(), order * direction, next])
            except StopIteration:
                pass
        _heapify(h)
        while len(h) > 1:
            try:
                while True:
                    value, order, next = s = h[0]
                    yield value
                    s[0] = next()
                    _heapreplace(h, s)
            except StopIteration:
                _heappop(h)
        if h:
            value, order, next = h[0]
            yield value
            yield from next.__self__
        return

    for order, it in enumerate(map(iter, iterables)):
        try:
            next = it.__next__
            value = next()
            h_append([key(value), order * direction, value, next])
        except StopIteration:
            pass
    _heapify(h)
    while len(h) > 1:
        try:
            while True:
                key_value, order, value, next = s = h[0]
                yield value
                value = next()
                s[0] = key(value)
                s[2] = value
                _heapreplace(h, s)
        except StopIteration:
            _heappop(h)
    if h:
        key_value, order, value, next = h[0]
        yield value
        yield from next.__self__

def nlargest(n, iterable, key=None):
    """Find the n largest elements in a dataset using a max-heap."""
    try:
        size = len(iterable)
    except (TypeError, AttributeError):
        iterable = list(iterable)
        size = len(iterable)

    if n <= 0:
        return []

    return sorted(iterable, key=key, reverse=True)[:n]

def nsmallest(n, iterable, key=None):
    """Find the n smallest elements in a dataset using a max-heap."""
    if n <= 0:
        return []

    # Maintain a max-heap of size n
    it = iter(iterable)
    if key is None:
        result = [(elem, i) for i, elem in zip(range(n), it)]
        if not result:
            return []
        _heapify_max(result)
        top = result[0][0]
        order = n
        for elem in it:
            if elem < top:
                result[0] = (elem, order)
                _siftup_max(result, 0)
                top = result[0][0]
                order += 1
        result.sort()
        return [elem for (elem, _) in result]
    else:
        result = [(key(elem), i, elem) for i, elem in zip(range(n), it)]
        if not result:
            return []
        _heapify_max(result)
        top = result[0][0]
        order = n
        for elem in it:
            k = key(elem)
            if k < top:
                result[0] = (k, order, elem)
                _siftup_max(result, 0)
                top = result[0][0]
                order += 1
        result.sort()
        return [elem for (_, _, elem) in result]
