from operator import itemgetter
import itertools

def appearance(intervals):
    timeline = []
    for key, value in test['data'].items():
        value = rm_nested_segments(value) # убираем вложенные отрезки (если таковые есть)
        value = sorted(
            [(elem, -1 if idx%2 else 1) for idx, elem in enumerate(value)]
        ) # список точек: начало интервала ставим (1), конец интервала ставим (-1)
        cut_idxes = []
        for i in range(len(value)):
            if value[i][1] == 1 and value[i-1][1] == 1: # случай "два начала подряд"
                cut_idxes.append(i)
            if value[i][1] == -1 and value[i-1][1] == -1: # случай "два конца подряд"
                cut_idxes.append(i-1)
        for i in reversed(cut_idxes): # убираем уже определенные лишние начала и концы
            value.remove(value[i])
        timeline.extend(value)
    timeline.sort()
    count, start, intersection = 0, 0, 0
    for event in timeline:
        count += event[1]
        if count == 3:                       # три события пересеклись, начался общий интервал
            start = event[0]                 # записали время, когда начался общий интервал
        if count == 2 and start > 0:         # count изменился 2 и кончился интервал (start > 0)
            intersection += event[0] - start # вычисляем длину интервала присутствия
            start = 0
    return intersection

tests = [
        {'data': {'lesson': [1594663200, 1594666800],
                  'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                  'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
         'answer': 3117
         },
        {'data': {'lesson': [1594702800, 1594706400],
                  'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                            1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                            1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                            1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                  'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
         'answer': 3577
         },
        {'data': {'lesson': [1594692000, 1594695600],
                  'pupil': [1594692033, 1594696347],
                  'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
         'answer': 3565
         },
    ]

def rm_nested_segments(segm): # nested segments - вложенные отрезки
    cuts = sorted([[segm[i], segm[i+1]] for i in range(0, len(segm) - 1, 2)], key=itemgetter(0))
    indxs = set()
    for i in range(len(cuts)):
        for j in range(i+1,len(cuts)):
            if cuts[i][1] >= cuts[j][1]:
                indxs.add(j)
    for j in sorted(list(indxs), reverse=True):
        cuts.remove(cuts[j])
    return list(itertools.chain(*cuts))

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
