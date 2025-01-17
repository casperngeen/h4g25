CREATE TABLE "Voucher_Tasks" (
    "Taskid" INTEGER NOT NULL UNIQUE,
    "Userid" INTEGER NOT NULL,
    "Description" TEXT NOT NULL,
    "Amount" REAL NOT NULL,
    "Status" TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'rejected')),
    "Created" DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("Taskid" AUTOINCREMENT),
    CONSTRAINT "User"
        FOREIGN KEY ("Userid") 
        REFERENCES "User" ("Userid")
        ON DELETE CASCADE
);
