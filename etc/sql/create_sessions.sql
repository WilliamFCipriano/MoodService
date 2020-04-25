create table sessions
(
	session_id integer not null
		constraint sessions_pk
			primary key autoincrement,
	user_int_id integer not null,
	token string not null
);

create unique index sessions_session_id_uindex
	on sessions (session_id);

create unique index sessions_token_uindex
	on sessions (token);