import customtkinter
import pyautogui
import pytesseract
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image
from playsound import playsound
import time
import os

game_screenshot = Image.new('RGB', (25, 25), (255, 255, 255))
base_dir = os.path.dirname(__file__)


class Character:
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias
        self.desirability = 1
        self.role = "Unselected"
        self.coords = (0, 0, 0, 0)
        self.center_point = (0, 0)
        self.desirability_option = customtkinter.CTkOptionMenu

    def __str__(self):
        return f"Character: {self.name} | Alias: {self.alias:8} |" \
               f" Desirability: {self.desirability:2} | Role: {self.role:10} | Coords: {self.coords}"


ambassador = Character("Placeholder", "Placeholder")


def calculate_center(character):
    x, y, width, height = character.coords
    height_offset = 500
    character.center_point = (x + (width / 2), y + (height / 2) + height_offset)


# Examines pixel colors on screen to determine the spy portrait
def find_spy(character):
    screenshot_path = os.path.join(base_dir, 'images', 'cast_screenshot.png')
    screenshot = Image.open(screenshot_path)
    width, height = screenshot.size

    for y in range(height):
        for x in range(width):
            pixel_color = screenshot.getpixel((x, y))
            if pixel_color == (0, 191, 0):
                fileSavePath = os.path.join(base_dir, 'images', 'character_screenshots', f'{character.name}.png')
                crop = screenshot.crop((x - 5, y - 5, x + 150, y + 150))
                crop.save(fileSavePath)
                print("Found spy: " + character.name)
                character.coords = (x - 5, y - 5, x + 150, y + 150)
                return x, y
    print("findSpy failed.")
    return False


def get_game_data():
    data = game_screenshot.crop((50, 100, 425, 600))
    dataSavePath = os.path.join(base_dir, 'images', 'game_data.png')
    data.save(dataSavePath)
    gray_screenshot = data.convert('L') # Convert the screenshot to grayscale
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(gray_screenshot)

    """
    0: Venue-Name
    1: 
    2: Quickplay Mode:
    3: Quickplay-Mode-Name
    4:                          has the potential for 3 to spill over to 4 for realllly long names
    5: Missions: Any x of y
    6: Guests: #
    7: Time: x:xx
    """

    lines = text.split('\n')
    venue = lines[0]
    mode = lines[3]
    if lines[4] == '\n':
        guest_count = int(lines[6].split(':')[-1].strip())
        game_time = int(lines[7].split(':')[1].strip().split(':')[0]) * 60
    else:
        guest_count = int(lines[7].split(':')[-1].strip())
        game_time = int(lines[8].split(':')[1].strip().split(':')[0]) * 60
    game_properties = [venue, mode, guest_count, game_time]
    formatted_output = " Venue: {}\n Mode: {}\n Guests: {}\n Time: {}\n".format(venue, mode, guest_count, game_time)
    print(formatted_output)

    return game_properties


def swap(high, low):
    calculate_center(high)
    calculate_center(low)
    print("Swapping {}: {} with {}: {}, {}".format(high.alias, high.desirability, low.alias, low.desirability, low.role))
    print("Moving mouse to {} and clicking down".format(low.center_point))
    pyautogui.moveTo(low.center_point)
    pyautogui.mouseDown()
    print("Moving mouse to {} and releasing up".format(high.center_point))
    pyautogui.moveTo(high.center_point)
    pyautogui.mouseUp()
    temp_role = high.role
    high.role = low.role
    low.role = temp_role


def optimize_cast():
    if get_characters() != 21:
        print("Not all characters found. Will not optimize")
        return

    #venue, mode, guest_count, game_time = get_game_data()
    sorted_desirability_list = sorted(character_list, key=lambda person: int(person.desirability), reverse=True)

    for character in sorted_desirability_list:
        print(f"{character.alias:7}: {character.desirability}")

    pyautogui.moveTo(1000, 700)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    for character in reversed(sorted_desirability_list):
        if character.role == "Amba":
            print("Swapping {} with ambassador {}".format(character.name, ambassador.alias))
            swap(ambassador, character)
            break

    start_pointer = 0
    end_pointer = 20

    #beep_file = r'C:\Users\Max\PycharmProjects\SpyPartyCharacterPicker\adjusted_beep.wav'
    #playsound(beep_file)

    while start_pointer <= end_pointer:
        high = sorted_desirability_list[start_pointer]
        low = sorted_desirability_list[end_pointer]
        if high == ambassador:
            start_pointer += 1
        elif low == ambassador:
            end_pointer -= 1
        elif high.role == "Unselected" and low.role != "Unselected":
            swap(high, low)
            start_pointer += 1
            end_pointer -= 1
        elif low.role == "Unselected":
            print("{}: {} Unselected, Moving On".format(low.alias, low.desirability))
            end_pointer -= 1
        elif high.role != "Unselected":
            print("{}: {} Already Selected".format(high.alias, high.desirability))
            start_pointer += 1
        else:
            print("{}: {} | {}: {}".format(high.alias, high.desirability, low.alias, low.desirability))


# ======================================================================================================================
# Retrieves screenshot and determines the currently selected roles of the party
# ======================================================================================================================
def get_characters():
    print("Starting Search")
    character_path = os.path.join(base_dir, 'images', 'character_portraits')
    count = 0   # used to determine how many people have been matched
    extra_pixels = 5    # used for cropping top, bottom, left, right images of matched portraits
    screen_width, screen_height = pyautogui.size()  # used for creating screenshots of specific areas based off ratio
    height_restriction = screen_height // 2     # used to cut off bottom half of screen for portrait matching
    search_region = (0, height_restriction, screen_width, screen_height - 60)    # area searched for portraits
    global game_screenshot
    game_screenshot = pyautogui.screenshot()   # saved screenshot of characters/roles
    screenshotPath = os.path.join(base_dir, 'images', 'game_screenshot.png')
    game_screenshot.save(screenshotPath)
    cast_screenshot = game_screenshot
    cast_screenshot = cast_screenshot.crop(search_region)
    cast_screenshotPath = os.path.join(base_dir, 'images', 'cast_screenshot.png')
    cast_screenshot.save(cast_screenshotPath)
    unselected = []
    civilians = []
    unknown = []

    # Loop through each character and find a match on the cast_screenshot image
    for char_code in range(ord('A'), ord('U')+1):
        character = character_list[index(chr(char_code))]
        name = str(character.name)
        character_portrait = os.path.join(character_path, f'{name}.png')

        portrait_screenshot_path = os.path.join(base_dir, 'images', 'character_screenshots', f'{name}.png')
        print("Searching for: " + character_portrait)
        match = pyautogui.locate(character_portrait, cast_screenshot, grayscale=True, confidence=0.85)
        if match:
            print("Found " + name + ": " + str(match))
            left = max(0, match.left - extra_pixels)
            top = max(0, match.top)
            right = min(cast_screenshot.width, match.left + match.width + extra_pixels)
            bottom = min(cast_screenshot.height, match.top + match.height + extra_pixels + 5)
            match_photo = cast_screenshot.crop((left, top, right, bottom))
            match_photo.save(portrait_screenshot_path)
            character.coords = (left, top, right - left, bottom - top)
            role = get_role(character)
            character.role = role
            count += 1
            if role == "Civ":
                civilians.append(character)
            elif role == "Amba":
                do_nothing = 1
            elif role == "ST":
                seduction_target = character
            elif role == "DA":
                double_agent = character
            elif role == "Spy":
                spy = character
            else:
                unselected.append(character)

        else:
            print("----------------- Did not find " + name)
            random_cast_path = os.path.join(base_dir, 'images', 'RandomCast.png')
            portrait = Image.open(random_cast_path)
            portrait.save(portrait_screenshot_path)
            unknown.append(character)

    if len(unknown) == 1:
        character = unknown[0]
        character_coords = find_spy(character)
        x, y = character_coords
        if character_coords:
            character.role = "Spy"
            spy = character
            character.coords = x, y, 154, 154
            count += 1
    elif len(unknown) > 1:
        print("Greater than 1 unknown.")
        for character in unknown:
            print(character.name, end=" ")

    print("\n Found " + str(count) + "/21 Characters")
    print_character_list(character_list)

    return count


def get_role(character):
    character_screenshots_path = os.path.join(base_dir, 'images', 'character_screenshots', f'{character.name}.png')
    portrait_image = Image.open(character_screenshots_path)
    x, y, width, height = character.coords
    character.center_point = (x + (width / 2), y + (height / 2))

    for y in range(height // 3):
        for x in range(width // 3):
            pixel_color = portrait_image.getpixel((x, y))
            Civ = (162, 162, 162)
            Amba = (191, 0, 191)
            ST = (191, 0, 0)
            Spy = (0, 191, 0)
            DA = (191, 191, 0)

            if pixel_color == Civ:
                return "Civilian"
            elif pixel_color == Amba:
                return "Amba"
            elif pixel_color == ST:
                return "ST"
            elif pixel_color == DA:
                return "DA"
            elif pixel_color == Spy:
                return "Spy"

    return "Unselected"


def read_preset(number):
    preset_file_path = os.path.join(base_dir, 'presets', f'preset_{str(number)}.txt')
    with open(preset_file_path) as file:
        data = []
        for line in file:
            key, value = line.strip().split('=')
            data.append((key, value))
            print("Loading the data: ", key, " ", value)
            if key != "Amba":
                character_list[index(key)].desirability = value
            else:
                amba = character_list[index(value)]
                set_amba(amba)

    return data


# =================================================================================================================
#
# Getting and setting characters, lists, etc
#
# =================================================================================================================
# presets_frame has the buttons and labels for choosing and saving the current preset
# =================================================================================================================

def set_amba(amba):
    global ambassador
    ambassador = amba


def get_amba():
    global ambassador
    return ambassador


def get_characters_list():
    return character_list


def get_alias_list():
    alias_list = []
    for character in character_list:
        alias_list.append(character.alias)
    return alias_list


def index(character):
    return ord(character.upper()) - ord('A')


def alias_to_index(alias):
    count = 0
    for character in character_list:
        if character.alias == alias:
            return count
        count += 1


def print_character_list(characters):
    count = 1
    for person in characters:
        print(f"{count:2}) {person}")
        count += 1


character_list = [
    Character("A", "Disney"),
    Character("B", "Boots"),
    Character("C", "Taft"),
    Character("D", "Papa"),
    Character("E", "Pearls"),
    Character("F", "Alice"),
    Character("G", "General"),
    Character("H", "Oprah"),
    Character("I", "Wheels"),
    Character("J", "Queen"),
    Character("K", "Sikh"),
    Character("L", "Rocker"),
    Character("M", "Plain"),
    Character("N", "Bling"),
    Character("O", "Irish"),
    Character("P", "Carlos"),
    Character("Q", "Salmon"),
    Character("R", "Teal"),
    Character("S", "Smalls"),
    Character("T", "Sari"),
    Character("U", "Duke")
]
