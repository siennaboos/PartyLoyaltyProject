USE loyalty_lines;

-- PREPARE POLIICAL PARTIES
INSERT INTO political_party (partyName)
VALUES ("European People's Party");

INSERT INTO political_party (partyName)
VALUES ("Progressive Alliance of Socialists and Democrats");

INSERT INTO political_party (partyName)
VALUES ("Patriots for Europe");

INSERT INTO political_party (partyName)
VALUES ("European Conservatives and Reformists");

INSERT INTO political_party (partyName)
VALUES ("Renew Europe");

INSERT INTO political_party (partyName)
VALUES ("Greens/European Free Alliance");

INSERT INTO political_party (partyName)
VALUES ("The Left in the European Parliament - GUE/NGL");

INSERT INTO political_party (partyName)
VALUES ("Europe of Sovereign Nations");

INSERT INTO political_party (partyName)
VALUES ("Non-attached Members");

INSERT INTO political_party(partyName)
VALUES ("Identity and Democracy");

-- PREPARE USER ROLES
INSERT INTO userRole(userRoleID, userRoleName)
VALUES (1, "PartyLeader");

INSERT INTO userRole(userRoleID, userRoleName)
VALUES (2, "PoliticalJournalist");

INSERT INTO userRole(userRoleID, userRoleName)
VALUES (3, "Citizen");

-- PREARE USER PERSONAS
INSERT INTO user (age, countryOfOrigin, firstName, lastName, partyID, userRoleID)
VALUES ("59", "Greece", "Yanni", "Polous", 1, 3);

INSERT INTO user (age, countryOfOrigin, firstName, lastName, userRoleID)
VALUES ("30", "Spain", "Camila", "Romero", 2);

INSERT INTO user (age, countryOfOrigin, firstName, lastName, partyID, userRoleID)
VALUES ("23", "Switzerland", "Greg", "Gerborg", 3, 1);


