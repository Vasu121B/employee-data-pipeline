# Findings

Results of the questions in analysis.sql, run against data/employees.db. The data is synthetic (see README.md).

## Q1: How many employees does each department have?

| department | employees |
| --- | --- |
| Sales | 946 |
| Finance | 761 |
| Human Resources | 728 |
| Customer Support | 702 |
| Engineering | 698 |
| Marketing | 477 |

## Q2: What is the average and median salary in each department?

| department | employees | avg_salary | median_salary |
| --- | --- | --- | --- |
| Customer Support | 702 | 76,654.23 | 76,061.77 |
| Engineering | 698 | 78,092.00 | 77,118.12 |
| Finance | 761 | 76,900.72 | 75,692.42 |
| Human Resources | 728 | 78,634.96 | 79,420.31 |
| Marketing | 477 | 75,877.02 | 74,887.24 |
| Sales | 946 | 77,760.49 | 78,705.56 |

## Q3: How do salaries compare across employee statuses?

| status | employees | avg_salary |
| --- | --- | --- |
| Terminated | 634 | 77,962.23 |
| Unknown | 205 | 77,476.52 |
| Inactive | 946 | 77,378.65 |
| Active | 1611 | 77,330.26 |
| On Leave | 916 | 77,238.99 |

## Q4: How many people were hired in each year?

| hire_year | hires |
| --- | --- |
| 2015 | 386 |
| 2016 | 405 |
| 2017 | 370 |
| 2018 | 416 |
| 2019 | 381 |
| 2020 | 404 |
| 2021 | 397 |
| 2022 | 373 |
| 2023 | 412 |
| 2024 | 375 |
| 2025 | 393 |

## Q5: Who are the 5 highest-paid employees in each department?

| department | name | salary |
| --- | --- | --- |
| Customer Support | Grace Walker | 119,991.46 |
| Customer Support | Nora Adams | 119,759.60 |
| Customer Support | Liam Davis | 119,645.12 |
| Customer Support | Noah Harris | 119,631.47 |
| Customer Support | Mason Anderson | 119,490.06 |
| Engineering | Liam Smith | 119,661.17 |
| Engineering | Olivia Harris | 119,592.63 |
| Engineering | Leo Jackson | 119,548.99 |
| Engineering | Sophia Adams | 119,508.79 |
| Engineering | Harper Harris | 119,431.38 |
| Finance | Evelyn Lewis | 119,866.85 |
| Finance | Nora Taylor | 119,720.24 |
| Finance | Ben Smith | 119,640.31 |
| Finance | Liam White | 119,396.74 |
| Finance | Lucas White | 119,378.82 |
| Human Resources | Sam Garcia | 119,963.62 |
| Human Resources | Mia Davis | 119,884.40 |
| Human Resources | Charlotte Hall | 119,790.86 |
| Human Resources | Luke Thomas | 119,657.40 |
| Human Resources | Jack Adams | 119,454.77 |
| Marketing | Olivia Hall | 119,509.23 |
| Marketing | Jack Baker | 119,467.86 |
| Marketing | Emma Johnson | 119,185.11 |
| Marketing | Jack Adams | 118,982.10 |
| Marketing | Emma Nguyen | 118,816.08 |
| Sales | Lucas Harris | 119,741.54 |
| Sales | Grace Young | 119,735.98 |
| Sales | Sophia Jackson | 119,499.29 |
| Sales | James Thomas | 119,485.22 |
| Sales | Lucas Taylor | 119,461.34 |

## Q6: Which departments have the most rows with Unknown status?

| department | unknown_status_rows |
| --- | --- |
| Sales | 44 |
| Human Resources | 39 |
| Finance | 39 |
| Customer Support | 33 |
| Engineering | 29 |
| Marketing | 21 |
