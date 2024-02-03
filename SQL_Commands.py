# ###################### NAMES
name_db_office_workers = "office_workers"
name_table_emp = "employees"
name_table_branches = "branches"

# ###################### TABLE_DEFS
create_employees_table = f"CREATE TABLE {name_table_emp}  ( \
                            id INT PRIMARY KEY AUTO_INCREMENT,\
                            first_name VARCHAR(50) NOT NULL, \
                            last_name VARCHAR(50) NOT NULL, \
                            salary INT DEFAULT 0, \
                            age INT, \
                            department VARCHAR(20), \
                            branch_id INT, \
                            email VARCHAR(60),\
                            CHECK (age >= 18));"

create_branches_table = f"CREATE TABLE branches(\
                            id INT PRIMARY KEY AUTO_INCREMENT,\
                            branch_name VARCHAR(20),\
                            address VARCHAR(100) NOT NULL,\
                            budget INT,\
                            CHECK(budget >= 0));"

# ###################### BRANCH VALS
branch_info = [('JERUSALEM', 'YAFFO 27, JERUSALEM, ISRAEL', 12000000),
               ('TLV', 'YARKON 44, TEL AVIV, ISRAEL', 10000000),
               ('STOCKHOLM', '5 STORGATAN, STOCKHOLM, SWEDEN', 8000000),
               ('BOULDER', '256 MAIN STREET, BOULDER, COLORADO-USA', 10000000),
               ('HOUSTON', '101 OAK AVENUE, HOUSTON, TEXAS-USA', 7000000)]

####################### ACTIONS
act_insert_workers = f"INSERT INTO {name_table_emp} " \
                     f"(first_name, last_name, salary, age, department, branch_id, email)" \
                     f" VALUES (%s, %s, %s, %s, %s, %s, %s)"
act_insert_branches = f"INSERT INTO {name_table_branches} " \
                     f"(branch_name, address, budget)" \
                     f" VALUES (%s, %s, %s)"


####################### SELECTS

# shows the avg salary by branch
sel_avg_sal_branch = f"SELECT \
                            branch_name AS 'Branch', \
                            count(*) AS '# Employees', \
                            AVG(salary) AS 'AVG Salary' \
                        FROM employees \
                        JOIN branches ON branches.id = employees.branch_id \
                        GROUP BY branch_id \
                        ORDER BY AVG(salary) DESC; "

# shows the avg salary by department
sel_avg_sal_dep = f" SELECT \
                            department AS 'Department', \
                            count(*) AS '# Employees', \
                            AVG(salary) AS 'AVG Salary' \
                        FROM employees \
                        GROUP BY department \
                        ORDER BY AVG(salary) DESC; "

# shows the 50 workers that get the most in the company
sel_top_sals = f" SELECT \
                        employees.id, \
                        CONCAT(first_name, ' ', last_name) as Name, \
                        age, \
                        salary, \
                        department, \
                        branch_name \
                    FROM employees \
                    JOIN branches ON branches.id = employees.branch_id \
                    ORDER BY salary DESC LIMIT 50; "


# ranks salaries by branch and department
sel_rank_sals = f" SELECT \
                        employees.id, \
                        CONCAT(first_name, ' ', last_name) as Name, \
                        salary, \
                        DENSE_RANK() OVER(ORDER BY salary DESC) as overall_rank, \
                        RANK() OVER(PARTITION BY department ORDER BY SALARY DESC) as dept_salary_rank, \
                        RANK() OVER(PARTITION BY branch_id ORDER BY SALARY DESC) as branch_salary_rank, \
                        department, \
                        branch_name \
                    FROM employees \
                    JOIN branches ON branches.id = employees.branch_id \
                    ORDER BY overall_rank;"

# what branch is with the oldest employees (over 60)
sel_branch_oldest_emps = f" SELECT \
                                branch_name, \
                                COUNT(*) AS count \
                            FROM employees \
                            JOIN branches ON branches.id = employees.branch_id \
                            WHERE age > 60 \
                            GROUP BY branch_name \
                            ORDER BY count DESC LIMIT 3; "

# all the employees in HUSTON with a salary between 100k and 200k
sel_hu_sal_range = f" SELECT \
                            id, \
                            email, \
                            department, \
                            salary, \
                            NTILE(4) OVER(ORDER BY salary ) AS salary_quartile \
                        FROM employees \
                        WHERE salary BETWEEN 100000 AND 200000 \
                        AND branch_id = (SELECT id FROM branches WHERE branch_name = 'HOUSTON') \
                        ORDER BY department, salary_quartile; "

# shows the salary diffs by department
sel_diff_dept_employees = f"SELECT \
                                id, \
                                department, \
                                RANK() OVER(PARTITION BY department ORDER BY SALARY DESC) as dept_salary_rank, \
                                salary, \
                                salary - LAG(salary) OVER(PARTITION BY department ORDER BY salary DESC) as dept_diff \
                            FROM employees \
                            ORDER BY salary DESC; "

select_commands = [sel_avg_sal_branch, sel_avg_sal_dep,
                   sel_top_sals, sel_branch_oldest_emps,
                   sel_hu_sal_range, sel_diff_dept_employees]
