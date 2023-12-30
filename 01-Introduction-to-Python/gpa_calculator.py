from typing import List
from college import Student, Course
import utils

def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    id = student.id
    my_courses = [c for c in courses if id in c.grades]
    if len(my_courses) == 0:
        return 0
    hours = sum([c.hours for c in my_courses])
    if hours == 0:
        return 0
    gpa = sum([c.hours * Course.convert_grade_to_points(c.grades[id]) for c in my_courses]) / hours
    return gpa