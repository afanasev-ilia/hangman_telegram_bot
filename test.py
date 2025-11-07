athletes = [('Дима', 10, 130, 35), ('Тимур', 11, 135, 39), ('Руслан', 9, 140, 33), ('Рустам', 10, 128, 30), ('Амир', 16, 170, 70), ('Рома', 16, 188, 100), ('Матвей', 17, 168, 68), ('Петя', 15, 190, 90)]


def compare_name(point):
    return point[0]


def compare_age(point):
    return point[1]


def compare_height(point):
    return point[2]


def compare_weight(point):
    return point[3]


compares = [None, compare_name, compare_age, compare_height, compare_weight]

[print(*item) for item in sorted(athletes, key=compares[1])]
