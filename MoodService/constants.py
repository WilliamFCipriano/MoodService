database_location = 'moodService.db'

create_user_table = ["""
create table users
(
  int_id        integer not null
    constraint users_pk
      primary key autoincrement,
  user_name       string  not null,
  password_hash integer not null,
  last_submission date,
  streak_days integer
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
	on sessions (session_id);""","""
	create unique index sessions_token_uindex
	on sessions (token);"""]

create_mood_tables = ["""
create table mood_values
(
	id integer not null
		constraint mood_values_pk
			primary key autoincrement,
	value string not null
);""","""
create unique index mood_values_id_uindex
	on mood_values (id);""","""
create unique index mood_values_value_uindex
	on mood_values (value);""","""
create table mood_report
(
	id integer not null
		constraint mood_report_pk
			primary key autoincrement,
	mood_value_id integer not null,
	user_id integer not null,
	date date not null
);
""","""
create unique index mood_report_id_uindex
	on mood_report (id);"""]