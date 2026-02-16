SELECT DISTINCT grade_level
FROM students;

SELECT COUNT(DISTINCT students.grade_level)
FROM students;

SELECT MAX(students.gpa) - MIN(students.gpa) as gpa_range
FROM students;

SELECT *
FROM students
WHERE grade_level < 12 AND school_lunch = 'Yes';

SELECT *
FROM students
WHERE grade_level IN(10,11,12) AND school_lunch ='No'
ORDER BY student_name DESC;

SELECT *
FROM students
WHERE email LIKE '%.com';

SELECT students.student_name, students.gpa
FROM students
ORDER BY gpa DESC
LIMIT 10;

SELECT students.student_name, students.grade_level,
       CASE WHEN students.grade_level = 9 THEN 'Freshman'
            WHEN students.grade_level = 10 THEN  'Shophomore'
            ELSE 'Senior' END AS student_class
FROM students;

