CREATE TABLE "User" (
	"UserId"	INTEGER,
	"Name"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
    "Isadmin"   INTEGER NOT NULL,
	PRIMARY KEY("UserId")
);