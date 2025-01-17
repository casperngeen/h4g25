CREATE TABLE "Otps" (
    "Otpid" INTEGER NOT NULL UNIQUE,
    "Userid" INTEGER NOT NULL,
    "Otp" TEXT NOT NULL,
    PRIMARY KEY("Otpid" AUTOINCREMENT),
    CONSTRAINT "User"
        FOREIGN KEY ("Userid") 
        REFERENCES "User" ("Userid")
        ON DELETE CASCADE
);
