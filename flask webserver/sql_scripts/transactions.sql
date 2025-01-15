CREATE TABLE "Transactions" (
    "Transactionid" INTEGER NOT NULL UNIQUE,
	"Userid"	    INTEGER NOT NULL,
    "Description"   TEXT,
    "Amount"        REAL NOT NULL,
    "Created"       DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("Transactionid" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE
);
