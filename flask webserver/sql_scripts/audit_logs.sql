CREATE TABLE "Audit_Logs" (
    "Logid" INTEGER NOT NULL UNIQUE,
    "Userid" INTEGER NOT NULL,
    "Action" TEXT NOT NULL,
    "Details" TEXT,
    "Timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("Logid" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE SET NULL
);
