CREATE TABLE ticket(
   id SERIAL PRIMARY KEY,
	ticketid CHARACTER(4),
	personid INTEGER,
	levelid INTEGER,
	gradeid INTEGER,
	categoryid CHARACTER(1),
	stateid CHARACTER(1) DEFAULT 'P',
	write_uid INTEGER,
	write_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE person(
	personid INTEGER  PRIMARY KEY,
	name VARCHAR(200)
);
CREATE TABLE level(
	levelid INTEGER  PRIMARY KEY,
	description VARCHAR(200)
);
CREATE TABLE grade(
	gradeid INTEGER  PRIMARY KEY,
	description VARCHAR(200)
);
CREATE TABLE category(
	categoryid CHARACTER(1)  PRIMARY KEY,
	description VARCHAR(200)
);
CREATE TABLE state(
	stateid CHARACTER(1)  PRIMARY KEY,
	description VARCHAR(200)
);