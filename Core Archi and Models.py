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

class Appointment:
    def __init__(self, appointment_id, pet_id, date_time, service):
        self.appointment_id = appointment_id
        self.pet_id = pet_id
        self.date_time = date_time
        self.service = service
        self.status = "Scheduled"

    def cancel(self):
        self.status = "Cancelled"

    def complete(self):
        self.status = "Completed"

    def __str__(self):
        return (f"Appointment[{self.appointment_id}]: Pet ID {self.pet_id} on "
                f"{self.date_time} for '{self.service}' | Status: {self.status}")

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
            cls._instance = super(ClinicDatabase, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.owners = {}
        self.pets = {}
        self.appointments = {}

    def reset_database(self):
        """Utility method to reset singleton state for test isolation."""
        self._initialize()
      
    def register_owner(self, owner_id, name, contact_number):
        if owner_id in self.owners:
            raise ValueError(f"Owner ID {owner_id} already exists.")
        new_owner = PetOwner(owner_id, name, contact_number)
        self.owners[owner_id] = new_owner
        return new_owner

    def view_registered_owners(self):
        print("\n--- Registered Pet Owners ---")
        if not self.owners:
            print("No owners registered.")
        for owner in self.owners.values():
            print(owner)
        return list(self.owners.values())

    def add_pet_record(self, pet_type, pet_id, name, owner_id):
        if owner_id not in self.owners:
            raise ValueError(f"Cannot add pet. Owner ID {owner_id} does not exist.")
        if pet_id in self.pets:
            raise ValueError(f"Pet ID {pet_id} already exists.")

        new_pet = PetFactory.create_pet(pet_type, pet_id, name, owner_id)
        self.pets[pet_id] = new_pet
        return new_pet

    def view_pet_information(self):
        print("\n--- Registered Pets ---")
        if not self.pets:
            print("No pets registered.")
        for pet in self.pets.values():
            print(pet)
        return list(self.pets.values())

    def schedule_appointment(self, appointment_id, pet_id, date_time, service):
        if pet_id not in self.pets:
            raise ValueError(f"Cannot schedule appointment. Pet ID {pet_id} does not exist.")
        if appointment_id in self.appointments:
            raise ValueError(f"Appointment ID {appointment_id} already exists.")

        new_appointment = Appointment(appointment_id, pet_id, date_time, service)
        self.appointments[appointment_id] = new_appointment
        return new_appointment

    def view_appointments(self):
        print("\n--- Scheduled Appointments ---")
        if not self.appointments:
            print("No appointments found.")
        for appt in self.appointments.values():
            print(appt)
        return list(self.appointments.values())

    def cancel_appointment(self, appointment_id):
        if appointment_id not in self.appointments:
            raise ValueError(f"Appointment ID {appointment_id} does not exist.")
        self.appointments[appointment_id].cancel()
        return self.appointments[appointment_id]

    def update_appointment_status(self, appointment_id, status):
        if appointment_id not in self.appointments:
            raise ValueError(f"Appointment ID {appointment_id} does not exist.")
        if status.lower() == "completed":
            self.appointments[appointment_id].complete()
        elif status.lower() == "cancelled":
            self.appointments[appointment_id].cancel()
        else:
            self.appointments[appointment_id].status = status
        return self.appointments[appointment_id]
  
  


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
  
  db1.schedule_appointment("A-001", "P-001", "2026-10-01 09:00 AM", "Annual Checkup")
  db1.schedule_appointment("A-002", "P-002", "2026-10-01 10:30 AM", "Vaccination")
  db1.view_appointments()

  db1.cancel_appointment("A-001")
  db1.update_appointment_status("A-002", "Completed")
  db1.view_appointments()
  
