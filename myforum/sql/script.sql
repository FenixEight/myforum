

CREATE TABLE "comments"(
	comment_id int not null default nextval('"seq_comment"'::text) primary key,
	user_name varchar(128),
	comment_text text,
	creation_date timestamp not null);

CREATE TABLE "users"(
id int not null default nextval('"seq_users"'::text) primary key,
username varchar(128),
password varchar,
admin_mod int
);

CREATE TABLE "posts"(
post_id int not null default nextval('"seq_comments"'::text) primary key,
post varchar,
date_time varchar,
user_agent varchar,
ip varchar,
user id references users(id)
);


###
-- Выполнение запроса:
CREATE SEQUENCE seq_users MINVALUE 1;
Query returned successfully with no result in 22 msec.

-- Выполнение запроса:
CREATE SEQUENCE seq_comments MINVALUE 1;
Query returned successfully with no result in 23 msec.
###