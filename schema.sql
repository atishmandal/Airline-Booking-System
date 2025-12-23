-- Database: airline
CREATE DATABASE IF NOT EXISTS airline;
USE airline;

-- ----------------------------
-- Table: details
-- ----------------------------
CREATE TABLE details (
    Flightno DECIMAL(4,0) NOT NULL,
    Airline VARCHAR(20),
    Departure VARCHAR(20),
    Arrival VARCHAR(20),
    DateDepart DATE,
    DateArrival DATE,
    TimeDep VARCHAR(10),
    TimeArrive VARCHAR(10),
    Duration VARCHAR(10),
    BaseCost DECIMAL(6,0),
    PRIMARY KEY (Flightno)
);

-- ----------------------------
-- Table: passenger
-- ----------------------------
CREATE TABLE passenger (
    FlightNo DECIMAL(4,0),
    PassengerID DECIMAL(4,0),
    PassengerName VARCHAR(30),
    Dob DATE,
    Seattype VARCHAR(20),
    bookdate DATE,
    Foodtype VARCHAR(15),
    LuggageWeight DECIMAL(4,0)
);

-- ----------------------------
-- Table: cancellation
-- ----------------------------
CREATE TABLE cancellation (
    FlightNo DECIMAL(4,0) NOT NULL,
    PassengerID DECIMAL(4,0),
    BaseCost DECIMAL(6,0),
    Foodcost DECIMAL(6,0),
    LuggageCost DECIMAL(6,0),
    Seatcost DECIMAL(6,0),
    AvailabilityCost DECIMAL(5,0)
);
