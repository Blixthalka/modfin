import requests
import datetime
from heapq import heappush, heappushpop


def main():
    end = datetime.date.today() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=366)
    data = requests.get('http://fx.modfin.se/' + str(start) + '/' + str(end) + '/?base=usd&symbols=sek').json()

    median_calc = MedianCalculator()
    for item in data:
        median_calc.insert_value(float(item['rates']['SEK']))

    print 'median: ', median_calc.get_median()


class MedianCalculator:

    def __init__(self):
        self.higher_heap = []   # min heap
        self.lower_heap = []    # max heap, thus contains negated values
        self.median = None

    def insert_value(self, value):
        if self.median is None:
            self.median = value
        elif len(self.higher_heap) == len(self.lower_heap):
            if value > self.median:
                heappush(self.higher_heap, value)
            else:
                heappush(self.lower_heap, value * -1)
        elif len(self.higher_heap) > len(self.lower_heap):
            if value > self.median:
                heappush(self.lower_heap, self.median * -1)
                self.median = heappushpop(self.higher_heap, value)
            else:
                heappush(self.lower_heap, value * -1)
        elif len(self.higher_heap) < len(self.lower_heap):
            if value > self.median:
                heappush(self.higher_heap, value)
            else:
                heappush(self.higher_heap, self.median)
                self.median = heappushpop(self.lower_heap, value * -1) * -1
        return self.get_median()

    def get_median(self):
        if len(self.higher_heap) < len(self.lower_heap):
            return (self.median + self.lower_heap[0] * -1) / 2
        elif len(self.higher_heap) > len(self.lower_heap):
            return (self.median + self.higher_heap[0]) / 2
        else:
            return self.median

if __name__ == "__main__":
    main()
