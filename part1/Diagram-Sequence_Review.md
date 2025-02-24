```mermaid
sequenceDiagram
    participant ReviewSubmission
    participant API
    participant BusinessLogic
    participant Database

    ReviewSubmission->>API: Review created
    API->>BusinessLogic: Validate and Process Request
    BusinessLogic-->>ReviewSubmission: 404 ERROR
    BusinessLogic->>Database: Save Data
    Database-->>BusinessLogic: Confirm Save
    BusinessLogic-->>API: Return Response
    API-->>ReviewSubmission: Return Success
