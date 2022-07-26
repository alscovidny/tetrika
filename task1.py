def task(array):
    # самое простое решение
    return array.find('0')

    # решение без использования строковых методов
    # for index, elem in enumerate(array):
    #     if elem == '0':
    #         return index

if __name__ == '__main__':
    print(task("111111111110000000000000000"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
