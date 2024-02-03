import random
from faker import Faker

def create_employees(number_of_employees: int) :
    assert number_of_employees > 0
    employees = []
    f = Faker()
    deps = ['HR', 'CUSTOMER SUPPORT', 'IT', 'MARKETING', 'R&D', 'SALES']
    branch_in = ['je', 'tl', 'st', 'bo', 'hu']
    for i in range(number_of_employees):
        fname = f.first_name()
        lname = f.last_name()
        age = f.random_int(min=20, max=70)
        dep_id = random.randint(1,6);
        salary = f.random_int(min=7*pow(age,2)*dep_id, max=15*pow(age,2)*dep_id, step=1000)
        department = deps[dep_id-1]
        branch_id = random.randint(1,5)
        email = fname.lower() + lname[0].upper() + "." + branch_in[branch_id-1] + '@comp.com'
        employees.append((fname, lname, salary, age, department, branch_id, email))
        # employees.append((place, salary))
    return employees


