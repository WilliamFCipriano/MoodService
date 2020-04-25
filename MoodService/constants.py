database_location = 'moodService.db'

create_user_table = ["""
create table users
(
  int_id        integer not null
    constraint users_pk
      primary key autoincrement,
  user_name       string  not null,
  password_hash integer not null
);
""","""
create unique index users_int_id_uindex
  on users (int_id);
""","""
create unique index users_user_name_uindex
  on users (user_name);
"""]

create_session_table = ["""
create table sessions
(
	session_id integer not null
		constraint sessions_pk
			primary key autoincrement,
	user_int_id integer not null,
	token string not null
);""","""
create unique index sessions_session_id_uindex
	on sessions (session_id);"""]