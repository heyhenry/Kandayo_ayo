# Todo next session: 
# - Double check dictionary retains valid information and format
# - Learn how to store the characters dictionary nicely into json storage file ('chars_save.json')
# - Learn how to redistribute characters dictionary content as string for display etc (if its an issue)
# - create function that updates the characters dictionary as well as the storage file simultaneously 
# - create function or add onto an existing function that reflects and implements these changes in the listbox in real time as well
# - create delete character entry function
# - update character details function 
# - figure a way to incorporate the boss checklist for each character
# - - maybe add all the bosses as vars in the charInfo and update add_char popup to reflect ability to select bosses
# - - maybe just have a new popup display the bosses, with relevant stuff (bosses killed, party size, mesos gained) that gets saved as a separate obj? (cont.)
# - - (cont. ^) maybe second boss obj can be added in a list form for characters i.e. {char_name : [charinfo obj, bossing obj]} ? main thing - find a way to retain player's character progression (cont.)
# - - (cont. ^) maybe forget about the mesos accumulated (party size identification/calculations) for the time being and have it as a simple boss checklist

import tkinter as tk
from datetime import timezone, timedelta
import datetime as dt
import webbrowser
from charinfo import CharInfo
import json
import os # note to self: needed to find json file from prev experience

# list of charinfo (characters) objs
characters = {}

storage_filename = 'chars_save.json'

# custom json serializer
def custom_serializer(obj):
    if isinstance(obj, CharInfo):
        return {
            'ign': obj.ign,
            'job': obj.job,
            'level': obj.level,
            'capped': obj.capped
        }
    return obj

# create a new character entry
def create_char(ign, job, level):

    # loads the existing character entries into the characters dictionary
    load_characters()

    # create a new character obj
    new_char = CharInfo(ign, job, level, False)
    
    # add new character obj to the characters dictionary
    characters[new_char.ign] = new_char
    
    # set serialization for characters dictionary for json save file / serialize the characters dictionary to json string
    json_data = json.dumps(characters, default=custom_serializer, indent=4)
    
    # save latest version of characters dictionary to the json save file / updates the json save file with latest data
    with open(storage_filename, 'w') as outfile:
        outfile.write(json_data)

# read and add existing character entries found in the json save file to the characters dictionary
def load_characters():

    # check if file exists
    if os.path.exists(storage_filename):

        # read the file
        with open(storage_filename, 'r') as file:

            # load the json file data
            characters_data = json.load(file)

            # update the characters dictionary with existing character entries in the selected json save file
            for char_ign, char_info in characters_data.items():
                characters[char_ign] = CharInfo(char_ign, char_info['job'], char_info['level'], char_info['capped'])

# to check if characters dictionary is storing data correctly
# def check_characters():
#     load_characters()
#     for k, v in characters.items():
#         v.charinfo_str()

# check_characters()

root = tk.Tk()
root.resizable(False, False)

# frames setup
yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nwse')
red_frame.grid(rowspan=4, column=0, sticky='nwse')
blue_frame.grid(row=1, column=1, sticky='nwse')
magenta_frame.grid(row=2, column=1, sticky='nwse')
orange_frame.grid(row=3, column=1, sticky='nwse')
green_frame.grid(row=4, column=1, sticky='nwse')

# to not ignore frame attributes when widgets are introduced
yellow_frame.grid_propagate(False)
red_frame.grid_propagate(False)

# yellow frame
co_lbl = tk.Label(yellow_frame, text='Characters Overview', font=('Kozuka Gothic Pro B', 18), bg='yellow')
co_lbl.place(relx=0.5, rely=0.5, anchor='center')

# red frame
chars_lb = tk.Listbox(red_frame, height=30)
chars_lb.place(relx=0.5, rely=0.5, anchor='center')

# blue frame

# to check if buttons are working correctly
def run(i : str):
    if i == 'add':
        print('add works')
    elif i == 'upd':
        print('update works')
    elif i == 'del':
        print('delete works')
    else:
        print('Error!')

# add a new character pop-up window
def add_character_popup():

    ac_ign = tk.StringVar()
    ac_job = tk.StringVar()
    ac_level = tk.StringVar()

    aesthetic_params = {'font': ('Kozuka Gothic Pro B', 12)}

    # close pop-up window
    def close_ac():
        ac_win.destroy()

    # ac short for add_character
    ac_win = tk.Toplevel(blue_frame)
    ac_win.title('Add New Character')
    ac_win.geometry('300x200+650+150')
    
    ac_title_lbl = tk.Label(ac_win, text='Add New Character', **aesthetic_params)
    ac_ign_lbl = tk.Label(ac_win, text='In-Game Name:', **aesthetic_params)
    ac_ign_entry = tk.Entry(ac_win, textvariable=ac_ign)
    ac_job_lbl = tk.Label(ac_win, text='Job (Class):', **aesthetic_params)
    ac_job_entry = tk.Entry(ac_win, textvariable=ac_job)
    ac_level_lbl = tk.Label(ac_win, text='Level:', **aesthetic_params)
    ac_level_entry = tk.Entry(ac_win, textvariable=ac_level)
    ac_submit_btn = tk.Button(ac_win, text='Add to Roster', command=lambda:create_char(ac_ign.get(), ac_job.get(), ac_level.get()), **aesthetic_params)
    ac_cancel_btn = tk.Button(ac_win, text='Cancel', command=close_ac, **aesthetic_params)

    ac_title_lbl.grid(row=0, columnspan=2)
    ac_ign_lbl.grid(row=1, column=0)
    ac_ign_entry.grid(row=1, column=1)
    ac_job_lbl.grid(row=2, column=0)
    ac_job_entry.grid(row=2, column=1)
    ac_level_lbl.grid(row=3, column=0)
    ac_level_entry.grid(row=3, column=1)
    ac_submit_btn.grid(row=4, column=0)
    ac_cancel_btn.grid(row=4, column=1)

    ac_win.rowconfigure(0, weight=1)
    ac_win.rowconfigure(1, weight=1)
    ac_win.rowconfigure(2, weight=1)
    ac_win.rowconfigure(3, weight=1)
    ac_win.rowconfigure(4, weight=1)
    ac_win.columnconfigure(0, weight=1)
    ac_win.columnconfigure(1, weight=1)

btn_params = {'font':('Kozuka Gothic Pro B', 12), 'relief': 'raised'}

addchar_btn = tk.Button(blue_frame, text='Add Char', **btn_params, command=add_character_popup)
updchar_btn = tk.Button(blue_frame, text='Update Char', **btn_params, command=lambda:run('upd'))
delchar_btn = tk.Button(blue_frame, text='Delete Char', **btn_params, command=lambda:run('del'))

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)
blue_frame.grid_columnconfigure(2, weight=1)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=0, column=2)

# magenta frame

# updates the utc time clock aka server time
def update_utc():
    # finds the utc timezone's time
    utc_time = dt.datetime.now(timezone.utc)
    # reformats the time to string 
    string_time = utc_time.strftime('%H:%M:%S %p')
    # updates the display label that showcases the utc time
    utc_livetime_lbl.config(text=f"Current Server Time: {string_time}")
    # executes the update_utc function after time elapse (in ms)
    utc_livetime_lbl.after(1000, update_utc)

# ursus time countdown and tracker algorithm (sidenote: bonus as in 2x rewards)
def bonus_ursus_tracker():

    # ursus time ranges
    uto_start_str = '01:00:00'
    uto_end_str = '05:00:00'

    utt_start_str = '18:00:00'
    utt_end_str = '22:00:00'

    # get the current utc time aka server time
    utc_time = dt.datetime.now(timezone.utc)

    # get today's day
    today = utc_time.date()

    # create datetime objects for the ursus times (aka the triggers)
    uto_start = dt.datetime.combine(today, dt.datetime.strptime(uto_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    uto_end = dt.datetime.combine(today, dt.datetime.strptime(uto_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    utt_start = dt.datetime.combine(today, dt.datetime.strptime(utt_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    utt_end = dt.datetime.combine(today, dt.datetime.strptime(utt_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # check if server time is currently within the bonus ursus time period
    if utc_time >= uto_start and utc_time <= uto_end:
        ursus_time_lbl.config(text="It's Ursus 2x Now! (Round 1)")
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    elif utc_time >= utt_start and utc_time <= utt_end:
        ursus_time_lbl.config(text="It's Ursus 2x Now! (Round 2)")
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    else:
        # determine when the next trigger is (aka ursus bonus time)
        if utc_time <= uto_start:
            next_ursus = uto_start
        elif utc_time <= utt_start:
            next_ursus = utt_start
        else:
            # if the current time has passed for both triggers (ursus times), next_ursus will store the first ursus of the next day
            next_ursus = uto_start + timedelta(days=1)

            # calculate the time remaining til next bonus ursus
            time_remaining = next_ursus - utc_time

            # extract the components of the time_remaining object (timedelta object)
            days = time_remaining.days
            seconds = time_remaining.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = (seconds % 3600) % 60

            # format the result for time remaining
            time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

            # update the ursus_time label with relevant realtime 
            ursus_time_lbl.config(text=f"Next Ursus is at {next_ursus.strftime('%H:%M:%S')} \n Time Remaining until next Ursus: {time_remaining_str}")
            # prompt execution of function every second for a live reading of the ursus time tracker
            ursus_time_lbl.after(1000, bonus_ursus_tracker)

# update time remaining until daily reset
def daily_reset():

    # the new day trigger
    trigger_str = '00:00:00'

    # current time 
    utc_time = dt.datetime.now(timezone.utc)

    # setup datetime obj
    today = utc_time.date()
    trigger = dt.datetime.combine(today, dt.datetime.strptime(trigger_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # calculate time remaining until new day
    time_remaining = (trigger + timedelta(days=1)) - utc_time
    
    # extract components of the time_remaining timedelta obj
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # create string format of time remaining data
    time_remaining_str = f"Daily Reset in {hours} hours, {minutes} minutes, {seconds} seconds"

    # update the label responsible for displaing the daily reset timer
    daily_reset_lbl.config(text=time_remaining_str)

    # auto execute daily_reset function every second
    daily_reset_lbl.after(1000, daily_reset)

# update time remaining until weekly reset
def weekly_reset():

    # get current utc datetime and other details
    utc_time = dt.datetime.now(timezone.utc)
    today = utc_time.date()
    current_weekday = utc_time.weekday()

    # the target day (i.e. thursday)
    target_weekyday = 3

    # calculate how many days until target day
    days_until_target = (target_weekyday - current_weekday + 7) % 7

    # check to see if today is target day and reset to 7 days if its today
    if days_until_target == 0:
        days_until_target = 7

    # next thursday timedelta obj
    next_thursday_date = today + timedelta(days=days_until_target)

    # target day settings
    trigger_str = '00:00:00'
    trigger_time = dt.datetime.strptime(trigger_str, '%H:%M:%S').time()

    # next thursday datetime obj
    next_thursday = dt.datetime.combine(next_thursday_date, trigger_time, tzinfo=timezone.utc)
    
    # check if today is the target day
    if utc_time.weekday() == 3:
        print('Weekly Reset is Today')
        weekly_reset_lbl.after(1000, weekly_reset)
    # if its not the target day ..
    else:
        # calcuate the time remaining until next thursday from today
        time_remaining = next_thursday - utc_time

        # extract components from the time_remaining timedelta obj
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60

        # string format of time_remaining info
        time_remaining_str = f"Weekly Reset in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        # update weekly_reset label
        weekly_reset_lbl.config(text=time_remaining_str)

        # auto execute weekly_reset function after a second
        weekly_reset_lbl.after(1000, weekly_reset)

# temp using blue_button params
utc_livetime_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
ursus_time_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
daily_reset_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
weekly_reset_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')

utc_livetime_lbl.grid(row=0, column=0)
ursus_time_lbl.grid(row=1, column=0)
daily_reset_lbl.grid(row=2, column=0)
weekly_reset_lbl.grid(row=3, column=0)

magenta_frame.grid_rowconfigure(0, weight=1)
magenta_frame.grid_rowconfigure(1, weight=1)
magenta_frame.grid_rowconfigure(2, weight=1)
magenta_frame.grid_rowconfigure(3, weight=1)
magenta_frame.grid_columnconfigure(0, weight=1)

# orange frame

balance_lbl = tk.Label(orange_frame, text='Accumulated Balance: $ XXXXXXXXXX', font=('Kozuka Gothic Pro B', 12), background='orange')
reset_bal_btn = tk.Button(orange_frame, text='Reset Balance', **btn_params)

balance_lbl.grid(row=0, column=0)
reset_bal_btn.grid(row=1, column=0)

orange_frame.grid_rowconfigure(0, weight=1)
orange_frame.grid_rowconfigure(1, weight=1)
orange_frame.grid_columnconfigure(0, weight=1)

# green frame

# opens website when prompted
def redirect_flame_calc():
    webbrowser.open(r"https://starlinez.github.io/games/maplestory/item-flames")

# opens website when prompted
def redirect_bossing_guide():
    webbrowser.open(r"https://www.youtube.com/watch?v=y74KWpY9xQ0&list=PLa2-sX6gKTH_63Zfjp_W2cmWX7t6rnOuM")

# opens website when prompted
def redirect_wse_calc():
    webbrowser.open(r"https://brendonmay.github.io/wseCalculator/")

guide_calc_lbl = tk.Label(green_frame, text='Guides & Calculators', font=('Kozuka Gothic Pro B', 12), background='green')
flame_calc_btn = tk.Button(green_frame, text='Flame Score Calculator', **btn_params, command=redirect_flame_calc)
bossing_guide_btn = tk.Button(green_frame, text='Curated List of Bossing Guides', **btn_params, command=redirect_bossing_guide)
wse_calc_btn = tk.Button(green_frame, text='Optimize WSE Calculator', **btn_params, command=redirect_wse_calc)

guide_calc_lbl.grid(row=0, columnspan=3)
flame_calc_btn.grid(row=1, column=0)
bossing_guide_btn.grid(row=1, column=1)
wse_calc_btn.grid(row=1, column=2)

green_frame.grid_rowconfigure(0, weight=1)
green_frame.grid_rowconfigure(1, weight=1)
green_frame.grid_columnconfigure(0, weight=1)
green_frame.grid_columnconfigure(1, weight=1)
green_frame.grid_columnconfigure(2, weight=1)

# root configs for resizability ('can ignore for time being, may reinstate later')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# initial function execution to start off the various clocks and time trackers upon app startup
update_utc()
bonus_ursus_tracker()
daily_reset()
weekly_reset()

root.mainloop()

