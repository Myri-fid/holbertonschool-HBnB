from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repository = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner_id=place_data['owner_id'],
                amenities=place_data['amenities']
            )
            self.place_repository.save(place)
            return place
        except Exception as e:
            raise ValueError(f"Error creation place: {e}")
         

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repository.get_all()

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        place = self.place_repository.get_by_id(place_id)
        if not place:
            raise ValueError(f"Place avec ID {place_id} pas trouvé")

    def get_place_by_id(self, place_id):
        place = self.place_repository.get_by_id(place_id)
        if not place:
            raise ValueError(f"Place avec ID {place_id} pas trouvé")
        return place
