import os
import json
import hashlib

# Main filepaths used around helper functions
script_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(script_directory)
watched_folder = os.path.join(parent_directory, "watched")
data_folder = os.path.join(parent_directory, "data")
users_filepath = os.path.join(data_folder, "user_ids.json")


def get_users():
    try:
        with open(users_filepath, "r") as users_file:
            content = users_file.read()
            user_data = json.loads(content)
            return user_data

    except FileNotFoundError:
        print(
            "No users currently created. Creating corresponding data folders with no users..."
        )
        # Ensure the directory structure exists
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        with open(users_filepath, "w") as latest_file:
            json.dump([], latest_file, indent=2, sort_keys=True)
            print("Latest version generated and saved.")


def store_user(user_id):
    users_filepath = os.path.join(data_folder, "user_ids.json")
    try:
        with open(users_filepath, "r+") as users_file:
            content = users_file.read()
            user_data = json.loads(content)
            if user_id not in user_data:
                user_data.append(user_id)

            users_file.seek(0)
            users_file.truncate()
            users_file.flush()
            json.dump(user_data, users_file, indent=2, sort_keys=True)

    except FileNotFoundError:
        print(
            "No users currently created. Creating corresponding data folders with current user..."
        )
        # Ensure the directory structure exists
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        with open(users_filepath, "w") as users_file:
            json.dump([user_id], users_file, indent=2, sort_keys=True)
            print("Latest version generated and saved.")


def remove_user(user_id):
    users_filepath = os.path.join(data_folder, "user_ids.json")
    try:
        with open(users_filepath, "r+") as users_file:
            content = users_file.read()
            user_data = json.loads(content)
            for current_user in user_data:
                if user_id == current_user:
                    user_data.remove(current_user)
                    break
            users_file.seek(0)
            users_file.truncate()
            users_file.flush()
            json.dump(user_data, users_file, indent=2, sort_keys=True)

    except FileNotFoundError:
        print("No users currently exist. Cannot delete from an empty list.")
        pass


def checksum_diff(site, payload):
    """
    Compares the md5 checksum of the current payload with the latest stored payload for a given site.

    Parameters:
        site (str): Name of the site for comparison.
        payload (dict or list): Data to be compared.

    Raises:
        FileNotFoundError: If latest file for the site is not found.

    Returns:
        True: if md5 checksum differs from the latest stored payload
        False: if md5 checksum is the same as the latest stored payload
    """
    latest_filepath = os.path.join(watched_folder, f"{site}_latest.json")
    current_filepath = os.path.join(watched_folder, f"{site}_current.json")

    try:
        with open(latest_filepath, "r") as latest_file:
            with open(current_filepath, "w") as current_file:
                # Populate current file to compare checksums
                json.dump(payload, current_file, indent=2, sort_keys=True)
                current_file.close()
                
    except FileNotFoundError:
        print("Currently not watched. Generating latest version...")
        # Ensure the directory structure exists
        if not os.path.exists(watched_folder):
            os.makedirs(watched_folder)
        with open(latest_filepath, "w") as latest_file:
            json.dump(payload, latest_file, indent=2, sort_keys=True)
            print("Latest version generated and saved.")

    # Perform the actual comparison
    current_checksum = calculate_checksum(current_filepath)
    latest_checksum = calculate_checksum(latest_filepath)
    print(f"Checksum (SHA-256) of current file: {current_checksum}")
    print(f"Checksum (SHA-256) of latest file: {latest_checksum}")

    if current_checksum != latest_checksum:
        print("Checksum difference found:")
        print(
            f"Latest checksum: {latest_checksum}\nCurrent checksum: {current_checksum}"
        )
        print("Replacing latest file")
        with open(latest_filepath, "w") as latest_file:
            json.dump(payload, latest_file, indent=2, sort_keys=True)
            latest_file.close()
        return True
    else:
        return False


def calculate_checksum(filepath):
    """Calculate checksum of a file."""
    try:
        with open(filepath, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()
    except FileNotFoundError:
        print(f"File '{filepath}' not found.")
        return None
