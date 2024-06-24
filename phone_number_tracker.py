import tkinter as tk
from tkinter import StringVar, Label, Entry, Button, Frame, Listbox, Scrollbar, END, messagebox, Menu
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import csv
import webbrowser
import pyperclip
import logging

logging.basicConfig(level=logging.DEBUG)

def validate_phone_number(number):
    try:
        parsed_number = phonenumbers.parse(number)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def Track():
    enter_number = entry.get()
    if not validate_phone_number(enter_number):
        messagebox.showerror("Invalid Number", "Please enter a valid phone number")
        return

    number = phonenumbers.parse(enter_number)

    # Add number to history
    if enter_number not in history_listbox.get(0, END):
        history_listbox.insert(END, enter_number)

    display_information(number)

def display_information(number):
    try:
        # Country
        locate = geocoder.description_for_number(number, 'en')
        country.config(text=f"Country: {locate}")

        # Operator
        operator = carrier.name_for_number(number, 'en')
        sim.config(text=f"SIM: {operator}")

        # Timezone
        time = timezone.time_zones_for_number(number)
        zone.config(text=f"Timezone: {', '.join(time)}")

        # Longitude and Latitude
        geolocator = Nominatim(user_agent='geoapiExercises')
        location = geolocator.geocode(locate)
        if location:
            lng = location.longitude
            lat = location.latitude
            longitude.config(text=f"Longitude: {lng}")
            latitude.config(text=f"Latitude: {lat}")

            # Additional geographical information
            address_parts = location.address.split(',')
            city.config(text=f"City: {address_parts[-5].strip() if len(address_parts) > 4 else 'Unknown'}")
            state.config(text=f"State: {address_parts[-3].strip() if len(address_parts) > 2 else 'Unknown'}")

            # Time showing in phone
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=lng, lat=lat)
            if result:
                home = pytz.timezone(result)
                local_time = datetime.now(home)
                current_time = local_time.strftime('%I:%M %p')
                clock.config(text=f"Phone Time: {current_time}")
            else:
                clock.config(text="Phone Time: Unknown")

            # Show location on map
            map_button.config(state="normal", command=lambda: webbrowser.open(f"https://www.google.com/maps?q={lat},{lng}"))
        else:
            longitude.config(text="Longitude: Unknown")
            latitude.config(text="Latitude: Unknown")
            city.config(text="City: Unknown")
            state.config(text="State: Unknown")
            clock.config(text="Phone Time: Unknown")
            map_button.config(state="disabled")

    except Exception as e:
        logging.error(f"Error in display_information: {e}")
        messagebox.showerror("Error", f"An error occurred while fetching information: {e}")

def load_from_history(event):
    try:
        selected_number = history_listbox.get(history_listbox.curselection())
        entry.set(selected_number)
        number = phonenumbers.parse(selected_number)
        display_information(number)
    except Exception as e:
        logging.error(f"Error in load_from_history: {e}")
        messagebox.showerror("Error", f"An error occurred while loading history: {e}")

def clear_history():
    try:
        history_listbox.delete(0, END)
    except Exception as e:
        logging.error(f"Error in clear_history: {e}")
        messagebox.showerror("Error", f"An error occurred while clearing history: {e}")

def export_history():
    try:
        with open("phone_number_history.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for number in history_listbox.get(0, END):
                writer.writerow([number])
        messagebox.showinfo("Export History", "History exported successfully as phone_number_history.csv")
    except Exception as e:
        logging.error(f"Error in export_history: {e}")
        messagebox.showerror("Error", f"An error occurred while exporting history: {e}")

def copy_to_clipboard():
    try:
        details = f"{country.cget('text')}\n{sim.cget('text')}\n{zone.cget('text')}\n{clock.cget('text')}\n{longitude.cget('text')}\n{latitude.cget('text')}\n{city.cget('text')}\n{state.cget('text')}"
        pyperclip.copy(details)
        messagebox.showinfo("Copied", "Phone number details copied to clipboard")
    except Exception as e:
        logging.error(f"Error in copy_to_clipboard: {e}")
        messagebox.showerror("Error", f"An error occurred while copying to clipboard: {e}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Phone Number Tracker")
root.geometry("600x750+300+50")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Menu
menu = Menu(root)
root.config(menu=menu)
file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export History", command=export_history)
file_menu.add_command(label="Clear History", command=clear_history)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Entry Frame
entry_frame = Frame(root, bg="#34495e")
entry_frame.place(x=50, y=20, width=500, height=100)

entry_label = Label(entry_frame, text="Enter the phone number here with country code:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
entry_label.pack(anchor="w", padx=10, pady=(10, 5))

entry = StringVar()
enter_number = Entry(entry_frame, textvariable=entry, width=25, justify="center", bd=0, font=("Arial", 20))
enter_number.pack(side=tk.LEFT, padx=10)

search = Button(entry_frame, text="Search", borderwidth=0, cursor="hand2", bd=0, command=Track, font=("Arial", 15), bg="blue", fg="white")
search.pack(side=tk.RIGHT, padx=10)

# History Frame
history_frame = Frame(root, bg="#34495e")
history_frame.place(x=50, y=140, width=500, height=200)  # Reduce width from 500 to 400

history_label = Label(history_frame, text="History:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
history_label.pack(anchor="w", padx=10, pady=(10, 5))

history_listbox = Listbox(history_frame, height=8, width=40, bg="#ecf0f1", font=("Arial", 12), selectbackground="#3498db", selectforeground="white")
history_listbox.pack(pady=(5, 10), padx=(10, 0), anchor="center", expand=True, fill="both")  # Adjust width and center align

scrollbar = Scrollbar(history_frame, orient="vertical")
scrollbar.config(command=history_listbox.yview)
scrollbar.pack(side="right", fill="y", pady=(5, 10))

history_listbox.config(yscrollcommand=scrollbar.set)
history_listbox.bind('<<ListboxSelect>>', load_from_history)

clear_button = Button(history_frame, text="Clear History", borderwidth=0, cursor="hand2", bd=0, command=clear_history, font=("Arial", 12), bg="red", fg="white")
clear_button.pack(pady=(5, 10), anchor="e", padx=(0, 10))


# Information Frame
info_frame = Frame(root, bg="#34495e")
info_frame.place(x=50, y=350, width=500, height=350)

row_idx = 0

country = Label(info_frame, text="Country:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
country.grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")

sim = Label(info_frame, text="SIM:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
sim.grid(row=row_idx, column=1, padx=20, pady=10, sticky="w")

row_idx += 1

zone = Label(info_frame, text="Timezone:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
zone.grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")

clock = Label(info_frame, text="Phone Time:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
clock.grid(row=row_idx, column=1, padx=20, pady=10, sticky="w")

row_idx += 1

longitude = Label(info_frame, text="Longitude:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
longitude.grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")

latitude = Label(info_frame, text="Latitude:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
latitude.grid(row=row_idx, column=1, padx=20, pady=10, sticky="w")

row_idx += 1

city = Label(info_frame, text="City:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
city.grid(row=row_idx, column=0, padx=20, pady=10, sticky="w")

state = Label(info_frame, text="State:", bg="#34495e", fg="white", font=("Arial", 12, "bold"))
state.grid(row=row_idx, column=1, padx=20, pady=10, sticky="w")

row_idx += 1

map_button = Button(info_frame, text="Show on Map", state="disabled", borderwidth=0, cursor="hand2", bd=0, font=("Arial", 12), bg="#2980b9", fg="white")
map_button.grid(row=row_idx, column=0, columnspan=2, pady=(10, 5))

row_idx += 1

copy_button = Button(info_frame, text="Copy to Clipboard", borderwidth=0, cursor="hand2", bd=0, command=copy_to_clipboard, font=("Arial", 12), bg="#27ae60", fg="white")
copy_button.grid(row=row_idx, column=0, columnspan=2, pady=(5, 10))

root.mainloop()
