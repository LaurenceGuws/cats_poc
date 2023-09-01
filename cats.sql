-- Create table for Locations
CREATE TABLE Locations (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    -- add detail lines for address
    Address TEXT
);

-- Create table for HealthStatus
CREATE TABLE HealthStatus (
    HealthStatusID INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT,
    IsVaccinated BOOLEAN,
    IsFixed BOOLEAN,
    OtherMedicalProcedures TEXT
);

-- Create table for AdoptionStatus
CREATE TABLE AdoptionStatus (
    AdoptionStatusID INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT
);

-- Create table for Users
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash TEXT NOT NULL,
    Role VARCHAR(50),
    LocationID INT,
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

-- Create table for Cats
CREATE TABLE Cats (
    CatID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    Breed VARCHAR(255),
    HealthStatusID INT,
    LocationID INT,
    AdoptionStatusID INT,
    FOREIGN KEY (HealthStatusID) REFERENCES HealthStatus(HealthStatusID),
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
    FOREIGN KEY (AdoptionStatusID) REFERENCES AdoptionStatus(AdoptionStatusID)
);

-- Create table for CatImages
CREATE TABLE CatImages (
    ImageID INT AUTO_INCREMENT PRIMARY KEY,
    CatID INT,
    ImagePath TEXT,
    FOREIGN KEY (CatID) REFERENCES Cats(CatID)
);
