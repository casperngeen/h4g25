CREATE TABLE "Preorders" (
    "Preorderid"     INTEGER NOT NULL UNIQUE,
    "Userid"        INTEGER NOT NULL,
    "Productid"     INTEGER NOT NULL,
    "Quantity"      INTEGER NOT NULL,
    "Amount"        REAL NOT NULL,
    "Vouchers"      TEXT NOT NULL,
    "Status"        TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'rejected')),
    "Created"       DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("Preorderid" AUTOINCREMENT),
    CONSTRAINT "user"
        FOREIGN KEY ("Userid") 
        REFERENCES "User"("Userid")
        ON DELETE CASCADE,
    CONSTRAINT "product"
        FOREIGN KEY ("Productid") 
        REFERENCES "Products" (id) 
        ON DELETE CASCADE
);
