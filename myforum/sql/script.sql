CREATE TABLE "comment"(
	comment_id int not null,
	user_name varchar(128),
	comment_text text,
	creation_date timestamp not null,
	is_deleted bool not null default false);