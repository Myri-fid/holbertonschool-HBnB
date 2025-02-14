```mermaid
classDiagram
direction TB
    class User {
	    +int ID
	    +String firstName
	    +String lastName
	    +String email
	    -String _password
	    +bool is_admin
	    +List roles
	    +createReview()
	    +updateUser()
	    +deleteUser()
    }

    class Amenity {
	    +int ID
	    +String name
	    +String description
	    +Date creationDate
	    +String amenityType
	    +updateAmenity()
	    +deleteAmenity()
    }

    class Review {
	    +int ID
	    +Place place
	    +User user
	    +int rating
	    +String comment
	    +Date creationDate
	    +createReview()
	    +updateReview()
	    +deleteReview()
    }

    class Place {
	    +int ID
	    +String title
	    +String description
	    +float price
	    +float latitude
	    +float longitude
	    +Date creationDate
	    +addAmenityToPlace()
	    +updatePlace()
	    +deletePlace()
    }

    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : has
    Amenity "1..*" -- "0..*" Place : Add Amenity
    User "1" -- "0..*" Place : owns
    ```