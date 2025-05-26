DROP DATABASE IF EXISTS plp;
CREATE DATABASE IF NOT EXISTS plp;
USE plp;

CREATE TABLE IF NOT EXISTS political_party (
    partyID INT PRIMARY KEY,
    partyCohesionScore INT,
    partyName VARCHAR(255),
);


CREATE TABLE IF NOT EXISTS mep (
    mepID INT PRIMARY KEY,
    name VARCHAR(255),
    countryOfOrigin VARCHAR(255),
    partyID INT,
    recommendedParty INT,
    FOREIGN KEY (partyID) REFERENCES political_party(partyID),
    FOREIGN KEY (recommendedParty) REFERENCES political_party(partyID)
);

CREATE TABLE IF NOT EXISTS legislation (
    legislationID INT PRIMARY KEY,
    title VARCHAR(255),
    dateOfVote DATE,
);


CREATE TABLE IF NOT EXISTS vote (
    mepID INT,
    legislationID INT,
    vote VARCHAR(255),
    PRIMARY KEY (mepID, legislationID),
    FOREIGN KEY (mepID) REFERENCES mep(mepID),
    FOREIGN KEY (legislationID) REFERENCES legislation(legislationID)
);