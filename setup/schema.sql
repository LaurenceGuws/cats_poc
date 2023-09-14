-- schema.sql

-- Drop tables if they exist
DROP TABLE IF EXISTS Cats;
DROP TABLE IF EXISTS Moms;
DROP TABLE IF EXISTS Deaths;
DROP TABLE IF EXISTS VetVisits;
DROP TABLE IF EXISTS VetChecks;
DROP TABLE IF EXISTS LocationMoves;
DROP TABLE IF EXISTS Docs;

-- Create Cats table
CREATE TABLE Cats (
    CatID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Pic TEXT,
    Sex TEXT,
    Colour TEXT,
    Condition TEXT,
    Weight REAL,
    Age INTEGER,
    FirstVax DATE,
    SecondVax DATE,
    SteriDue DATE,
    AdoptedDate DATE,
    AdoptedBy TEXT,
    AdopterContact TEXT,
    Message TEXT,
    ReceivedDate DATE
);

-- Create Moms table
CREATE TABLE Moms (
    MomID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT UNIQUE,
    Password TEXT,
    Location TEXT
);

-- Create Deaths table
CREATE TABLE Deaths (
    DeathID INTEGER PRIMARY KEY AUTOINCREMENT,
    CatID INTEGER,
    CauseOfDeath TEXT,
    VetName TEXT,
    Date DATE,
    Location TEXT,
    FOREIGN KEY (CatID) REFERENCES Cats(CatID)
);

-- Create VetVisits table
CREATE TABLE VetVisits (
    VisitID INTEGER PRIMARY KEY AUTOINCREMENT,
    CatID INTEGER,
    Diagnosis TEXT,
    MedsPrescribed TEXT,
    Date DATE,
    FOREIGN KEY (CatID) REFERENCES Cats(CatID)
);

-- Create VetChecks table
CREATE TABLE VetChecks (
    CheckID INTEGER PRIMARY KEY AUTOINCREMENT,
    CatID INTEGER,
    Deworm TEXT,
    Date DATE,
    FOREIGN KEY (CatID) REFERENCES Cats(CatID)
);

-- Create LocationMoves table
CREATE TABLE LocationMoves (
    MoveID INTEGER PRIMARY KEY AUTOINCREMENT,
    CatID INTEGER,
    FromLocation TEXT,
    ToLocation TEXT,
    Date DATE,
    FOREIGN KEY (CatID) REFERENCES Cats(CatID)
);

-- Create Docs table
CREATE TABLE Docs (
    DocID INTEGER PRIMARY KEY AUTOINCREMENT,
    Type TEXT,
    File BLOB
);
