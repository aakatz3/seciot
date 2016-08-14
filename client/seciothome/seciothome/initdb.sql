create table iotdata(
	home_guid	text primary key,
	client_or_server integer,
	msg_time 	text,
	state		text
);

CREATE UNIQUE INDEX I1 ON iotdata(home_guid,client_or_server);


create table valuetables(
	valname		text,
	valvalue	text, 
	valtime		text,
	modified	integer
);
CREATE UNIQUE INDEX I1 ON valuetables(valname);
