CREATE SEQUENCE seq_users MINVALUE 1;
CREATE SEQUENCE seq_posts MINVALUE 1;
CREATE SEQUENCE seq_tags MINVALUE 1;
CREATE SEQUENCE seq_post_tag MINVALUE 1;
CREATE SEQUENCE seq_ban MINVALUE 1;
CREATE SEQUENCE seq_comments MINVALUE 1;

CREATE TABLE "users"(
id int not null default nextval('"seq_users"'::text) primary key,
username varchar(128),
password varchar,
admin_mod int,
has_photo boolean
);

CREATE TABLE "posts"(
post_id int not null default nextval('"seq_posts"'::text) primary key,
post varchar,
date_time varchar,
user_agent varchar,
ip varchar,
user_id int references users(id),
status varchar
);


create table tags(
tag_id int not null default
nextval('"seq_tags"'::text) primary key,
tag varchar);


create table post_tag(
id int not null default nextval('"seq_post_tag"'::text) primary key,
post_id int references posts(post_id),
tag_id int references tags(tag_id));

CREATE TABLE params(
param varchar, status varchar);
insert into params(param, status) values('moderation', 'off');

create table ban(
id int not null default nextval('"seq_ban"'::text) primary key,
username int,
username_banned int);

CREATE TABLE comments(
id int not null default nextval('"seq_comments"'::text) primary key,
post_id int,
parent_id int,
date_time TIMESTAMP,
comment varchar,
is_deleted boolean,
user_id int references users(id)
);