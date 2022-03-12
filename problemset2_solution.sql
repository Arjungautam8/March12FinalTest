SELECT
    dr.name AS Department, e1.name AS Employee, e1.salary
FROM
    Employee e1
        JOIN
    Department dr ON e1.departmentId = dr.id
WHERE
    3 > (SELECT
            COUNT(DISTINCT e2.salary)
        FROM
            Employee e2
        WHERE
            e2.salary > e1.salary
                AND e1.departmentId = e2.departmentId
        ) order by department, salary desc