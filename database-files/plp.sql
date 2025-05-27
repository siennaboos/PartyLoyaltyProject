DROP DATABASE IF EXISTS plp;
CREATE DATABASE IF NOT EXISTS plp;

USE plp;


CREATE TABLE IF NOT EXISTS political_party (
    partyID INT PRIMARY KEY,
    partyCohesionScore INT,
    partyName VARCHAR(255),
    leaderID INT,
    FOREIGN KEY (leaderID) REFERENCES mep(mepID)
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

CREATE TABLE IF NOT EXISTS referenceDocument(
    legislationID INT,
    referenceID INT,
    PRIMARY KEY (legislationID, referenceID),
    FOREIGN KEY (legislationID) REFERENCES legislation(legislationID),
);

CREATE TABLE IF NOT EXISTS vote (
    mepID INT,
    legislationID INT,
    description VARCHAR(255),
    PRIMARY KEY (mepID, legislationID),
    FOREIGN KEY (mepID) REFERENCES mep(mepID),
    FOREIGN KEY (legislationID) REFERENCES legislation(legislationID)
);

CREATE TABLE IF NOT EXISTS watchList (
    watchListID INT PRIMARY KEY,
);

CREATE TABLE IF NOT EXISTS user (
    userID INT PRIMARY KEY,
    age INT,
    countryOfOrigin VARCHAR(255),
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    partyID INT,
    watchListID INT,
    FOREIGN KEY (partyID) REFERENCES political_party(partyID),
    FOREIGN KEY (watchListID) REFERENCES watchList(watchListID)
);


CREATE TABLE IF NOT EXISTS mepToWatchList (
    watchListID INT,
    mepID INT,
    PRIMARY KEY (watchListID, mepID),
    FOREIGN KEY (watchListID) REFERENCES watchList(watchListID),
    FOREIGN KEY (mepID) REFERENCES mep(mepID)
);


