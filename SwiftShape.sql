CREATE DATABASE SwiftShip;
USE SwiftShip;


CREATE TABLE Partners (
    PartnerID INT PRIMARY KEY AUTO_INCREMENT,
    PartnerName VARCHAR(100),
    ContactEmail VARCHAR(100)
);

CREATE TABLE Shipments (
    ShipmentID INT PRIMARY KEY AUTO_INCREMENT,
    PartnerID INT,
    OriginCity VARCHAR(50),
    DestinationCity VARCHAR(50),
    OrderDate DATE,
    PromisedDate DATE,
    ActualDeliveryDate DATE,
    Status VARCHAR(20), -- Delivered / Returned / In Transit
    FOREIGN KEY (PartnerID) REFERENCES Partners(PartnerID)
);

CREATE TABLE DeliveryLogs (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    ShipmentID INT,
    StatusUpdate VARCHAR(100),
    UpdateTime DATETIME,
    FOREIGN KEY (ShipmentID) REFERENCES Shipments(ShipmentID)
);

INSERT INTO Partners (PartnerName, ContactEmail) VALUES
('FastTrack Logistics', 'fast@logi.com'),
('QuickMove Couriers', 'quick@courier.com'),
('Speedy Express', 'speedy@express.com');

INSERT INTO Shipments 
(PartnerID, OriginCity, DestinationCity, OrderDate, PromisedDate, ActualDeliveryDate, Status) 
VALUES 
(1, 'Chennai', 'Madurai', DATE_SUB(CURDATE(), INTERVAL 10 DAY), DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_SUB(CURDATE(), INTERVAL 4 DAY), 'Delivered'),

(2, 'Coimbatore', 'Trichy', DATE_SUB(CURDATE(), INTERVAL 8 DAY), DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Delivered'),

(1, 'Salem', 'Chennai', DATE_SUB(CURDATE(), INTERVAL 6 DAY), DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_SUB(CURDATE(), INTERVAL 1 DAY), 'Returned'),

(3, 'Madurai', 'Chennai', DATE_SUB(CURDATE(), INTERVAL 7 DAY), DATE_SUB(CURDATE(), INTERVAL 3 DAY), DATE_SUB(CURDATE(), INTERVAL 5 DAY), 'Delivered'),

(2, 'Chennai', 'Salem', DATE_SUB(CURDATE(), INTERVAL 5 DAY), DATE_SUB(CURDATE(), INTERVAL 2 DAY), DATE_SUB(CURDATE(), INTERVAL 2 DAY), 'Delivered');


SELECT *
FROM Shipments
WHERE ActualDeliveryDate > PromisedDate;

SELECT 
    P.PartnerName,
    COUNT(CASE WHEN S.Status = 'Delivered' THEN 1 END) AS SuccessfulDeliveries,
    COUNT(CASE WHEN S.Status = 'Returned' THEN 1 END) AS ReturnedDeliveries,
    COUNT(*) AS TotalShipments,
    ROUND(
        COUNT(CASE WHEN S.Status = 'Delivered' THEN 1 END) * 100.0 / COUNT(*), 2
    ) AS SuccessRate
FROM Shipments S
JOIN Partners P ON S.PartnerID = P.PartnerID
GROUP BY P.PartnerName
ORDER BY SuccessRate DESC;

SELECT DestinationCity, COUNT(*) AS TotalOrders
FROM Shipments
WHERE OrderDate >= CURDATE() - INTERVAL 30 DAY
GROUP BY DestinationCity
ORDER BY TotalOrders DESC
LIMIT 1;

SELECT 
    P.PartnerName,
    COUNT(*) AS TotalShipments,
    COUNT(CASE WHEN S.ActualDeliveryDate > S.PromisedDate THEN 1 END) AS DelayedShipments,
    ROUND(
        (COUNT(*) - COUNT(CASE WHEN S.ActualDeliveryDate > S.PromisedDate THEN 1 END)) * 100.0 / COUNT(*),
        2
    ) AS OnTimePercentage
FROM Shipments S
JOIN Partners P ON S.PartnerID = P.PartnerID
GROUP BY P.PartnerName
ORDER BY DelayedShipments ASC;