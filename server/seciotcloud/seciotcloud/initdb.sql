create table iotdata(
	home_guid	text,
	client_or_server integer,
	msg_time 	text,
	state		text,
	UNIQUE(home_guid, client_or_server) ON CONFLICT REPLACE
);


create table valuetables(
	valname		text,
	valvalue	text, 
	valtime		text
);
CREATE UNIQUE INDEX I1 ON valuetables(valname);
