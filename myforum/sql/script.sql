CREATE SEQUENCE seq_comment MINVALUE 1;

CREATE TABLE "comments"(
	comment_id int not null default nextval('"seq_comment"'::text) primary key,
	user_name varchar(128),
	comment_text text,
	creation_date timestamp not null);