import tkinter
import customtkinter
import characters
from PIL import Image

character_path = r'C:\Users\Max\PycharmProjects\SpyPartyCharacterPicker\images\character_portraits'
global root
global selected_preset
global purple
purple = "#bf00bf"
blue = "#032368"

def main():

    # =================================================================================================================
    # Root creation and settings
    # =================================================================================================================
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")   # blue, dark-blue, green

    global root
    root = customtkinter.CTk()
    root.title("SpyParty Guest Optimizer")
    root.geometry("1280x500")
    root.resizable(width=False, height=False)
    root.iconbitmap(r"C:\Users\Max\PycharmProjects\SpyPartyCharacterPicker\images\S.ico")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.configure(fg_color="black")

    # =================================================================================================================
    #
    # Frames
    #
    # =================================================================================================================
    # parent_frame main frame which all other frames will be organized into
    # =================================================================================================================
    parent_frame = customtkinter.CTkFrame(master=root, fg_color = "black", bg_color="black")
    parent_frame.pack(padx=0, pady=0)

    # =================================================================================================================
    #
    # Desirability Frame
    #
    # =================================================================================================================
    # desirability_frame contains all portraits of characters and their buttons to change their settings
    # =================================================================================================================
    desirability_frame = customtkinter.CTkFrame(master=parent_frame, bg_color="black")
    desirability_frame.grid(row=1, column=0, sticky='e')
    desirability_frame.rowconfigure = 5
    desirability_frame.columnconfigure = 30

    # label for desirability_frame showing the name of the frame at the top of it with a banner behind
    label = customtkinter.CTkLabel(master=desirability_frame, text="Desirability", bg_color=blue)
    label.grid(row=0, column=0, columnspan=50, padx=0, pady=0, sticky='news')

    # will hold all portraits of characters
    portraits_frame = customtkinter.CTkFrame(master=desirability_frame, fg_color="black", corner_radius=0)
    portraits_frame.grid(row=1, column=0, columnspan=50, padx=0, pady=0, sticky='news')

    # activates the optimize_guests() function within the characters file to move characters depending on desirability
    optimize_frame = customtkinter.CTkFrame(master=portraits_frame, corner_radius=0, fg_color="black")
    optimize_frame.grid(row=0, column=0, sticky='n', padx=5, pady=5)
    optimize_guests_button = customtkinter.CTkButton(master=optimize_frame, text="Optimize", height=96, width=96, corner_radius=0, command=characters.optimize_cast)
    optimize_guests_button.grid(row=0, column=0, columnspan=1, padx=5, pady=(5, 43), sticky='nw')

    # updates the character's information when an option is chosen within the desirability_option menu
    def create_desirability_selected_callback(char):
        def desirability_selected(choice):
            char.desirability = choice
            print(choice + " selected from option menu for " + char.alias)

        return desirability_selected

    # creates a frame containing the portrait, option menu, and label for a character then returns that frame
    def create_character_frame(person):
        print("Creating character_frame for ", person.alias)
        character_frame = customtkinter.CTkFrame(master=portraits_frame, bg_color="white", fg_color="black", corner_radius=0)

        path = character_path + '\\' + character.name + '.png'
        portrait = customtkinter.CTkImage(light_image=Image.open(path), size=(96, 96))
        character_portrait = customtkinter.CTkLabel(master=character_frame, image=portrait, text="", corner_radius=0)
        character_portrait.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='w')

        string_values = [str(value) for value in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
        desirability_menu = customtkinter.CTkOptionMenu(master=character_frame, values=string_values, width=40, height=20)
        desirability_menu.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='w')
        desirability_menu.set(character.desirability)
        callback = create_desirability_selected_callback(character)
        desirability_menu.configure(command=callback)
        character.desirability_option = desirability_menu

        name_label = customtkinter.CTkLabel(master=character_frame, text=character.alias)
        name_label.grid(row=1, column=0, columnspan=2, padx=(55, 0), pady=5, sticky='e')

        return character_frame

    # =================================================================================================================
    # creating and placing frames for each character
    # =================================================================================================================
    character_list = characters.get_characters_list()
    row_number = 0
    column_number = 1

    for character in character_list:
        if character.name == 'K':
            row_number = 1
            column_number = 0
        frame = create_character_frame(character)
        frame.grid(row=row_number, column=column_number, padx=5, pady=5)
        column_number += 1

    

    # =================================================================================================================
    # refinement_settings has the button for changing the Ambassador
    # =================================================================================================================
    refinement_settings_frame = customtkinter.CTkFrame(master=parent_frame, border_color="black", border_width=2, bg_color="black")
    refinement_settings_frame.grid(row=2, column=0, padx=260, pady=0, sticky='w')
    refinement_settings_frame.rowconfigure = 3
    refinement_settings_frame.columnconfigure = 10

    # frame and menu for choosing ambassador
    choose_amba_frame = customtkinter.CTkFrame(master=refinement_settings_frame, fg_color="black", bg_color="black")
    choose_amba_frame.grid(row=0, column=1)
    names_list = characters.get_alias_list()

    amba = characters.get_amba()
    amba_portrait_frame = customtkinter.CTkFrame(master=choose_amba_frame, border_color=purple, border_width=2, fg_color="black", bg_color="black")
    amba_portrait_frame.grid(row=0, column=0, padx=5, pady=5)
    path = character_path + '\\' + amba.name + '.png'
    portrait = customtkinter.CTkImage(light_image=Image.open(path), size=(96, 96))
    amba_portrait = customtkinter.CTkLabel(master=amba_portrait_frame, image=portrait, text="")
    amba_portrait.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='w')

    amba_option_menu = customtkinter.CTkOptionMenu(master=choose_amba_frame, values=names_list, width=100)
    amba_option_menu.set(amba.alias)
    amba_option_menu.grid(row=1, column=0, padx=5, pady=(0,5))

    def update_ambassador_choice(choice):
        amba = character_list[characters.alias_to_index(choice)]
        print("Updating amba to be ", amba.name, ": ", amba.alias)
        characters.set_amba(amba)
        amba_option_menu.configure(characters.get_amba().alias)
        path = character_path + '\\' + amba.name + '.png'
        portrait = customtkinter.CTkImage(light_image=Image.open(path), size=(96, 96))
        amba_portrait.configure(image=portrait)

    # Function to update the ambassador portrait and name
    def update_ambassador_display(ambassador):
        # Update the portrait
        path = character_path + '\\' + ambassador.name + '.png'
        portrait = customtkinter.CTkImage(light_image=Image.open(path), size=(96, 96))
        amba_portrait.configure(image=portrait)

        # Update the name
        amba_option_menu.set(ambassador.alias)


    amba_option_menu.configure(command=update_ambassador_choice)

    # =================================================================================================================
    #
    # Presets and miscellaneous settings
    #
    # =================================================================================================================
    # presets_frame has the buttons and labels for choosing and saving the current preset
    # =================================================================================================================
    presets_frame = customtkinter.CTkFrame(master=parent_frame, border_color="black", border_width=2, bg_color="black")
    presets_frame.grid(row=2, column=0, sticky='w')
    presets_frame.rowconfigure = 2
    presets_frame.columnconfigure = 10
    number_presets = 6

    row_number = 0
    col_offset = 0

    presets_header = customtkinter.CTkLabel(master=presets_frame, text="Preset Settings")
    presets_header.grid(row=row_number, column=0, rowspan=1, columnspan=10, padx=5, pady=(5, 0), sticky='news')

    row_number += 1

    def load_preset(number):
        print("Currently Loading Preset Number: ", number)
        count = 0
        data = characters.read_preset(number)  # Reads the preset file and returns key-value pairs

        for key, value in data:
            if key != "Amba":
                index = characters.index(key)  # Get the index of the character
                person = character_list[index]
                button = person.desirability_option
                button.set(value)  # Set the desirability in the option menu
            else:
                ambassador = character_list[characters.index(value)]
                characters.set_amba(ambassador)
                print("Set ambassador to " + ambassador.alias)
                update_ambassador_display(ambassador)

        count += 1

    # Helper function to handle preset selection
    def preset_click(preset_num):
        global selected_preset
        selected_preset = preset_num
        print(f"Preset {preset_num} Selected")

        # Deselect other radio buttons dynamically
        for i in range(1, number_presets + 1):
            if i != preset_num:
                preset_buttons[i].deselect()

        # Load the selected preset
        load_preset(preset_num)


    button_padding = (5, 0)
    text_padding = (0, 5)

    # Generic function to create preset radio buttons and labels
    def create_preset_button(preset_num, row, column_offset):
        preset_button = customtkinter.CTkRadioButton(
            master=presets_frame, text="", width=20, height=20, 
            command=lambda: preset_click(preset_num)
        )
        preset_button.grid(row=row, column=column_offset, rowspan=1, columnspan=1, padx=button_padding, pady=5, sticky='ne')

        preset_label = customtkinter.CTkLabel(master=presets_frame, text=f"Preset {preset_num}")
        preset_label.grid(row=row, column=column_offset + 1, rowspan=1, columnspan=1, padx=text_padding, pady=5, sticky='ne')

        return preset_button

    # Creating preset buttons dynamically
    row_number = 1
    starting_column = 0
    col_offset = 0

    # Dictionary to store radio buttons for later deselecting
    preset_buttons = {}

    for preset_num in range(1, number_presets + 1):
        if ((col_offset / 2) % 3 == 0): # Create preset buttons rows of 3 columns
            row_number += 1
            col_offset = 0
        preset_buttons[preset_num] = create_preset_button(preset_num, row_number, starting_column + col_offset)
        col_offset += 2  # Move to the next set of columns

    def save_preset():
        global selected_preset
        print("Saving Preset to " + str(selected_preset))
        filename = r'C:\Users\Max\PycharmProjects\SpyPartyCharacterPicker\presets\preset_' + str(
            selected_preset) + '.txt'
        file = open(filename, 'w')
        for person in character_list:
            file.write(person.name + "=" + person.desirability + '\n')
        file.write("Amba=" + characters.get_amba().name + '\n')

    
    # Select the first preset by default
    preset_buttons[1].select()
    preset_click(1)
    row_number += 1

    save_presets_button = customtkinter.CTkButton(master=presets_frame, text="Save Current Preset", command=save_preset)
    save_presets_button.grid(row=row_number, column=0, columnspan=6, padx=2, pady=3, sticky='news')

    root.mainloop()
