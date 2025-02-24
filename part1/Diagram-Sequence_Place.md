```mermaid
sequenceDiagram
    participant PlaceCreation
    participant API
    participant BusinessLogic
    participant Database

    PlaceCreation->>API: Place created
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic-->>PlaceCreation: 404 ERROR
    BusinessLogic->>Database: Save Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Response
    API-->>PlaceCreation: Return Success
