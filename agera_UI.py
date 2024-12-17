# Imports
import json
import tkinter as tk
from tkinter import ttk
from tkinter import font
from random import choices, choice
import time as ti


# Aesthetics
black = '#000000'
white = '#fff'
blue = '#0000FF'
neongreen = '#00ff00'
red = '#FF0000'


class PPGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aesthetics
        self.title("Agera - Checkmate")
        self.geometry("800x600")
        self.config(bg=black)
        self.font = font.Font(family="Helvetica", size=15, weight="bold")
        self.resizable(True, True)

        # Prowler Logo
        # desired_width = 50  # in pixels
        # desired_height = 50
        # self.p_image = Image.open('prowler.ico')
        # self.p_image = self.p_image.resize((desired_width, desired_height), Image.LANCZOS)
        # self.p_image = ImageTk.PhotoImage(self.p_image)


        # Key Bindings
        self.bind("qq", lambda q: self.quit())
        self.bind("qd", lambda d: self.destroy())

        # Init notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Init child notebook check
        self.children_window = None

        # Init self var.s
        self.submit = None  # for save button
        self.sv = ''
        self.duplicate_tabs_window = None  # Variable to store the duplicate tabs window

        # Init contacts dic
        self.contacts = {}

        # Init entry lists
        self.ka_entries = {}
        self.proptest_entries = {}
        self.propfire_entries = {}
        self.spt_entries = {}
        self.oisl_entries = {}
        self.link16_entries = {}

        # Init saving list
        self.activities = []

        # Settings
        # self.settings = mu.get_settings()

    # =================================================================================================================
    # Parent Frames

    def tab1_sv_selection(self):
        """
        This is the first tab from the initialization window.
        It has the standard format for the GUI's functionality.
        """
        # Forget previous packs here

        # Init tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="SV Selection")

        # Prowler logo
        # img_label = tk.Label(tab1, image=self.p_image)
        # img_label.pack(side='top', anchor='nw', padx=10, pady=10)

        # Receive inputs
        text = "SV Number (eg. 1, 1001, etc.)"
        self.txt = tk.Label(tab1, text=text, bg=black, fg=neongreen,
                            font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.txt.pack(side=tk.TOP, ipady=15)

        # Entry for SV
        self.sv_entry = ttk.Entry(tab1, font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.sv_entry.insert(0, "1001")
        self.sv_entry.pack(pady=10)

        # Init save button
        self.launch_button()

    def tab2_set_hours(self):
        text = "Set Hours to Write Out for Histy Selection:"

        # Init tab
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Hours Selection")

        # Logo
        # img_label = tk.Label(tab2, image=self.p_image)
        # img_label.pack(side='top', anchor='nw', padx=10, pady=10)

        # Receive Inputs
        self.txt = tk.Label(tab2, text=text, bg=black, fg=neongreen,
                            font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.txt.pack(side=tk.TOP, ipady=15)

        self.hrs_resp = ttk.Entry(tab2, font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.hrs_resp.insert(0, "24")
        self.hrs_resp.pack(side=tk.TOP, ipady=10)

    # =================================================================================================================
    # Initialization/Processing Parent Inputs

    def launch_button(self):
        if self.submit is None:
            self.submit = tk.Button(self, text="Launch", command=self.launch_query, bg='#f55555', fg=white,
                                    font=font.Font(family="Helvetica", size=15, weight="bold"))
            self.submit.pack(side=tk.BOTTOM)

    def launch_query(self):
        """
        Makes prowler object to work within
        Launches all activity tabs
        Makes API page possible
        """
        # Assign necessary vars
        self.sv = self.sv_entry.get()
        self.hrs_out = self.hrs_resp.get()

        # Initialize API pull here (removed)

        # Launch Children
        self.launch_child_window()

    # =================================================================================================================
    # Launch Child Window/Frames

    def launch_child_window(self):

        # Close the children tabs window if it exists
        if self.children_window:
            self.children_window.destroy()

        # Create a new Toplevel window for child tabs
        self.children_window = tk.Toplevel(self)
        self.children_window.title("Mission Operations Product")
        self.children_window.config(bg=black)
        self.children_window.geometry("800x600")

        # Create new Notebook for Child window
        self.children_notebook = ttk.Notebook(self.children_window)
        self.children_notebook.pack(expand=True, fill='both')

        # Launch all activities
        '''
        the order in which these are called is important for the appending function for scratch 
        '''
        self.ka_inputstab()
        self.link16_inputstab()
        self.proptest_inputstab()
        self.propfire_inputstab()
        self.oisl_inputstab()
        self.cont_histy_tab()

    # =================================================================================================================
    # Child SPT/Histy Frame - Separate because working

    def cont_histy_tab(self):
        """
        This tab would perform an API pull and allow the user to select between various options.
        """
        label_font = font.Font(family="Helvetica", size=15, weight="bold")

        # Init Frame for Func
        tt = "Activity Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        text = "Select option for activity:"

        self.txt = tk.Label(tab, text=text, bg=black, fg=neongreen, font=label_font)
        self.txt.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a canvas to add a scrollbar
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        self.hist_bool_list = []
        self.spt_bool_list = []

        for idx, contact in enumerate(self.contacts):
            boolin_apply = tk.BooleanVar(value=True)
            boolin_other = tk.BooleanVar(value=False)

            hist_butt_frame = tk.Frame(scrollable_frame, bg=blue)
            spt_butt_frame = tk.Frame(scrollable_frame, bg=red)

            hist_cbox = tk.Checkbutton(hist_butt_frame, variable=boolin_apply, onvalue=True,
                                               offvalue=False, highlightthickness=0, bd=0, bg=blue)
            spt_cbox = tk.Checkbutton(spt_butt_frame, variable=boolin_other, onvalue=True,
                                               offvalue=False, highlightthickness=0, bd=0, bg=red)

            contact_label = tk.Label(scrollable_frame, text=display_cont(contact), bg=white, fg=black, font=label_font)

            self.hist_bool_list.append(boolin_apply)
            self.spt_bool_list.append(boolin_other)

            hist_butt_frame.grid(row=idx, column=0, sticky="w", pady=5, padx=5)
            hist_cbox.pack()

            spt_butt_frame.grid(row=idx, column=1, sticky="w", pady=5, padx=5)
            spt_cbox.pack()

            contact_label.grid(row=idx, column=2, sticky="w", pady=5, padx=5)

        def cont_idx_butt():
            for contact_idx in range(len(self.contacts)):
                self.contacts[contact_idx]['hist'] = self.hist_bool_list[contact_idx].get()
                self.contacts[contact_idx]['spt'] = self.spt_bool_list[contact_idx].get()
            self.append_to_scratch()

        append_butt = tk.Button(tab, text="Append", command=cont_idx_butt, bg=neongreen, fg=black, font=label_font)
        append_butt.grid(row=2, column=0, columnspan=3, pady=10)

    # =================================================================================================================
    # Child Activity Input Frames

    def ka_inputstab(self):
        """
        Allows user to perform an activity bounded by time and location
        """
        # Init Frame for Func
        tt = "Activity Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        input_font = font.Font(family="Helvetica", size=13, weight="normal")

        label = tk.Label(tab, text=f"KA Activity Tab",
                         font=font.Font(family="Helvetica", size=15, weight="bold"))
        label.grid(row=0, columnspan=3, padx=140, pady=5, sticky='w')

        # SV input (default

        inputs = [
            ('Start Time, eg: 2024-07-09 17:18:51:', 'ka_start_time'),
            ('Location', 'ka_gep_location'),
            ('End Time, eg: 2024-07-09 17:24:51:', 'ka_end_time')
        ]

        self.ka_entries = {}

        for i, (label_text, key) in enumerate(inputs):
            label = tk.Label(tab, text=label_text, font=input_font)
            label.grid(row=i + 2, column=0, sticky=tk.W, padx=5, pady=5)

            entry = tk.Entry(tab, width=25, font=input_font)
            entry.grid(row=i + 2, column=1, padx=5, pady=5, sticky=tk.E)

            self.ka_entries[key] = entry


        append_butt = tk.Button(tab, text="Append", command=self.append_to_scratch)
        append_butt.grid(row=len(inputs) + 2, columnspan=2, pady=10)

    def proptest_inputstab(self):
        """

        """
        # Init Frame for Func
        tt = "Prop Test Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        input_font = font.Font(family="Helvetica", size=13, weight="normal")

        label = tk.Label(tab, text=f"Proptest Activity Tab",
                         font=font.Font(family="Helvetica", size=15, weight="bold"))
        label.grid(row=0, columnspan=3, padx=140, pady=5, sticky='w')

        inputs = [
            ('Start Time, eg: 2024-05-08 14:25:51:', 'start_time'),
            ('Location:', 'gep_location'),
            ('Duration, e.g. 30:', 'attempt_duration'),
            ('Duration Min, e.g. 0:', 'thrust_dur_min'),
            ('Duration Max, e.g. 5:', 'thrust_dur_max')
        ]

        self.proptest_entries = {}

        for i, (label_text, key) in enumerate(inputs):
            label = tk.Label(tab, text=label_text, font=input_font)
            label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)

            entry = tk.Entry(tab, width=25, font=input_font)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

            self.proptest_entries[key] = entry

        append_butt = tk.Button(tab, text="Append", command=self.append_to_scratch)
        append_butt.grid(row=len(inputs) + 2, columnspan=2, pady=10)

    def link16_inputstab(self):
        """
        
        """
        # Init Frame for Func
        tt = "Activity Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        input_font = font.Font(family="Helvetica", size=13, weight="normal")

        self.link16_entries = {}

        default_inputs = [
            ('Where?:', 'link_location'),
            ('X value in km:', 'x_axis'),
            ('Y value in km:', 'y_axis'),
            ('Z value in km:', 'z_axis'),
            ('Time in %Y-%m-%d %H%M%S:', 'time_of_AOR'),
            ('Length in seconds:', 'AOR_length'),
            ('other input:', 'ja_key_fill_bin'),
            ('other input:', 'wkek_key_fill_bin'),
            ('other input:', 'idl_init_file'),
            ('other input:', 'btek_key_fill_bin')
        ]

        self.l16_customo_inputs = [
            ("Custom Orientation: ", 'four_vector_orientation')
        ]

        self.l16_normalo_inputs = []

        # Radiobuttons to select layout
        selected_option = tk.IntVar(value=1)

        # Init content frame for different input routes
        content_frame = ttk.Frame(tab)
        content_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

        def update_inputstab():
            # Clear the current content in the content_frame
            for widget in content_frame.winfo_children():
                widget.destroy()

            self.new_l16_inputs = default_inputs.copy()  # Start with default inputs
            selection = selected_option.get()

            if selection == 1:
                '''
                Normal
                '''

                normalo_entry = tk.Entry(content_frame)
                normalo_entry.insert(0, '.PLUS_Z, .PLUS_X, .ECEF_TGT1, .VELOCITY, 0, 0, 0, 1')
                self.link16_entries['four_vector_orientation'] = normalo_entry

                for i, (label_text, key) in enumerate(self.new_l16_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)

                    if key != 'four_vector_orientation':
                        entry = tk.Entry(content_frame, width=25, font=input_font)
                        entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                        self.link16_entries[key] = entry

            elif selection == 2:
                '''
                Custom
                '''
                self.new_l16_inputs.extend(self.l16_customo_inputs)

                for i, (label_text, key) in enumerate(self.new_l16_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)

                    entry = tk.Entry(content_frame, width=25, font=input_font)
                    entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                    self.link16_entries[key] = entry

        # Add label above radiobuttons
        label_select_target = tk.Label(tab, text="Select Orientation", font=("Helvetica", 15, "bold"))
        label_select_target.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # Define the style for the radiobuttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=("Helvetica", 15, "bold"))

        # Init radiobuttons
        radiobutton1 = ttk.Radiobutton(tab, text="Normal", variable=selected_option, value=1,
                                       command=update_inputstab, style="Custom.TRadiobutton")
        radiobutton2 = ttk.Radiobutton(tab, text="Custom", variable=selected_option, value=2,
                                       command=update_inputstab, style="Custom.TRadiobutton")

        # Pack radiobuttons below the label in a horizontal line
        radiobutton1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        radiobutton2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Make sure the content frame expands properly
        tab.rowconfigure(2, weight=1)
        tab.columnconfigure(0, weight=1)
        for col in range(4):
            tab.columnconfigure(col, weight=1)

        self.propfire_entries = {}

        # Update layout initially based on the default selection
        update_inputstab()

        append_butt = tk.Button(tab, text="Append", command=self.append_to_scratch)
        append_butt.grid(row=len(self.new_l16_inputs) + 2, columnspan=2, pady=10)

    def propfire_inputstab(self):
        """
        Prop Fire Input Tab
        """
        # Init Frame for Func
        tt = "Activity Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        input_font = font.Font(family="Helvetica", size=13, weight="normal")

        # Master inputs list
        self.propfire_entries = {}

        default_inputs = [
            ('Option, eg: yes:', 'fire_onboard'),
            ('Start Time, eg: 2024-05-08 14:25:51:', 'start_time'),
            ('Orientation:', 'orientation'),
            ('x Duration, default x (in seconds): ', 'attempt_duration'),
            ('x Duration, default x (in seconds): ', 'thrust_dur_max'),
            ('x Duration, default x: ', 'apollo_thrust_duration'),
            ('Option, default x: ', 'thrust_attempts')
        ]

        self.gep_inputs = [
            ('Location:', 'gep_location')
        ]

        self.custom_inputs = [
            ('Custom Orientation:', 'fire_orientation'),
            ('Location:', 'gep_location')
        ]

        # Radiobuttons to select layout
        selected_option = tk.IntVar(value=1)

        # Init content frame for different input routes
        content_frame = ttk.Frame(tab)
        content_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

        def update_inputstab():
            # Clear the current content in the content_frame
            for widget in content_frame.winfo_children():
                widget.destroy()

            self.new_pf_inputs = default_inputs.copy()  # Start with default inputs
            selection = selected_option.get()

            if selection == 1:
                '''
                GEP
                '''
                self.new_pf_inputs.extend(self.gep_inputs)
            elif selection == 2:
                '''
                Custom
                '''
                self.new_pf_inputs.extend(self.custom_inputs)

            for i, (label_text, key) in enumerate(self.new_pf_inputs):
                label = tk.Label(content_frame, text=label_text, font=input_font)
                label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)

                entry = tk.Entry(content_frame, width=25, font=input_font)
                entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                self.propfire_entries[key] = entry

        # Add label above radiobuttons
        label_select_target = tk.Label(tab, text="Select : ", font=("Helvetica", 15, "bold"))
        label_select_target.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # Define the style for the radiobuttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=("Helvetica", 15, "bold"))

        # Init radiobuttons
        radiobutton1 = ttk.Radiobutton(tab, text="GEP", variable=selected_option, value=1,
                                       command=update_inputstab, style="Custom.TRadiobutton")
        radiobutton2 = ttk.Radiobutton(tab, text="Custom", variable=selected_option, value=2,
                                       command=update_inputstab, style="Custom.TRadiobutton")

        # Pack radiobuttons below the label in a horizontal line
        radiobutton1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        radiobutton2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Make sure the content frame expands properly
        tab.rowconfigure(2, weight=1)
        tab.columnconfigure(0, weight=1)
        for col in range(4):
            tab.columnconfigure(col, weight=1)

        self.propfire_entries = {}

        # Update layout initially based on the default selection
        update_inputstab()

        append_butt = tk.Button(tab, text="Append", command=self.append_to_scratch)
        append_butt.grid(row=len(self.new_pf_inputs) + 2, columnspan=2, pady=10)

    def oisl_inputstab(self):
        """
        TO-DO:
        - add inputs fn to make the inputs have textboxes
        - figure out what happened with that one button that did the extra steps (attempt type)
        """
        # Init tab
        tt = "Activity Tab"
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text=tt)

        # Init Normal Aesthetics
        input_font = font.Font(family="Helvetica", size=13, weight="normal")

        # Radiobuttons to select layout
        selected_option = tk.IntVar(value=1)

        # Init content frame for different input routes
        content_frame = ttk.Frame(tab)
        content_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

        # Master entries dic
        self.oisl_entries = {}

        # Init inputs lists (lists of tuples)
        default_inputs = [
            ('Input Host OISL ID (1 or 2):', 'host_oisl_id')
        ]

        moon_inputs = [
            ('t0_attempt_time (YYYY-MM-DD HH:MM:SS): ', 't0_attempt_time'),
            ('Host Leader Follower (leader of follower): ', 'host_leader_follower')
        ]

        spacex_inputs = [
            ('SpaceX Target SV ID:', 'target_sv_id'),
            ('Input Target OISL ID (1 or 2):', 'target_oisl_id'),
            ('Leader or Follower? ', 'host_leader_follower'),
            ('t0_attempt_time (YYYY-MM-DD HH:MM:SS): ', 't0_attempt_time')
        ]

        york_inputs = [
            ('York Target SV ID:', 'target_sv_id'),
            ('Input Target OISL ID (1 or 2):', 'target_oisl_id'),
            ('Host: Leader or Follower?', 'host_leader_follower'),
            ('Target: Leader or Follower?', 'target_leader_follower'),
            ('Slew Orientation ("FORWARD" or "BACKWARD"): ', 'slew_orientation_str')
        ]

        ghost_inputs = [
            ('Slew Orientation ("FORWARD" or "BACKWARD"): ', 'slew_orientation_str')
        ]

        def update_inputstab():
            # Clear the current content in the content_frame
            for widget in content_frame.winfo_children():
                widget.destroy()

            selection = selected_option.get()
            self.new_oisl_inputs = default_inputs.copy()  # Start with default inputs

            if selection == 1:
                '''
                Moon
                '''
                self.new_oisl_inputs.extend(moon_inputs)

                # Create a tkinter Entry object for 'moon' without displaying it
                moon_entry = tk.Entry(content_frame)
                moon_entry.insert(0, 'moon')
                self.oisl_entries['target_sv_id'] = moon_entry

                for i, (label_text, key) in enumerate(self.new_oisl_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)
                    if key != 'target_sv_id':
                        entry = tk.Entry(content_frame, width=25, font=input_font)
                        entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                        self.oisl_entries[key] = entry

            elif selection == 2:
                '''
                Ghost
                '''
                self.new_oisl_inputs.extend(ghost_inputs)

                ghost_entry = tk.Entry(content_frame)
                ghost_entry.insert(0, '')
                self.oisl_entries['target_sv_id'] = ghost_entry

                butt_attempt = tk.Button(content_frame, command=self.create_attempt_type_widgets, text='Attempt Type',
                                         font=input_font)
                butt_attempt.grid(row=len(self.new_oisl_inputs) + 2, columnspan=2, padx=5, pady=5)

                for i, (label_text, key) in enumerate(self.new_oisl_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)
                    if key != 'target_sv_id':
                        entry = tk.Entry(content_frame, width=25, font=input_font)
                        entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                        self.oisl_entries[key] = entry

            elif selection == 3:
                '''
                SpaceX
                '''
                self.new_oisl_inputs.extend(spacex_inputs)

                for i, (label_text, key) in enumerate(self.new_oisl_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)
                    entry = tk.Entry(content_frame, width=25, font=input_font)
                    entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                    self.oisl_entries[key] = entry

            elif selection == 4:
                '''
                York
                '''
                self.new_oisl_inputs.extend(york_inputs)

                butt_attempt = tk.Button(content_frame, command=self.create_attempt_type_widgets, text='Attempt Type',
                                         font=input_font)
                butt_attempt.grid(row=len(self.new_oisl_inputs) + 2, columnspan=2, padx=5, pady=5)

                for i, (label_text, key) in enumerate(self.new_oisl_inputs):
                    label = tk.Label(content_frame, text=label_text, font=input_font)
                    label.grid(row=i + 1, column=0, sticky=tk.W, padx=5, pady=5)
                    entry = tk.Entry(content_frame, width=25, font=input_font)
                    entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky=tk.E)

                    self.oisl_entries[key] = entry

        # Define the style for the radiobuttons
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=("Helvetica", 15, "bold"))

        # Add label above radiobuttons
        label_select_target = tk.Label(tab, text="Select Target", font=("Helvetica", 15, "bold"))
        label_select_target.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # Init radiobuttons
        radiobutton1 = ttk.Radiobutton(tab, text="Moon", variable=selected_option, value=1,
                                       command=update_inputstab, style="Custom.TRadiobutton")
        radiobutton2 = ttk.Radiobutton(tab, text="Ghost", variable=selected_option, value=2,
                                       command=update_inputstab, style="Custom.TRadiobutton")
        radiobutton3 = ttk.Radiobutton(tab, text="SpaceX", variable=selected_option, value=3,
                                       command=update_inputstab, style="Custom.TRadiobutton")
        radiobutton4 = ttk.Radiobutton(tab, text="York", variable=selected_option, value=4,
                                       command=update_inputstab, style="Custom.TRadiobutton")

        # Pack radiobuttons below the label in a horizontal line
        radiobutton1.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        radiobutton2.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        radiobutton3.grid(row=1, column=2, padx=10, pady=10, sticky="w")
        radiobutton4.grid(row=1, column=3, padx=10, pady=10, sticky="w")

        # Make sure the content frame expands properly
        tab.rowconfigure(2, weight=1)
        tab.columnconfigure(0, weight=1)
        for col in range(4):
            tab.columnconfigure(col, weight=1)

        # Update layout initially based on the default selection
        update_inputstab()

        append_butt = tk.Button(tab, text="Append", command=self.append_to_scratch)
        append_butt.grid(row=len(self.new_oisl_inputs) + 3, columnspan=2, pady=10)

    def create_attempt_type_widgets(self):
        """
        Attempt type widget
        """
        # Create a new top-level window
        self.input_window = tk.Toplevel(self)
        self.input_window.title("Attempt Type - DO NOT CLOSE WINDOW!")

        self.attempt_type = tk.StringVar(value="1")
        self.attempt_length = tk.StringVar(value="1")
        self.during_contacts = tk.StringVar(value="1")

        # Attempt type selection
        attempt_type_label = ttk.Label(self.input_window, text="Select Attempt Type:")
        attempt_type_label.grid(row=0, column=0, columnspan=2, pady=10)

        t0_radio = ttk.Radiobutton(self.input_window, text='t0_time_specified', variable=self.attempt_type, value='1',
                                   command=self.update_attempt_type_inputs)
        t0_radio.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        # Dynamic input fields
        self.input_frame = ttk.Frame(self.input_window)
        self.input_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='nsew')

        self.update_attempt_type_inputs()

        # Submit button
        submit_button = ttk.Button(self.input_window, text="Submit", command=self.submitattempt)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)

    def update_attempt_type_inputs(self):
        """
        makes the attempt type window update depending on the radiobutton selection
        """
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if self.attempt_type.get() == '1':
            t0_label = ttk.Label(self.input_frame, text="t0_attempt_time (YYYY-MM-DD HH:MM:SS):")
            t0_label.grid(row=0, column=0, padx=5, pady=5)

            self.t0_attempt_time = ttk.Entry(self.input_frame)
            self.t0_attempt_time.grid(row=0, column=1, padx=5, pady=5)

        elif self.attempt_type.get() == '2':
            '''
            backend still in dev 8/20 
            '''
            length_label = ttk.Label(self.input_frame, text="How would you like to do attempts:")
            length_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

            hours_radio = ttk.Radiobutton(self.input_frame, text='Number of hours', variable=self.attempt_length,
                                          value='1')
            hours_radio.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            contacts_radio = ttk.Radiobutton(self.input_frame, text='Number of contacts', variable=self.attempt_length,
                                             value='2')
            contacts_radio.grid(row=1, column=1, padx=5, pady=5, sticky='w')

            attempts_radio = ttk.Radiobutton(self.input_frame, text='Number of attempts', variable=self.attempt_length,
                                             value='3')
            attempts_radio.grid(row=1, column=2, padx=5, pady=5, sticky='w')

            amount_label = ttk.Label(self.input_frame, text="Amount:")
            amount_label.grid(row=2, column=0, padx=5, pady=5)

            self.attempt_length_amount = ttk.Entry(self.input_frame)
            self.attempt_length_amount.grid(row=2, column=1, padx=5, pady=5)

            contacts_label = ttk.Label(self.input_frame, text="Select Contact Time:")
            contacts_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

            only_radio = ttk.Radiobutton(self.input_frame, text='Only during contacts', variable=self.during_contacts,
                                         value='1')
            only_radio.grid(row=4, column=0, padx=5, pady=5, sticky='w')

            anytime_radio = ttk.Radiobutton(self.input_frame, text='Anytime', variable=self.during_contacts, value='2')
            anytime_radio.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    def submitattempt(self):
        """
        should append the entry for the attempt type to the oisl_entries dict
        multi attempt backend is still in development (8/20)
        """
        attempt_type_input = self.attempt_type.get()

        if attempt_type_input == '1':
            '''
            Takes the attempt type and the time and adds it to the oisl_entries dict which becomes the oisl_prompt_dict
            '''

            # Make attempt type into a tkinter entry object because of how the append helper works
            attempt_type_entry_object = tk.Entry(self.input_window)
            attempt_type_entry_object.insert(0, 't0_time_specified')

            # self.oisl_entries['attempt_type_chosen'] = attempt_type_entry_object # <= I dont think this is needed for
            #                                                                                                 oisl main
            self.oisl_entries['attempt_type'] = attempt_type_entry_object
            self.oisl_entries['t0_attempt_time'] = self.t0_attempt_time

        elif attempt_type_input == '2':
            '''
            Still in dev (Stew, as of 8/20) 
            '''
            attempt_type_chosen = 'multi_attempt'

            attempt_length = self.attempt_length.get()
            attempt_length_amount = self.attempt_length_amount.get()

            if attempt_length == '1':
                attempt_length_unit = 'hours'
            elif attempt_length == '2':
                attempt_length_unit = 'contacts'
            elif attempt_length == '3':
                attempt_length_unit = 'attempts'

            during_contacts = self.during_contacts.get()
            if during_contacts == '1':
                during_contacts = True
            elif during_contacts == '2':
                during_contacts = False



    # =================================================================================================================
    # Activity Append to Scratch Fn

    def append_to_scratch(self):
        """
        will .get() from each textbox within respective prowling tabs
        will append the inputs to {activity}_entries list
        """

        current_tab = self.children_notebook.index(self.children_notebook.select())

        if current_tab == 5:
            self.append_spt_helper()
        else:
            if current_tab == 0:
                acti_name = 'ka'
                acti_entry = self.ka_entries

            elif current_tab == 1:
                acti_name = 'l16'
                acti_entry = self.link16_entries

            elif current_tab == 2:
                acti_name = 'testburn'
                acti_entry = self.proptest_entries

            elif current_tab == 3:
                acti_name = 'burn'
                acti_entry = self.propfire_entries

            elif current_tab == 4:
                acti_name = 'oisl'
                self.oisl_entries['host_sv_id'] = self.sv_entry
                acti_entry = self.oisl_entries
            self.append_helper(acti_name, acti_entry)
        self.ctab_activity_scratch()

    def append_spt_helper(self):
        for contact in self.contacts:
            activities = pst.inputs2eris(contact)
            for activity in activities:
                self.prime.add_activity(name=activity['name'], args=activity['args'])

    def append_helper(self, acti_name, acti_entry):

        # Take entries from frame
        inputty = {}
        for key, entry in acti_entry.items():
            if entry.winfo_exists():
                inputty[key] = entry.get()
            else:
                print(f"Widget {key} no longer exists")

        # Add sv id from first page
        inputty['sv'] = self.sv

        # Filter/massage inputs thru prowling
        filtered_args = prowlers[acti_name].inputs2eris(inputty)

        # Create a list of GUI objects that are in the prowler format
        # self.activities.append(poo.Activity(name=acti_name, args=filtered_args))

        # Creates prowler objects
        self.prime.add_activity(poo.Activity(name=acti_name, args=filtered_args))



    # =================================================================================================================
    # Child Scratch Frame/Tab

    def ctab_activity_scratch(self):
        """
        Will display all entries once they have been appended
        Checkboxes
        Remove, Check, and Save buttons
        """
        # Check if it already exists and delete itself
        tabs = self.children_notebook.tabs()
        if len(tabs) == 7:
            self.children_notebook.forget(tabs[-1])

        # Re-Init the tab
        tab = ttk.Frame(self.children_notebook)
        self.children_notebook.add(tab, text="Activities Scratch Tab")


        # Init checkboxes
        self.cbox_list = []
        self.boolvar_list = []

        for activity in self.prime.activities:
            boolvar = tk.BooleanVar(value=True)
            act_str = f"[{activity.start} to {activity.end}] {activity.name}"
            box = tk.Checkbutton(tab, text=act_str, variable=boolvar, onvalue=True,
                                  offvalue=False, highlightthickness=0, bd=0, bg=white, fg=blue,
                                  font=font.Font(family="Helvetica", size=15, weight="bold"))
            self.cbox_list.append(box)
            self.boolvar_list.append(boolvar)
            box.pack(side=tk.TOP, fill=tk.X)

        #make remove button (removes all True lines)
        self.rm = tk.Button(tab, text="Remove", command=self.butt_rm_acti, bg=black, fg=white,
                            font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.rm.pack(side=tk.BOTTOM)

        #make check button (runs self.prime.sort_n_check)
        self.run = tk.Button(tab, text="Run All", command=self.butt_run_acti, bg=black, fg=white,
                             font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.run.pack(side=tk.BOTTOM)

        #make save button (saves all inputs, ends loops, passes to backend)
        self.check = tk.Button(tab, text="Check", command=self.butt_check_acti, bg=black, fg=white,
                               font=font.Font(family="Helvetica", size=15, weight="bold"))
        self.check.pack(side=tk.BOTTOM)


    # =================================================================================================================
    # Child Scratch Frame Buttons

    def butt_rm_acti(self):
        idx = 0
        while idx < len(self.boolvar_list):
            if self.boolvar_list[idx].get():
                self.prime.activities.pop(idx)
                self.boolvar_list.remove(self.boolvar_list[idx])
            else:
                idx += 1

        self.ctab_activity_scratch()

    def butt_run_acti(self):
        self.prime.sort_n_check(hard=True)
        eg.generate_n_write(prowling=self.prime)
        print(self.prime)

    def butt_check_acti(self):
        """
        Will run constraint checks on ALL inputs
        currently nothing
        """
        operator_insults = {"you absolute buffoon.": 0.3,
                            "you child.": 0.3,
                            "you fool.": 0.3,
                            "what were you thinking?": 0.025,
                            "Kevin Hand!": 0.015,
                            "fat fingers.": 0.06}

        code = self.prime.sort_n_check()
        if code:
            op_insult = choices(list(operator_insults.keys()),
                                weights=operator_insults.values(),
                                k=1)[0]
            print(f"Activities are overlapping, {op_insult}")


# =================================================================================================================
# Utility Fn's
# Table of Contents:
#   - show activity inputs on scratch
#   - display contacts


def show_acti_vals(activity):
    """
    Will take inputs for each activity and make it readable for the operator
    if statements for each activity, it will show only necessary <= idea
    """
    print(f"I will show you the inputs for {activity}")

def display_cont(contact):
    return f'{contact["resource"]} at {contact["start"]}'

# =================================================================================================================
# Launch Main Fn

def build_ui():
    print("X========PP========X\n\n"
          "Starting UI build...\n\n"
          "X========PP========X\n")
    ti.sleep(1)

    # Set root
    root = PPGUI()

    # Init GUI
    root.tab1_sv_selection()
    root.tab2_set_hours()
    tk.mainloop()

    # preparing schedule
    # dic_out = {'activities': [], 'upload': root.contacts.pop(0)}
    #
    # for contact in root.contacts:
    #     if contact['apply']:
    #         contact['action'] = 'hist'
    #         contact['args'] = 0
    #     else:
    #         contact['action'] = 'skip'
    #     contact.pop('active', None)
    #     contact.pop('apply', None)
    #     dic_out['activities'].append(contact)

if __name__ == "__main__":
    build_ui()
