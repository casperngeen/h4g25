CREATE TABLE "User" (
	"UserId"	INTEGER,
	"Name"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL,
    "Isadmin"   INTEGER NOT NULL,
	PRIMARY KEY("UserId")
);