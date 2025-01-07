#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Immigrant Helper Tool


# In[5]:


DEBUG_MODE = False # Set to True for debugging output

from datetime import datetime
from typing import List
import json

# ------------------ Helper Functions for File I/O ------------------

def save_data(filename: str, data: dict, verbose: bool = False) -> None:
    """
    Save data to a JSON file with indentation for readability.

    Args:
        filename (str): Name of the file to save data to.
        data (dict): The dictionary to be saved.
        verbose (bool): Whether to print a success message. Default is False.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        if verbose:
            print(f"Data saved to {filename}: {data}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")


def load_data(filename: str) -> dict:
    """
    Load data from a JSON file. If the file doesn't exist, return an empty dictionary.

    Args:
        filename (str): Name of the file to load data from.

    Returns:
        dict: The loaded data or an empty dictionary if the file is not found.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            if DEBUG_MODE:
                print(f"Loaded data from {filename}: {data}")  # Debugging output
            return data
    except FileNotFoundError:
        if DEBUG_MODE:
            print(f"{filename} not found. Starting fresh.")
        return {}
    except json.JSONDecodeError as e:
        if DEBUG_MODE:
            print(f"Error decoding JSON from {filename}: {e}")
        return {}

def is_valid_email(email: str) -> bool:
    """
    Validate an email address format using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    import re
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None



# ------------------ Helper Functions for Object Creation ------------------

def create_immigrant_from_dict(data: dict):
    """
    Create an Immigrant object from a dictionary.

    Args:
        data (dict): Dictionary containing immigrant details.

    Returns:
        Immigrant or None: A new Immigrant object or None if creation fails.
    """
    try:
        immigrant = Immigrant(
            name=data["name"],
            email=data["email"],
            native_language=data["native_language"],
            desired_language=data["desired_language"],
            location=data["location"],
            goals=data["goals"]
        )
        immigrant.progress_log = data.get("progress_log", [])
        if DEBUG_MODE:
            print(f"Created immigrant: {immigrant}")  # Debugging output
        return immigrant
    except KeyError as e:
        if DEBUG_MODE:
            print(f"Missing key {e} in immigrant data: {data}")
        return None
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error creating immigrant from data {data}: {e}")
        return None

def create_volunteer_from_dict(data: dict):
    """
    Create a Volunteer object from a dictionary.

    Args:
        data (dict): Dictionary containing mentor details.

    Returns:
        Volunteer or None: A Volunteer object or None if creation fails.
    """
    try:
        expertise = data["expertise"].lower()
        volunteer_mapping = {
            "language": LanguageMentor,
            "cultural integration": CulturalIntegrationMentor,
            "career": CareerMentor,
            "health": HealthAdvisor,
            "legal": LegalAdvisor
        }

        if expertise in volunteer_mapping:
            volunteer = volunteer_mapping[expertise](
                name=data["name"],
                email=data["email"],
                available_languages=data["available_languages"],
                availability=data.get("availability", True)
            )
            if DEBUG_MODE:
                print(f"Created volunteer: {volunteer}")  # Debugging output
            return volunteer
        else:
            if DEBUG_MODE:
                print(f"Invalid expertise '{expertise}' in mentor data: {data}")
            return None
    except KeyError as e:
        if DEBUG_MODE:
            print(f"Missing key {e} in mentor data: {data}")
        return None
    except Exception as e:
        if DEBUG_MODE:
            print(f"Error creating volunteer from data {data}: {e}")
        return None
    

# ------------------  Classes ------------------   

# ------------------ Immigrant Class ------------------

class Immigrant:
    """
    Designed to store personal data and track progress 
    Represents an immigrant seeking help with resources and mentoring.
    """
    def __init__(self, name: str, email: str, native_language: str, desired_language: str, location: str, goals: list):
        self.name = name
        self.email = email
        self.native_language = native_language
        self.desired_language = desired_language
        self.location = location
        self.goals = goals
        self.progress_log = []  # Tracks mentoring sessions and progress.-as a list of dictionaries
        
        
    def __str__(self):
        """
        Return a human-readable string representation of the immigrant.
        """
        goals_str = ", ".join(self.goals)
        return (f"Name: {self.name}, Email: {self.email}, Native Language: {self.native_language}, "
                f"Desired Language: {self.desired_language}, Location: {self.location}, "
                f"Goals: {goals_str}")

                                

    def update_progress(self, session_type: str, details: str) -> None:
        """
        Add a progress log entry.

        Args:
            session_type (str): Type of session (e.g., Language Practice).
            details (str): Details about the session.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.progress_log.append({
            "session_type": session_type,
            "details": details,
            "timestamp": timestamp
        })
        print(f"Progress updated: {session_type} - {details} at {timestamp}")

    def view_progress(self) -> None:
        """
        Display all progress logs for the immigrant.
        """
        if not self.progress_log:
            print("No progress logged yet.")
        else:
            print("\n=== Progress Log ===")
            for log in self.progress_log:
                print(f"- {log['session_type']} ({log['timestamp']}): {log['details']}")
                
            
                
    def update_goals(self, new_goals: list) -> None:
        """
        Update the immigrant's goals.

        Args:
            new_goals (list): The updated list of goals.
        """
        self.goals = new_goals
        print(f"Goals updated to: {', '.join(self.goals)}")
        

        # ------------------ Volunteer Classes ------------------
'''
The Volunteer class and its subclasses represent different types of volunteers
who can provide guidance and support to immigrants in various areas such as 
language, cultural integration, career advice, health, and legal matters.

Volunteers are not necessarily direct service providers in their fields.
For example:
- A Health Advisor might not be a doctor but could guide immigrants on navigating
  the healthcare system, understanding rules, finding opportunities, and accessing 
  resources, whether paid or free.
- Similarly, a Career Mentor might suggest strategies for job hunting, offer networking tips,
  or point toward relevant skill-building opportunities.

These roles focus on helping immigrants understand systems, access resources, 
and build connections to achieve their goals effectively.
'''


# ------------------ Volunteer Classes ------------------

class Volunteer:
    """
    Base class for all volunteers, holding shared attributes and methods.
    """
    def __init__(self, name: str, email: str, expertise: str, available_languages: List[str], availability=True):
        self.name = name
        self.email = email
        self.expertise = expertise
        self.available_languages = [lang.strip().lower() for lang in available_languages]
        self.availability = availability
        
        
    def set_availability(self, status: bool) -> None:
        """
        Update the volunteer's availability status.

        Args:
            status (bool): True for available, False for unavailable.
        """
        self.availability = status
        state = "Available" if status else "Unavailable"
        print(f"{self.name}'s availability updated to {state}.")       
        
    

    def __str__(self):
        """
        Return a human-readable string representation of the volunteer.
        """
        status = "Available" if self.availability else "Unavailable"
        languages = ", ".join(self.available_languages)
        return f"Name: {self.name}, Expertise: {self.expertise}, Availability: {status}, Languages: {languages}"

#Specialized subclasses to represent different types of volunteers:

class LanguageMentor(Volunteer):
    def __init__(self, name, email, available_languages, availability=True):
        super().__init__(name, email, "Language", available_languages, availability)

    def __str__(self):
        return f"[Language Mentor] {super().__str__()}"


class CulturalIntegrationMentor(Volunteer):
    def __init__(self, name, email, available_languages, availability=True):
        super().__init__(name, email, "Cultural Integration", available_languages, availability)

    def __str__(self):
        return f"[Cultural Integration Mentor] {super().__str__()}"


class CareerMentor(Volunteer):
    def __init__(self, name, email, available_languages, availability=True):
        super().__init__(name, email, "Career", available_languages, availability)

    def __str__(self):
        return f"[Career Mentor] {super().__str__()}"


class HealthAdvisor(Volunteer):
    def __init__(self, name, email, available_languages, availability=True):
        super().__init__(name, email, "Health", available_languages, availability)

    def __str__(self):
        return f"[Health Advisor] {super().__str__()}"


class LegalAdvisor(Volunteer):
    def __init__(self, name, email, available_languages, availability=True):
        super().__init__(name, email, "Legal", available_languages, availability)

    def __str__(self):
        return f"[Legal Advisor] {super().__str__()}"
    
    
# ------------------ MentorManager Class ------------------


'''
The MentorManager class is responsible for managing a list of mentors and facilitating
their interaction with immigrants. It acts as a bridge to match immigrants with the 
mentor based on expertise, language, and availability.

'''


# ------------------ MentorManager Class ------------------
class MentorManager:
    """
    Manages the list of mentors and matches them with immigrants.
    """

    def __init__(self):
        """
        Initialize the MentorManager with an empty list of mentors.
        """
        self.mentors = []  # List to store all mentors.

    def add_mentor(self, mentor: Volunteer,verbose: bool = False):
        """
        Add a mentor to the system.

        Args:
            mentor (Volunteer): The mentor to add.

        Raises:
            TypeError: If the mentor is not an instance of Volunteer or its subclasses.
        """
        try:
            # Check if the provided mentor is a valid Volunteer object or subclass.
            if not isinstance(mentor, Volunteer):
                raise TypeError("Only objects of type Volunteer or its subclasses can be added as mentors.")

            # Add the mentor to the list.
            self.mentors.append(mentor)

            # Print only if verbose is True
            if verbose:
                print(f"Mentor added: {mentor}")

        except TypeError as e:
            # Handle cases where the provided object is not a valid mentor.
            print(f"Error adding mentor: {e}")

        except Exception as e:
            # Catch any other unexpected errors during the addition process.
            print(f"An unexpected error occurred while adding a mentor: {e}")
            

    def find_mentor(self, immigrant: Immigrant, expertise: str):
        """
        Find an available mentor for the immigrant based on expertise and language.

        Args:
            immigrant (Immigrant): The immigrant requesting a mentor.
            expertise (str): Desired expertise (e.g., "Language", "Career").

        Returns:
            Volunteer: A matched mentor or None if no match is found.
        """
        try:
            # Ensure the immigrant is an Immigrant object.
            if not isinstance(immigrant, Immigrant):
                raise TypeError("The immigrant parameter must be an instance of the Immigrant class.")

            # Ensure the expertise is a string.
            if not isinstance(expertise, str):
                raise TypeError("The expertise parameter must be a string.")

            # Iterate through the list of mentors to find a match.
            for mentor in self.mentors:
                # Match based on expertise and availability.
                if mentor.expertise.lower() == expertise.lower() and mentor.availability:
                    # Check if the mentor speaks the immigrant's desired language.
                    if immigrant.desired_language.lower() in map(str.lower, mentor.available_languages):
                        # Mentor matched
                        mentor.availability = False
                        save_data("mentors.json", {mentor.email: mentor.__dict__ for mentor in self.mentors})
                        immigrant.update_progress("Mentor Matched", f"Matched with {mentor.name}")
                        return mentor

            # If no match is found, inform the user.
            print("No mentor available.")
            return None

        except AttributeError as e:
            # Handle cases where required attributes are missing.
            print(f"Error: A mentor or immigrant is missing a required attribute. Details: {e}")

        except TypeError as e:
            # Handle type-related issues.
            print(f"Type Error: {e}")

        except Exception as e:
            # Catch any other unexpected errors during the matching process.
            print(f"An unexpected error occurred during mentor matching: {e}")

        # Return None if no mentor is found or an error occurs.
        return None
    

    def remove_mentor(self, mentor_email: str):
        """
        Remove a mentor from the system by email.

        Args:
            mentor_email (str): The email of the mentor to remove.

        Returns:
            bool: True if the mentor was successfully removed, False otherwise.
        """
        try:
            # Iterate through the mentors to find a match by email.
            for mentor in self.mentors:
                if mentor.email.lower() == mentor_email.lower():  # Case-insensitive match.
                    # Remove the mentor from the list.
                    self.mentors.remove(mentor)

                    # Print confirmation of successful removal.
                    print(f"Mentor removed: {mentor}")
                    return True

            # If no mentor with the given email is found, inform the user.
            print(f"No mentor found with email: {mentor_email}")
            return False

        except ValueError as e:
            # Handle cases where the removal process fails unexpectedly.
            print(f"Error: Failed to remove mentor. Details: {e}")

        except Exception as e:
            # Catch any other unexpected errors during the removal process.
            print(f"An unexpected error occurred while removing a mentor: {e}")
            return False

    def list_mentors(self):
        """
        List all mentors currently in the system.
        """
        try:
            # Check if there are any mentors in the system.
            if not self.mentors:
                print("No mentors in the system.")
                return

            # Print each mentor's details.
            print("\n=== Mentors ===")
            for mentor in self.mentors:
                print(mentor)

        except Exception as e:
            # Catch any unexpected errors during the listing process.
            print(f"An unexpected error occurred while listing mentors: {e}")
            

# ------------------ Resource Class ------------------
class Resource:
    """
    Manages resources available for immigrants, organized by location and category.
    """

    def __init__(self):
        self.resource_db = {}  # Dictionary to store resources.

    def add_resource(self, location, category, name, verbose=False):
        """
        Add a new resource to the database.

        Args:
            location (str): The location (city or region) of the resource.
            category (str): The type of resource (e.g., Health, Legal, Education).
            name (str): The name of the resource to add.
            verbose (bool): Whether to print a success message. Default is False.
        """
        # Debugging: Show the input values
        #print(f"DEBUG: Adding resource with location='{location}', category='{category}', name='{name}'")

        # Validation with detailed error messages
        if not location.replace(" ", "").isalpha():
            print(f"Invalid location: '{location}'. Ensure it contains only letters and spaces.")
            return
        if not category.replace(" ", "").isalpha():
            print(f"Invalid category: '{category}'. Ensure it contains only letters and spaces.")
            return
        if not len(name.strip()) > 0:
            print(f"Invalid name: '{name}'. Ensure it is not empty.")
            return

        # Normalize inputs
        location = location.strip().lower()
        category = category.strip().lower()
        name = name.strip()

        # Add the resource
        if location not in self.resource_db:
            self.resource_db[location] = {}
        if category not in self.resource_db[location]:
            self.resource_db[location][category] = []
        self.resource_db[location][category].append(name)

        # Print success message if verbose is enabled
        if verbose:
            print(f"Resource '{name}' successfully added to {category.capitalize()} in {location.capitalize()}.")

    def save_resources(self, filename):
        """
        Save the resource database to a JSON file.

        Args:
            filename (str): Name of the file to save the resources.
        """
        try:
            with open(filename, 'w') as file:
                json.dump(self.resource_db, file, indent=4)
            print(f"Resources saved to {filename}.")
        except Exception as e:
            print(f"Error saving resources: {e}")

    def load_resources(self, filename):
        """
        Load the resource database from a JSON file.

        Args:
            filename (str): Name of the file to load the resources from.
        """
        try:
            with open(filename, 'r') as file:
                self.resource_db = json.load(file)
            print(f"Resources loaded from {filename}.")
        except FileNotFoundError:
            print(f"{filename} not found. Starting with an empty resource database.")
            self.resource_db = {}
        except Exception as e:
            print(f"Error loading resources: {e}")

    def _selection_sort(self, data):
        """
        Sort a list using the Selection Sort algorithm.

        Args:
            data (list): The list to sort.

        Returns:
            list: The sorted list.
        """
        for i in range(len(data)):
            min_index = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_index]:
                    min_index = j
            data[i], data[min_index] = data[min_index], data[i]
        return data

    def _binary_search(self, sorted_list, target, left, right):
        """
        Perform a binary search on a sorted list recursively.

        Args:
            sorted_list (list): The list to search.
            target (str): The item to search for.
            left (int): The starting index of the search range.
            right (int): The ending index of the search range.

        Returns:
            int: The index of the target if found, -1 otherwise.
        """
        if left <= right:
            mid = (left + right) // 2
            if sorted_list[mid] == target:
                return mid
            elif sorted_list[mid] < target:
                return self._binary_search(sorted_list, target, mid + 1, right)
            else:
                return self._binary_search(sorted_list, target, left, mid - 1)
        return -1

    def search_resources_by_location(self, location):
        """
        Display all resources available in a specific location.

        Args:
            location (str): The location to search for resources.
        """
        location = location.strip().lower()

        # Sort locations
        sorted_locations = self._selection_sort(list(self.resource_db.keys()))

        # Search for location
        index = self._binary_search(sorted_locations, location, 0, len(sorted_locations) - 1)
        if index != -1:
            actual_location = sorted_locations[index]
            print(f"\nResources in '{actual_location.capitalize()}':")
            for category, resources in self.resource_db[actual_location].items():
                print(f"- {category.capitalize()}: {', '.join(resources)}")
        else:
            print(f"No resources found for location '{location}'.")

    def search_resources_by_category(self, location, category):
        """
        Display resources in a specific location and category.

        Args:
            location (str): The location to search.
            category (str): The category to search within the location.
        """
        location = location.strip().lower()
        category = category.strip().lower()

        # Sort locations
        sorted_locations = self._selection_sort(list(self.resource_db.keys()))

        # Search for location
        location_index = self._binary_search(sorted_locations, location, 0, len(sorted_locations) - 1)
        if location_index != -1:
            actual_location = sorted_locations[location_index]
            # Sort categories
            sorted_categories = self._selection_sort(list(self.resource_db[actual_location].keys()))

            # Search for category
            category_index = self._binary_search(sorted_categories, category, 0, len(sorted_categories) - 1)
            if category_index != -1:
                actual_category = sorted_categories[category_index]
                print(f"\nResources in '{actual_location.capitalize()}' under '{actual_category.capitalize()}':")
                print(", ".join(self.resource_db[actual_location][actual_category]))
            else:
                print(f"No resources found in '{location}' under category '{category}'.")
        else:
            print(f"No resources found for location '{location}'.")
            
            
# ------------------ ROLE- SPECIFIC MENUS ------------------


def display_goal_menu() -> None:
    """
    Display the list of possible goals for immigrants.
    """
    print("\n🌟 Welcome to the Goal Setting Menu! 🌟")
    print("Here, you can define the areas where you'd like to focus and receive support.")
    print("Simply choose from the options below by entering the corresponding number:(1-6)")
    print("---------------------------------------------------")
    print("1. Language Practice")
    print("2. Career Guidance")
    print("3. Health Support")
    print("4. Community Engagement")
    print("5. Cultural Adaptation")
    print("6. Other (Enter your custom goal)")
    print("---------------------------------------------------")
    print("💡 Tip: You can select multiple goals, but please add one goal at a time.")
    print("🙏 A big thank you to all our dedicated volunteers who make this support possible!")



# ------------------ Immigrant Helper Functions ------------------

def update_goals_interactively(immigrant: Immigrant) -> None:
    """
    Allow the immigrant to update their goals interactively.

    Args:
        immigrant (Immigrant): The immigrant object whose goals are being updated.
    """
    print(f"\nYour current goals are: {', '.join(immigrant.goals)}")
    print("Let's update your goals! You can select from the predefined list or enter a custom goal.")
    updated_goals = []

    while True:
        display_goal_menu()
        goal_choice = input("Enter the number corresponding to your goal (or type 'done' to finish): ").strip().lower()
        if goal_choice == "done":
            if updated_goals:
                confirm = input(f"Your new goals will be: {', '.join(updated_goals)}. Confirm? (y/n): ").strip().lower()
                if confirm == "y":
                    immigrant.update_goals(updated_goals)
                    print("Your goals have been updated successfully!")
                else:
                    print("No changes made to your goals.")
                break
            else:
                print("You must select at least one goal before finishing.")
        elif goal_choice in ['1', '2', '3', '4', '5']:
            goal = ["Language Practice", "Career Guidance", "Health Support",
                    "Community Engagement", "Cultural Adaptation"][int(goal_choice) - 1]
            if goal not in updated_goals:
                updated_goals.append(goal)
                print(f"Added: {goal}")
            else:
                print(f"{goal} is already in your list.")
        elif goal_choice == '6':
            custom_goal = input("Enter your custom goal: ").strip()
            if all(part.isalpha() for part in custom_goal.split()):  # Ensure custom goal is meaningful
                if custom_goal not in updated_goals:
                    updated_goals.append(custom_goal)
                    print(f"Added custom goal: {custom_goal}")
                else:
                    print(f"Custom goal '{custom_goal}' is already in your list.")
            else:
                print("Invalid custom goal. Please enter only letters.")
        else:
            print("Invalid choice. Please enter a number between 1 and 6 or 'done'.")
            
##########
def immigrant_menu(immigrant: Immigrant, mentor_manager: MentorManager, resource_manager: Resource) -> None:
    """
    Display the main menu for immigrants and handle user actions.

    Args:
        immigrant (Immigrant): The immigrant interacting with the system.
        mentor_manager (MentorManager): Manages mentors for matching.
        resource_manager (Resource): Manages available resources.
    """
    print(f"\nWelcome, {immigrant.name}!")
    print(f"Your current goals are: {', '.join(immigrant.goals)}")

    expertise_mapping = {
        "1": "language",
        "2": "cultural integration",
        "3": "career",
        "4": "health",
        "5": "legal"
    }

    while True:
        print("\n=== Immigrant Menu ===")
        print("Please select an option by entering the corresponding number:(1-5)")
        print("1. Ask for a Mentor")
        print("2. Check Resources")
        print("3. View Progress")
        print("4. Update Goals")
        print("5. Exit to Main Menu")

        try:
            choice = int(input("Enter your choice (1-5): ").strip())
            if choice == 1:
                # Ask for a mentor
                print("\nMentor Matching")
                print("We can connect you with mentors in the following expertise areas:")
                print("1. Language\n2. Cultural Integration\n3. Career\n4. Health\n5. Legal")

                while True:
                    expertise_choice = input("Enter the expertise you need help with (1-5): ").strip()
                    expertise = expertise_mapping.get(expertise_choice)
                    if expertise:
                        mentor = mentor_manager.find_mentor(immigrant, expertise)
                        if mentor:
                            print(f"\n🎉 Congratulations! You have been matched with {mentor.name}.")
                            print(f"📧 Contact Email: {mentor.email}")
                        else:
                            print("⚠️ Sorry, no available mentors match your request at this time.")
                        break
                    else:
                        print("❌ Invalid input. Please enter a number between 1 and 5.")

            elif choice == 2:
                # Check resources
                resource_menu(resource_manager)
            elif choice == 3:
                # View progress
                immigrant.view_progress()
            elif choice == 4:
                # Update goals
                update_goals_interactively(immigrant)
            elif choice == 5:
                print(f"Goodbye, {immigrant.name}! Returning to the Main Menu.")
                return
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            


# Supported languages
LANGUAGES = [
    "english", "spanish", "turkish", "korean", "chinese", "vietnamese", "farsi",
    "french", "german", "japanese", "arabic", "hindi", "russian", "portuguese"
]

# Expertise areas
EXPERTISE_AREAS = ["language", "cultural integration", "career", "health", "legal"]



def validate_email_input(prompt: str) -> str:
    """
    Prompt the user for an email and validate its format.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The valid email address.
    """
    while True:
        email = input(prompt).strip()
        if is_valid_email(email):
            return email
        print("Invalid email format. Please try again.")
        
        
def volunteer_menu(mentor_manager: MentorManager, immigrants_db: dict) -> None:
    """
    Display the volunteer menu and handle volunteer-related actions.

    Args:
        mentor_manager (MentorManager): The mentor manager instance.
        immigrants_db (dict): The dictionary of immigrants for mentee-related functionality.
    """
    while True:
        print("\n=== Volunteer Menu ===")
        print("Please select an option by entering the corresponding number:")
        print("1. Log in as an Existing Volunteer")
        print("2. Register as a New Volunteer")
        print("3. Update Your Availability")
        print("4. View Your Information")
        print("5. View Your Mentees")
        print("6. Back to Main Menu")
        print("---------------------------------------------------")
        print("💡 Tip: Use option 2 if you're a first-time volunteer!")

        # Validate menu choice
        while True:
            try:
                choice = int(input("Enter your choice (1-6): ").strip())
                if 1 <= choice <= 6:
                    break
                print("Invalid choice. Please enter a number between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == 1:
            # Log in as an existing volunteer
            email = validate_email_input("Enter your email to log in: ")
            mentor_found = False
            for mentor in mentor_manager.mentors:
                if mentor.email.lower() == email:
                    mentor_found = True
                    print(f"\n🎉 Welcome back, {mentor.name}!")
                    print("Here are your details:")
                    print(mentor)
                    break
            if not mentor_found:
                print("🚫 No volunteer found with that email. Please check the email or register as a new volunteer.")

        elif choice == 2:
            # Register as a new volunteer
            email = validate_email_input("Enter your email to register: ")

            # Check if the email already exists
            for mentor in mentor_manager.mentors:
                if mentor.email.lower() == email:
                    print("⚠️ A volunteer with this email already exists. Please log in instead.")
                    break
            else:
                # Proceed with registration
                while True:
                    name = input("Enter your full name: ").strip()
                    if all(part.isalpha() for part in name.split()) and len(name) > 1:
                        break
                    print("❌ Invalid name. Please enter a valid name with only letters and spaces.")

                while True:
                    expertise = input("Enter your area of expertise (choose one: Language, Career, etc.): ").strip().lower()
                    if expertise.lower() in [e.lower() for e in EXPERTISE_AREAS]:
                        expertise = expertise.lower() 
                        break
                    print(f"⚠️ Invalid expertise. Please choose from: {', '.join(EXPERTISE_AREAS)}.")

                while True:
                    print(f"Supported languages: {', '.join([lang.capitalize() for lang in LANGUAGES])}")
                    languages = input("Enter the languages you speak (comma-separated): ").strip().lower()
                    if languages:
                        language_list = [lang.strip().lower() for lang in languages.split(',') if lang.strip()]
                        invalid_languages = [lang for lang in language_list if lang not in LANGUAGES]
                        if not invalid_languages:
                            break
                        print(f"❌ Invalid language(s): {', '.join(invalid_languages)}. Please choose from the supported languages.")
                    else:
                        print("❌ Invalid input. Please enter at least one language.")

                while True:
                    availability = input("Are you currently available? (y/n): ").strip().lower()
                    if availability in ['y', 'n']:
                        availability = availability == 'y'
                        break
                    print("❌ Invalid input. Please enter 'y' or 'n'.")

                new_mentor = Volunteer(name, email, expertise, language_list, availability)
                mentor_manager.add_mentor(new_mentor)
                # Save the mentor data immediately
                save_data("mentors.json", {mentor.email: mentor.__dict__ for mentor in mentor_manager.mentors})
                print(f"🎉 Thank you, {name}! You have been successfully registered as a mentor.")

        elif choice == 3:
            # Update volunteer availability
            email = validate_email_input("Enter your email to update availability: ")
            mentor_found = False
            for mentor in mentor_manager.mentors:
                if mentor.email.lower() == email:
                    mentor_found = True
                    while True:
                        status = input("Are you currently available? (y/n): ").strip().lower()
                        if status in ['y', 'n']:
                            mentor.set_availability(status == 'y')
                            print(f"✅ Your availability has been updated to {'Available' if status == 'y' else 'Unavailable'}.")
                            break
                        print("❌ Invalid input. Please enter 'y' or 'n'.")
                    break
            if not mentor_found:
                print("🚫 No volunteer found with that email.")

        elif choice == 4:
            # View volunteer information
            email = validate_email_input("Enter your email to view your information: ")
            mentor_found = False
            for mentor in mentor_manager.mentors:
                if mentor.email.lower() == email:
                    mentor_found = True
                    print("\n📋 Here is your information:")
                    print(mentor)
                    break
            if not mentor_found:
                print("🚫 No volunteer found with that email.")

        elif choice == 5:
            # View mentees for a specific mentor
            email = validate_email_input("Enter your email to view your mentees: ")
            mentor_found = False
            for mentor in mentor_manager.mentors:
                if mentor.email.lower() == email:
                    mentor_found = True
                    print(f"\n👥 Mentees matched with {mentor.name}:")
                    mentees_found = False
                    for immigrant in immigrants_db.values():
                        for log in immigrant.progress_log:
                            if f"Matched with {mentor.name}" in log['details']:
                                print(f"- {immigrant.name} ({immigrant.email})")
                                mentees_found = True
                    if not mentees_found:
                        print("❌ No mentees matched with you yet.")
                    break
            if not mentor_found:
                print("🚫 No volunteer found with that email.")

        elif choice == 6:
            # Exit the volunteer menu
            print("🔙 Returning to the Main Menu.")
            break
        
#Resource Menu
def resource_menu(resource_manager: Resource) -> None:
    """
    Display the resource management menu and handle resource-related actions.

    Args:
        resource_manager (Resource): The resource manager instance.
    """
    while True:
        print("\n=== 📚 Resource Menu ===")
        print("Please select an option by entering the corresponding number:")
        print("1. View all resources in your city")
        print("2. Search resources by category")
        print("3. Add a new resource")
        print("4. Back to Immigrant Menu")
        print("---------------------------------------------------")

        # Validate menu choice
        while True:
            try:
                choice = int(input("Enter your choice (1-4): ").strip())
                if 1 <= choice <= 4:
                    break
                print("Invalid choice. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == 1:
            # View all resources by location
            location = input("Enter your location (e.g., 'San Francisco'): ").strip()
            if not location.replace(" ", "").isalpha():
                print("❌ Invalid location. Please enter a valid location name (e.g., 'San Francisco').")
                continue
            if location.lower() in resource_manager.resource_db:
                print(f"📍 Resources available in {location.capitalize()}:")
                resource_manager.search_resources_by_location(location)
            else:
                print(f"🚫 No resources found for location '{location}'.")
                print(f"🗺️ Supported locations: {', '.join([loc.capitalize() for loc in resource_manager.resource_db.keys()])}")

        elif choice == 2:
            # Search resources by category
            location = input("Enter your location (e.g., 'San Francisco'): ").strip()
            if not location.replace(" ", "").isalpha():
                print("❌ Invalid location. Please enter a valid location name (e.g., 'San Francisco').")
                continue
            if location.lower() in resource_manager.resource_db:
                category = input("Enter the category of resources you are looking for (e.g., Health, Legal, Education): ").strip().lower()
                if not category.replace(" ", "").isalpha():
                    print("❌ Invalid category. Please enter a valid category name (e.g., 'Health').")
                    continue
                if category in resource_manager.resource_db[location.lower()]:
                    print(f"🔎 Searching for {category.capitalize()} resources in {location.capitalize()}...")
                    resource_manager.search_resources_by_category(location, category)
                else:
                    print(f"🚫 No resources found in '{location}' under category '{category}'.")
                    print(f"📂 Supported categories in '{location.capitalize()}': {', '.join(resource_manager.resource_db[location.lower()].keys())}")
            else:
                print(f"🚫 No resources found for location '{location}'.")
                print(f"🗺️ Supported locations: {', '.join([loc.capitalize() for loc in resource_manager.resource_db.keys()])}")

        elif choice == 3:
            # Add a new resource
            location = input("Enter the location for the new resource (e.g., 'San Jose'): ").strip()
            if not location.replace(" ", "").isalpha():
                print("❌ Invalid location. Please enter a valid location name (e.g., 'San Jose').")
                continue

            category = input("Enter the resource category (e.g., 'Health', 'Education'): ").strip()
            if not category.replace(" ", "").isalpha():
                print("❌ Invalid category. Please enter a valid category name (e.g., 'Health').")
                continue

            name = input("Enter the name of the resource (e.g., 'San Jose Community Center'): ").strip()
            if not name:
                print("❌ Invalid resource name. Please enter a non-empty name.")
                continue

            resource_manager.add_resource(location, category, name, verbose=True)
            print(f"✅ Resource '{name}' added to {category.capitalize()} in {location.capitalize()} successfully!")

        elif choice == 4:
            # Return to Immigrant Menu
            print("🔙 Returning to Immigrant Menu...")
            break


# Prepopulate resources and volunteer list with default data to make the application functional and demo-ready.

#------------------ Prepopulate Resources ------------------
def prepopulate_resources(resource_manager: Resource, verbose: bool = False) -> None:
    """
    Prepopulate the resource manager with a wide variety of resources for demonstration.

    Args:
        resource_manager (Resource): The Resource object to populate with data.
        verbose (bool): Whether to print success messages. Default is False.
    """
    if verbose:
        print("Prepopulating resources...")

    # San Jose Resources
    resource_manager.add_resource(
        "san jose", "Health", "San Jose Community Health Center - https://www.sjcommunityhealth.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Education", "San Jose Adult Learning Center - https://www.sjadulted.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Legal", "San Jose Immigration Legal Aid - https://www.immigrationadvocates.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Nonprofit Organizations", "SIREN: Services, Immigrant Rights & Education Network - https://siren-bayarea.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Employment", "San Jose Career and Job Training Center - https://www.careercentersanjose.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Mental Health", "San Jose Family Counseling Center - https://www.sanjosecounseling.com", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Housing", "San Jose Housing Assistance - https://www.sanjosehousing.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san jose", "Transportation", "San Jose Public Transport Assistance - https://www.vta.org", verbose=verbose
    )

    # Cupertino Resources
    resource_manager.add_resource(
        "cupertino", "Cultural", "Cupertino Cultural Center - https://www.cupertinoculture.org", verbose=verbose
    )
    resource_manager.add_resource(
        "cupertino", "Education", "Cupertino Language Immersion Program - https://www.clipprogram.org", verbose=verbose
    )
    resource_manager.add_resource(
        "cupertino", "Nonprofit Organizations", "Cupertino Immigrant Support Network - https://www.cupertinoisn.org", verbose=verbose
    )
    resource_manager.add_resource(
        "cupertino", "Legal", "Cupertino Legal Aid Society - https://www.cupertinolegalaid.org", verbose=verbose
    )
    resource_manager.add_resource(
        "cupertino", "Health", "Cupertino Community Clinic - https://www.cupertinocommunityclinic.org", verbose=verbose
    )
    resource_manager.add_resource(
        "cupertino", "Childcare", "Cupertino Childcare Resources - https://www.cupertinochildcare.org", verbose=verbose
    )

    # San Francisco Resources
    resource_manager.add_resource(
        "san francisco", "Health", "San Francisco General Hospital - https://www.sfgh.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Education", "City College of San Francisco - https://www.ccsf.edu", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Legal", "San Francisco Legal Aid Society - https://www.legalaidatwork.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Nonprofit Organizations", "SF Immigrant Support Network - https://www.sfisn.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Employment", "San Francisco Workforce Development Center - https://www.workforcedevelopmentsf.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Mental Health", "San Francisco Behavioral Health Center - https://www.sfbhc.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Housing", "San Francisco Housing Support Services - https://www.sfhousing.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Cultural", "San Francisco Cultural Center - https://www.sfculturalcenter.org", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Transportation", "San Francisco Muni Assistance - https://www.sfmta.com", verbose=verbose
    )
    resource_manager.add_resource(
        "san francisco", "Childcare", "San Francisco Childcare Resources - https://www.sfchildcare.org", verbose=verbose
    )

    if verbose:
        print("Resource prepopulation completed.")
        
        
def prepopulate_volunteers(mentor_manager: MentorManager, verbose: bool = False) -> None:
    """
    Prepopulate the mentor manager with some default mentors for demonstration.

    Args:
        mentor_manager (MentorManager): The MentorManager object to populate with mentors.
        verbose (bool): Whether to print success messages. Default is False.
    """
    if verbose:
        print("Prepopulating volunteers with demo data...")

    # Dictionary format for demo data
    demo_volunteers = {
        # Language Mentors
        "alice.smith@example.com": {
            "name": "Alice Smith",
            "email": "alice.smith@example.com",
            "expertise": "language",
            "available_languages": ["english", "spanish"],
            "availability": True,
        },
        "juan.perez@example.com": {
            "name": "Juan Perez",
            "email": "juan.perez@example.com",
            "expertise": "language",
            "available_languages": ["spanish", "english"],
            "availability": True,
        },
        "mai.nguyen@example.com": {
            "name": "Mai Nguyen",
            "email": "mai.nguyen@example.com",
            "expertise": "language",
            "available_languages": ["vietnamese", "english"],
            "availability": True,
        },
        # Cultural Integration Mentors
        "ahmet@example.com": {
            "name": "Ahmet Yilmaz",
            "email": "ahmet@example.com",
            "expertise": "cultural integration",
            "available_languages": ["turkish", "english"],
            "availability": True,
        },
        "sofia.rossi@example.com": {
            "name": "Sofia Rossi",
            "email": "sofia.rossi@example.com",
            "expertise": "cultural integration",
            "available_languages": ["italian", "english"],
            "availability": True,
        },
        # Career Mentors
        "charlie.davis@example.com": {
            "name": "Charlie Davis",
            "email": "charlie.davis@example.com",
            "expertise": "career",
            "available_languages": ["english", "french"],
            "availability": True,
        },
        "priya.patel@example.com": {
            "name": "Priya Patel",
            "email": "priya.patel@example.com",
            "expertise": "career",
            "available_languages": ["hindi", "english"],
            "availability": True,
        },
        # Health Mentors
        "dana.lee@example.com": {
            "name": "Dana Lee",
            "email": "dana.lee@example.com",
            "expertise": "health",
            "available_languages": ["korean", "english"],
            "availability": True,
        },
        "alex.green@example.com": {
            "name": "Alex Green",
            "email": "alex.green@example.com",
            "expertise": "health",
            "available_languages": ["english", "german"],
            "availability": True,
        },
        # Legal Advisors
        "eve.martinez@example.com": {
            "name": "Eve Martinez",
            "email": "eve.martinez@example.com",
            "expertise": "legal",
            "available_languages": ["english", "portuguese"],
            "availability": True,
        },
        "yuki.tanaka@example.com": {
            "name": "Yuki Tanaka",
            "email": "yuki.tanaka@example.com",
            "expertise": "legal",
            "available_languages": ["japanese", "english"],
            "availability": True,
        },
    }

    # Iterate over the dictionary and add each mentor
    for email, volunteer_data in demo_volunteers.items():
        mentor = create_volunteer_from_dict(volunteer_data)
        if mentor:
            mentor_manager.add_mentor(mentor, verbose=verbose)
            if verbose:
                print(f"🎉 Volunteer '{mentor.name}' added successfully with expertise in {mentor.expertise.capitalize()}.")

                
                
                
# ------------------ Main Menu ------------------



def main_menu() -> None:
    # Initialize resources, mentor manager, and data
    resource_manager = Resource()
    prepopulate_resources(resource_manager, verbose=False)

    # Load immigrant data
    immigrants_db = {email: create_immigrant_from_dict(data) for email, data in load_data("immigrants.json").items()}

    # Create MentorManager instance
    mentor_manager = MentorManager()

    # Load mentor data
    mentors_data = load_data("mentors.json")
    if isinstance(mentors_data, dict) and mentors_data:  # Ensure it's a dictionary and non-empty
        print(f"Mentors loaded from JSON: {len(mentors_data)} mentors.")  # Debug statement
        for email, data in mentors_data.items():
            mentor = create_volunteer_from_dict(data)
            if mentor:
                mentor_manager.add_mentor(mentor, verbose=False)
        print("Using mentors from JSON file.")  # Debug statement
    else:
        print("No valid mentor data found. Prepopulating with demo mentors.")
        prepopulate_volunteers(mentor_manager, verbose=False)

    # Track changes to databases
    immigrants_modified = False
    mentors_modified = False

    while True:
        print("\n🌟 Welcome to the Immigrant Assistance Toolkit 🌟")
        print("Your trusted platform for connecting immigrants with resources and mentors.")
        print("\n=== Main Menu ===")
        print("1. Immigrant Seeking Help")
        print("2. Volunteer/Mentor Registration")
        print("3. Resource Management")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice (1-4): ").strip())
            if 1 <= choice <= 4:
                if choice == 1:
                    # Immigrant workflow
                    email = validate_email_input("Enter your email: ")

                    if email in immigrants_db:
                        current_immigrant = immigrants_db[email]
                    else:
                        # Register a new immigrant
                        while True:
                            name = input("Enter your name: ").strip()
                            if all(part.isalpha() for part in name.split()) and len(name) > 1:
                                break
                            print("Invalid name. Please enter a valid name with only letters and spaces.")

                        while True:
                            native_language = input("What is your native language? ").strip().lower()
                            if native_language in LANGUAGES:
                                break
                            print(f"Invalid language. Please choose from: {', '.join([lang.capitalize() for lang in LANGUAGES])}.")

                        while True:
                            desired_language = input("Which language would you like to practice? ").strip().lower()
                            if desired_language in LANGUAGES:
                                break
                            print(f"Invalid language. Please choose from: {', '.join([lang.capitalize() for lang in LANGUAGES])}.")

                        while True:
                            location = input("Enter your location: ").strip()
                            if location.replace(" ", "").isalpha():  # Allow spaces but ensure all other characters are alphabetic
                                break
                            print("Invalid location. Please enter a valid location (e.g., 'San Francisco').")

                        # Select goals
                        goals = []
                        while True:
                            display_goal_menu()
                            goal_choice = input("Enter a goal number (or type 'done' to finish): ").strip().lower()
                            if goal_choice == "done":
                                if goals:
                                    break
                                else:
                                    print("You must select at least one goal before finishing.")
                            elif goal_choice in ['1', '2', '3', '4', '5']:
                                goal = ["Language Practice", "Career Guidance", "Health Support",
                                        "Community Engagement", "Cultural Adaptation"][int(goal_choice) - 1]
                                if goal not in goals:
                                    goals.append(goal)
                                else:
                                    print("You have already added this goal.")
                            elif goal_choice == '6':
                                custom_goal = input("Enter your custom goal: ").strip()
                                if custom_goal.isalpha():  # Ensure custom goal is meaningful
                                    goals.append(custom_goal)
                                else:
                                    print("Invalid custom goal. Please enter only letters.")
                            else:
                                print("Invalid choice. Please enter a number between 1 and 6 or 'done'.")

                        current_immigrant = Immigrant(name, email, native_language, desired_language, location, goals)
                        immigrants_db[email] = current_immigrant
                        immigrants_modified = True  # Mark changes to immigrants

                    immigrant_menu(current_immigrant, mentor_manager, resource_manager)

                elif choice == 2:
                    # Volunteer workflow
                    if volunteer_menu(mentor_manager, immigrants_db):
                        mentors_modified = True  # Mark changes to mentors

                elif choice == 3:
                    # Resource management workflow
                    resource_menu(resource_manager)

                elif choice == 4:
                    # Exit the application
                    if immigrants_modified:
                        save_data("immigrants.json", {email: immigrant.__dict__ for email, immigrant in immigrants_db.items()})
                    if mentors_modified:
                        save_data("mentors.json", {mentor.email: mentor.__dict__ for mentor in mentor_manager.mentors})
                    print("Goodbye! Thank you for using the Immigrant Assistance Toolkit. Your participation helps create a stronger, more connected community where everyone can thrive. We deeply appreciate your efforts and contributions, whether you're seeking guidance or volunteering to support others. Together, we're making a meaningful difference. Have a wonderful day! 😊")
                    break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")





main_menu()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




