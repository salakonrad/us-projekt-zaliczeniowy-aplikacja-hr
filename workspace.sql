UPDATE hr.holidays_balance INNER JOIN hr.holidays_requests ONSET amount_left = amount_left - 1 WHERE id=2;

UPDATE T1, T2,
[INNER JOIN | LEFT JOIN] T1 ON T1.C1 = T2. C1
SET T1.C2 = T2.C2,
    T2.C3 = expr
WHERE condition

UPDATE hr.holidays_balance INNER JOIN hr.holidays_requests ON holidays_balance.id_users = holidays_requests.id_users SET holidays_balance.amount_left = amount_left - 1 WHERE



DELETE FROM hr.holidays_requests WHERE holidays_requests.id={absence_id};

UPDATE hr.holidays_requests INNER JOIN hr.holidays_balance ON holidays_balance.id_users = holidays_requests.id_users
SET holidays_balance.amount_left = amount_left - 1
WHERE holidays_balance.id_users = 2 AND holidays_balance.holiday_type='urlop-macierzynski';


UPDATE hr.holidays_requests SET holidays_balance.amount_left = amount_left - 1 WHERE holidays_balance.id_users = 2 AND holidays_balance.holiday_type='urlop-macierzynski';


SELECT hr.holidays_requests.id AS holiday_request_id, hr.users.id AS user_id ,hr.users.email, hr.holidays_requests.holiday_type, hr.holidays_requests.date_from, hr.holidays_requests.date_to
FROM `holidays_requests`
INNER JOIN hr.users
ON holidays_requests.id_users = users.id;


SELECT salaries.id,salaries.amount_net,salaries.amount_gross,salaries.date,users.email FROM hr.salaries INNER JOIN hr.users ON salaries.id_users = users.id WHERE id_users=2;
SELECT * FROM hr.salaries WHERE id_users=2;


INSERT INTO holidays_balance (id_users, holiday_type, amount_left)
SELECT users.id, 'urlop-wypoczynkowy', 10 FROM hr.users INNER JOIN holidays_balance ON  holidays_balance.id_users = users.id WHERE users.email='stefan@salins.pl';

SELECT users.id, 'urlop-wypoczynkowy', 10 FROM hr.users INNER JOIN holidays_balance ON  holidays_balance.id_users = users.id WHERE users.email='stefan@salins.pl';