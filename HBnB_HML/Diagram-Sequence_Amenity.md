```mermaid
sequenceDiagram
    participant Amenity
    participant API
    participant BusinessLogic
    participant Database

    Amenity->>API: Amenity created
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic-->>Amenity: 404 ERROR
    BusinessLogic->>Database: Save Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Response
    API-->>Amenity: Return Success
