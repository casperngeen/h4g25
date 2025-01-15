CREATE TABLE "Products" (
    "Productid" INTEGER NOT NULL UNIQUE,
    "Name"      TEXT NOT NULL,
    "Stock"     INTEGER NOT NULL,
    "Price"     REAL NOT NULL,
    PRIMARY KEY("Productid" AUTOINCREMENT)
);
