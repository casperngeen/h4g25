CREATE TABLE "Vouchers" (
	"Voucherid"	INTEGER NOT NULL UNIQUE,
	"Userid"	INTEGER NOT NULL,
	"Amount"	REAL NOT NULL,
	PRIMARY KEY("Voucherid" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE
);
