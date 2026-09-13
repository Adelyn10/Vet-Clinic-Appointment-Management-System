from abc import ABC

class PetOwner:
  def __init__(self, owner_id, name, contact_number):
    self.owner_id = owner_id
    self.name = name
    self.contact_number = contact_number

  def __str__(self):
    return f"Owner[{self.owner_id}]: {self.name} - {self.contact_number}"

class Pet(ABC):
  def __init__(self, pet_id, name, owner_id):
    self.pet_id = pet_id
    self.name = name
    self.owner_id = owner_id
    self.species = self.__class__.__name__

  def __str__(self):
    return f"Pet[{self.pet_id}]: {self.name} ({self.species}) - Belong to Owner ID: {self.owner_id}"

class Dog(Pet): pass
class Cat(Pet): pass
class Bird(Pet): pass
class Rabbit(Pet): pass

class PetFactory:
  @staticmethod
  def create_pet(pet_type, pet_id, name, owner_id):
    pet_type = pet_type.lower()
    if pet_type == 'dog':
      return Dog(pet_id, name, owner_id)
    elif pet_type == 'cat':
      return Cat(pet_id, name, owner_id)
    elif pet_type == 'bird':
      return Bird(pet_id, name, owner_id)
    elif pet_type == 'rabbit':
      return Rabbit(pet_id, name, owner_id)
    else:
      raise ValueError(f"Unsupported pet type: {pet_type}")

class ClinicDatabase:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(ClinicDatabase, cls.).__new__(cls)
      cls._instance._initialize()
    return cls._instance

  def _initialize(self):
    self.owners = {}
    self.pets = {}
    self.appointments = {}

  def register_owner(self, owner_id, name, contact_number):
    if owner_id in self.owners:
      raise ValueError(f"Owner ID {owner_id} already exists.")

    new_owner = PetOwner(owner_id, name, contact_number)
    self.owners[owner_id] = new_owner
    print(f"Success: Registered {new_owner}")
    return new_owner

  def view_registered_owners(self):
    print("\n-- Registered Pet Owners ---")
    if not self.owners:
      print("No owners registered.")
    for owner in self.owners:
      print(owner)
    return list(self.owners.values())

  def add_pet_record(self, pet_type, name, owner_id):
    if owner_id not in self.owners:
      print(f"Cannot add pet. Owner ID {owner_id} does not exist.")
    if pet_id in self.pets:
      raise ValueError(f"Pet ID {pet_id} already exists.")

    new_pet = PetFactory.create_pet(pet_type, pet_id, name, owner_id)
    self.pets[pet_id] = new_pet
    print(f"Success: Added {new_pet}")
    return new_pet

  def view_pet_information(self):
    print(f"\n-- Registered Pets ---")
    if not self.pets:
      print("No pets registered.")
    for pet in self.pets.values():
      print(pet)
    return list(self.pets.values())

if __name__ == "__main__":
  db1 = ClinicDatabase()
  db2 = ClinicDatabase()
  print(f"Are db1 and db2 the same instance? {db1 is db2}\n")

  db1.register_owner(owner_id="O-001", name="Alice Smith", contact_number="555-0100")
  db1.register_owner(owner_id="O-002", name="Bob Jones", contact_number="555-0200")
  db1.registered_owners()

  print("\n")
  db1.add_pet_record(pet_type="dog", pet_id="P-001", name="Buddy", owner_id="O-001")
  db1.add_pet_record(pet_type="cat", pet_id="P-002", name="Whiskers", owner_id="O-001")
  db1.add_pet_record(pet_type="rabbit", pet_id="P-003", name="Thumper", owner_id="O-002")
  db1.view_pet_information()
