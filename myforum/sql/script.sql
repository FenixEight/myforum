CREATE SEQUENCE seq_users MINVALUE 1;
CREATE SEQUENCE seq_comments MINVALUE 1;

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
user_id int references users(id)
);


