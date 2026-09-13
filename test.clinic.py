"""
CPE106L-4 Laboratory 4 : Unit Testing
Vet Clinic Appointment Management System

Tests covered:
  1. Register Pet Owner
  2. Add Pet Record
  3. Schedule Appointment
  4. Cancel Appointment
  5. Validate Singleton Instance

Note: The module under test is named "Core Archi and Models.py" (with spaces),
so it can't be imported with a normal `import` statement. We load it
dynamically with importlib instead. Make sure this test file sits in the
same folder as "Core Archi and Models.py" in the repo.
"""

import unittest
import importlib.util
import os

# --- Dynamically import "Core Archi and Models.py" ---
MODULE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Core Archi and Models.py")
spec = importlib.util.spec_from_file_location("core_archi_and_models", MODULE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

ClinicDatabase = core.ClinicDatabase


class TestVetClinicSystem(unittest.TestCase):

    def setUp(self):
        # Singleton, so grab the existing instance and wipe its state
        # before every test to keep tests independent of each other.
        self.db = ClinicDatabase()
        self.db.reset_database()

    # ---------- 1. Register Pet Owner ----------
    def test_register_pet_owner(self):
        owner = self.db.register_owner("O-001", "Jane Doe", "555-1234")

        self.assertIn("O-001", self.db.owners)
        self.assertEqual(owner.name, "Jane Doe")
        self.assertEqual(owner.contact_number, "555-1234")

    def test_register_pet_owner_duplicate_id_raises_error(self):
        self.db.register_owner("O-001", "Jane Doe", "555-1234")

        with self.assertRaises(ValueError):
            self.db.register_owner("O-001", "Different Name", "555-9999")

    # ---------- 2. Add Pet Record ----------
    def test_add_pet_record(self):
        self.db.register_owner("O-001", "Jane Doe", "555-1234")
        pet = self.db.add_pet_record(pet_type="dog", pet_id="P-001", name="Max", owner_id="O-001")

        self.assertIn("P-001", self.db.pets)
        self.assertEqual(pet.species, "Dog")
        self.assertEqual(pet.owner_id, "O-001")

    def test_add_pet_record_nonexistent_owner_raises_error(self):
        with self.assertRaises(ValueError):
            self.db.add_pet_record(pet_type="cat", pet_id="P-002", name="Luna", owner_id="O-999")

    # ---------- 3. Schedule Appointment ----------
    def test_schedule_appointment(self):
        self.db.register_owner("O-001", "Jane Doe", "555-1234")
        self.db.add_pet_record(pet_type="cat", pet_id="P-001", name="Luna", owner_id="O-001")

        appt = self.db.schedule_appointment("A-001", "P-001", "2026-10-10 2:00 PM", "Vaccination")

        self.assertIn("A-001", self.db.appointments)
        self.assertEqual(appt.status, "Scheduled")
        self.assertEqual(appt.pet_id, "P-001")

    def test_schedule_appointment_nonexistent_pet_raises_error(self):
        with self.assertRaises(ValueError):
            self.db.schedule_appointment("A-002", "P-999", "2026-10-10 2:00 PM", "Checkup")

    # ---------- 4. Cancel Appointment ----------
    def test_cancel_appointment(self):
        self.db.register_owner("O-001", "Jane Doe", "555-1234")
        self.db.add_pet_record(pet_type="rabbit", pet_id="P-001", name="Bunny", owner_id="O-001")
        self.db.schedule_appointment("A-001", "P-001", "2026-10-10 3:00 PM", "Checkup")

        cancelled = self.db.cancel_appointment("A-001")

        self.assertEqual(cancelled.status, "Cancelled")
        self.assertEqual(self.db.appointments["A-001"].status, "Cancelled")

    def test_cancel_appointment_nonexistent_id_raises_error(self):
        with self.assertRaises(ValueError):
            self.db.cancel_appointment("A-999")

    # ---------- 5. Validate Singleton Instance ----------
    def test_validate_singleton_instance(self):
        db1 = ClinicDatabase()
        db2 = ClinicDatabase()

        self.assertIs(db1, db2)

    def test_singleton_shares_state_across_references(self):
        db1 = ClinicDatabase()
        db2 = ClinicDatabase()

        db1.register_owner("O-050", "Shared State Owner", "555-0000")

        # db2 should see the same data since it's the same underlying object
        self.assertIn("O-050", db2.owners)


if __name__ == "__main__":
    unittest.main(verbosity=2)
