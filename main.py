class Student:
    students_list = []

    def __init__(self, first_name, last_name, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.finished_courses = []
        self.courses_progress = []
        self.grade = {}
        self.students_list.append(self)

    def add_finish_courses(self, course):
        if course not in self.finished_courses:
            self.finished_courses.append(course)
        else:
            print('Error')

    def rate_hw(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in self.courses_progress and course in lecturer.courses_attached
                or course in self.finished_courses):
            if course in lecturer.lecture_grade:
                lecturer.lecture_grade[course] += [grade]
            else:
                lecturer.lecture_grade[course] = [grade]
        else:
            print('Error')

    def average_grade(self):
        avg_lec = {val: round((sum(items) / len(items)), 2) for val, items in self.grade.items()}
        res = []
        for key, val in avg_lec.items():
            res.append(f'Средняя оценка домашних заданий по курсу {key}: {val}')
        return '\n'.join(res)

    def general_average(self):
        avg_gen = [i for val in self.grade.values() for i in val]
        return round(sum(avg_gen) / len(avg_gen), 2)

    def __str__(self):
        res = f'Имя: {self.first_name} \nФамилия: {self.last_name} \n{self.average_grade()} \n' \
              f'Общая средняя оценка: {self.general_average()} \n' \
              f'Курсы в процессе изучения: {",".join(self.courses_progress)} \n' \
              f'Завершенные курсы: {", ".join(self.finished_courses)}'
        return res

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.general_average() < other.general_average()
        else:
            print(other, 'not Student!')
            return


class Mentor:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.courses_attached = []


class Lecturer(Mentor):  # Лекторы
    lecturer_list = []

    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.lecture_grade = {}
        self.lecturer_list.append(self)

    def add_courses(self, course):
        if course not in self.courses_attached:
            self.courses_attached.append(course)
        else:
            print('The course has already been added')

    def average_grade(self):
        avg_lec = {val: round(sum(items) / len(items), 2) for val, items in self.lecture_grade.items()}
        res = []
        for key, val in avg_lec.items():
            res.append(f'Средняя оценка лекций по курсу {key}: {val}')
        return '\n'.join(res)

    def general_average(self):
        avg_gen = [i for val in self.lecture_grade.values() for i in val]
        return round(sum(avg_gen) / len(avg_gen), 2)

    def __str__(self):
        res = f'Имя: {self.first_name} \nФамилия: {self.last_name} \n{self.average_grade()} \n' \
              f'Общая средняя оценка лекций {self.general_average()}'
        return res

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.general_average() < other.general_average()
        else:
            print(other, 'not Lecturer!')
            return


class Reviewer(Mentor):  # Эксперты - проверяющие задания
    def __str__(self):
        res = f'Имя: {self.first_name} \nФамилия: {self.last_name}'
        return res

    def add_courses(self, course):
        Lecturer.add_courses(self, course)

    def _rate_hw(self, students, course, grade):
        if isinstance(students, Student) and course in self.courses_attached and course in students.courses_progress:
            if course in students.grade:
                students.grade[course] += [grade]
            else:
                students.grade[course] = [grade]
        else:
            print('Error')


aleks = Student('Aleksandr', 'Mamontov', 'man')  # объявим экземпляр класса Студент
aleks.finished_courses += ['sql', 'git']  # добавили завершенные курсы
aleks.courses_progress += ['python']  # добавили, курс, изучаемый в настоящее время
aleks.grade['python'] = [10, 10, 10, 8, 8]
aleks.grade['sql'] = [10, 10, 2, 10, 7]

sergey = Student('Sergey', 'Lazarev', 'man')
sergey.finished_courses += ['sql', 'git']
sergey.courses_progress += ['python']
sergey.grade['python'] = [10, 8, 7, 8, 8]
sergey.grade['sql'] = [10, 4, 2, 10, 7]

oleg = Lecturer('Oleg', 'Bulygin')  # объявили экземпляр класса Лектор
oleg.courses_attached = ['python']  # добавили курс, по которому лектор ведет лекцию
oleg.add_courses('git')  # реализация метода класса Лектор добавления курса
oleg.add_courses('sql')

ivan = Lecturer('Ivan', 'Filolov')
ivan.courses_attached = ['python']
ivan.add_courses('git')
ivan.add_courses('sql')

# print(f'{oleg.first_name} {oleg.last_name} преподает следующие курсы:', *oleg.courses_attached)

aleks.rate_hw(oleg, 'python', 10)  # реализовали метод класса Студент, позволяющий оценивать лекции
aleks.rate_hw(oleg, 'python', 9)
aleks.rate_hw(oleg, 'git', 10)
aleks.rate_hw(oleg, 'sql', 2)

sergey.rate_hw(ivan, 'python', 7)
sergey.rate_hw(ivan, 'python', 5)
sergey.rate_hw(ivan, 'git', 10)
sergey.rate_hw(ivan, 'sql', 10)


some_reviewer = Reviewer('Хороший', 'Эксперт')  # объявили экземпляр класса Эксперт
some_reviewer.courses_attached.append('python')  # в явном виде добавили курс, который Эксперт может оценивать
some_reviewer.add_courses('git')  # с помощью прямого наследования метода из класса Лектора добавляем курс
some_reviewer._rate_hw(aleks, 'python', 9)  # реализация метода класса Эксперт оценивание студента


# функция предназначена для автоматизации обработки метода оценивания
# def some_reviewer_rate_hw(some_reviewer, student):
#     if isinstance(some_reviewer, Reviewer) and isinstance(student, Student):
#         course = input('Введите название курса для его оценки\n# ').lower()
#         grade = int(input('Введите оценку от 0 до 10\n# '))
#         some_reviewer._rate_hw(student, course, grade)
#     else:
#         print('Error')
#
# some_reviewer_rate_hw(some_reviewer, aleks)


print()
print('#' * 10, 'Задача 3.1, п. 1')
print(some_reviewer)
print('#' * 10, 'Задача 3.1, п. 2')
print(oleg)
print(ivan)
print('#' * 10, 'Задача 3.1, п. 3')
print(aleks)
print('#' * 10, 'Задача 3.2')
print(aleks < sergey)
print(oleg > ivan)
print('#' * 10, 'Задача 4')


def averege_greade_courses_students(students, course):
    grade = []
    for i in students:
        for courses, grades in i.grade.items():
            if courses == course:
                grade.extend(grades)
    if len(grade) > 0:
        res = f'Средняя оценка студентов по курсу {course}: {round(sum(grade) / len(grade), 2)}'
        return res
    else:
        res = f'Курс {course} еще не оценивался преподавателем'
        return res

def averege_greade_courses_lecturers(lecturers, course):
    grade = []
    for lector in lecturers:
        for courses, grades in lector.lecture_grade.items():
            if courses == course:
                grade.extend(grades)
    if len(grade) > 0:
        res = f'Средняя оценка лекторов по курсу {course}: {round(sum(grade) / len(grade), 2)}'
        return res
    else:
        res = f'Курс {course} еще не оценивался студентами'
        return res


print(averege_greade_courses_students(Student.students_list, 'sql'))
print(averege_greade_courses_lecturers(Lecturer.lecturer_list, 'python'))