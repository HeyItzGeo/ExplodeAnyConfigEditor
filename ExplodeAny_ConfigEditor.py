import yaml
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
from tkinter import font



def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return {'Groups': {}, 'VanillaEntity': {}}

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml;*.yaml")])
    if file_path:
        return file_path
    return None

def save_config(file_path, config):
    with open(file_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def add_new_group(entity_group, block_group, config, block_particles_var, entity_particles_var):
    if entity_group not in config['Groups']:
        config['Groups'][f"{entity_group}_Entity"] = []
    if block_group not in config['Groups']:
        config['Groups'][f"{block_group}_Block"] = []

    if f"{entity_group}_Entity" not in config['VanillaEntity']:
        materials = {
            f"{block_group}_Block": {
                'Damage': 50.0,  # Set the default damage value
                'DropChance': 0.0,
                'DistanceAttenuationFactor': 0.0,
                'UnderwaterDamageFactor': 0.5,
                'FancyUnderwaterDetection': False,
                **({'Particles': {  # Particles of the broken block
                    'DeltaX': 5.0,
                    'DeltaY': 5.0,
                    'DeltaZ': 5.0,
                    'Amount': 2000,
                    'Speed': 1.0,
                    'Force': True,
                    'Name': 'BLOCK_CRACK',  # Updated particle name
                    'Material': 'OBSIDIAN'
                }} if block_particles_var.get() else {}),
                **({'Sound': {  # Updated sound for the block
                    'Name': 'ENTITY_OCELOT_HURT',
                    'Volume': 1.0,
                    'Pitch': 1.0
                }} if block_particles_var.get() else {})
            }
        }

        properties = {
            'ExplosionRadius': 0.0,
            'ExplosionFactor': 1.0,
            'ReplaceOriginalExplosion': False,
            'ExplosionDamageBlocksUnderwater': False,
            'UnderwaterExplosionFactor': 0.5,
            'ReplaceOriginalExplosionWhenUnderwater': True,
            'ExplosionRemoveWaterloggedStateFromNearbyBlocks': False,
            'ExplosionRemoveWaterloggedStateFromNearbyBlocksOnSurface': True,
            'ExplosionRemoveWaterloggedStateFromNearbyBlocksUnderwater': True,
            'ExplosionRemoveNearbyWaterloggedBlocks': False,
            'ExplosionRemoveNearbyWaterloggedBlocksOnSurface': True,
            'ExplosionRemoveNearbyWaterloggedBlocksUnderwater': True,
            'ExplosionRemoveNearbyLiquids': False,
            'ExplosionRemoveNearbyLiquidsOnSurface': True,
            'ExplosionRemoveNearbyLiquidsUnderwater': True,
            'PackDroppedItems': False,
            **({'Particles': {  # Updated particles for the entity explosion
                'Name': 'REDSTONE',
                'DeltaX': 2.0,
                'DeltaY': 2.0,
                'DeltaZ': 2.0,
                'Amount': 2000,
                'Speed': 1.0,
                'Force': True,
                'Red': 255,
                'Green': 0,
                'Blue': 255,
                'Size': 2.0
            }} if entity_particles_var.get() else {}),
            **({'Sound': {  # Updated sound for entity explosion
                'Name': 'ENTITY_OCELOT_HURT',
                'Volume': 1.0,
                'Pitch': 1.0
            }} if entity_particles_var.get() else {})
        }

        config['VanillaEntity'][f"{entity_group}_Entity"] = {
            'Materials': materials,
            'Properties': properties
        }




def display_groups(config, output_text):
    output_text.delete(1.0, tk.END)
    for group_name, items in config['Groups'].items():
        output_text.insert(tk.END, f"{group_name}:\n")
        for item in items:
            output_text.insert(tk.END, f"  - {item}\n")
    output_text.insert(tk.END, "\nVanillaEntity:\n")
    for entity, data in config['VanillaEntity'].items():
        output_text.insert(tk.END, f"  {entity}:\n")
        output_text.insert(tk.END, "    Materials:\n")
        for material, mat_data in data['Materials'].items():
            output_text.insert(tk.END, f"      {material}:\n")
            for key, value in mat_data.items():
                output_text.insert(tk.END, f"        {key}: {value}\n")
        output_text.insert(tk.END, "    Properties:\n")
        for key, value in data['Properties'].items():
            output_text.insert(tk.END, f"      {key}: {value}\n")



def handle_add_group(entity_entry, block_entry, config, output_text, group_combobox,block_particles_var, entity_particles_var):
    entity_group = entity_entry.get().strip()
    block_group = block_entry.get().strip()
    
    if not entity_group or not block_group:
        messagebox.showerror("Input Error", "Both Entity Group and Block Group must be filled out.")
        return
        
    max_name_length = 19  # You can adjust this limit as needed

    if len(entity_group) > max_name_length:
        messagebox.showerror("Input Error", f"Entity Group name is too long! Limit is {max_name_length} characters (excluding _Entity).")
        return

    if len(block_group) > max_name_length:
        messagebox.showerror("Input Error", f"Block Group name is too long! Limit is {max_name_length} characters (excluding _Block).")
        return
    
    add_new_group(entity_group, block_group, config,block_particles_var, entity_particles_var)
    display_groups(config, output_text)
    
    group_combobox['values'] = list(config['Groups'].keys())
    entity_entry.delete(0, tk.END)
    block_entry.delete(0, tk.END)

def handle_add_item(group_combobox, item_entry, config, output_text, remove_var):
    group_name = group_combobox.get().strip()
    item_name = item_entry.get().strip()
    
    if not group_name or not item_name:
        messagebox.showerror("Input Error", "Both Group Name and Item Name must be filled out.")
        return

    if remove_var.get():
        if group_name in config['Groups'] and item_name in config['Groups'][group_name]:
            config['Groups'][group_name].remove(item_name)
            messagebox.showinfo("Success", f"Item '{item_name}' removed from '{group_name}'.")
        else:
            messagebox.showerror("Item Not Found", f"The item '{item_name}' is not found in the group '{group_name}'.")
    else:
        if group_name in config['Groups']:
            config['Groups'][group_name].append(item_name)
            messagebox.showinfo("Success", f"Item '{item_name}' added to '{group_name}'.")
        else:
            messagebox.showerror("Group Not Found", f"The group '{group_name}' does not exist.")

    display_groups(config, output_text)
    item_entry.delete(0, tk.END)


import tkinter as tk
from tkinter import ttk, messagebox
import yaml
import os


class SoundAndParticlesConfigurator:
    def __init__(self, master, config, config_file='config.yml', default_entity=None):
        self.master = master
        self.config = config
        self.config_file = config_file  # Store the config file path
        self.default_entity = default_entity
        self.master.configure(bg='light blue')

        self.entity_combobox = ttk.Combobox(master)
        self.entity_combobox['values'] = [key for key in config['VanillaEntity'].keys()]
        self.entity_combobox.grid(row=0, column=0, columnspan=3, pady=10)

        self.entity_combobox.bind('<<ComboboxSelected>>', lambda e: self.select_entity())

        self.save_button = tk.Button(master, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.particle_vars_block = {}
        self.particle_vars_explosion = {}
        self.sound_vars_block = {}
        self.sound_vars_explosion = {}
        self.selected_entity = None

        self.particles_block_frame = tk.LabelFrame(master, text="Block-Breaking Particles")
        self.particles_block_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        self.particles_explosion_frame = tk.LabelFrame(master, text="Entity-Explodes Particles")
        self.particles_explosion_frame.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

        self.sound_frame_block = tk.LabelFrame(master, text="Block-Breaking Sound")
        self.sound_frame_block.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        self.sound_frame_explosion = tk.LabelFrame(master, text="Entity-Explodes Sound")
        self.sound_frame_explosion.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

        if self.default_entity:
            self.entity_combobox.set(self.default_entity)
            self.select_entity()  # Automatically display properties for the selected entity

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def select_entity(self):
        self.selected_entity = self.entity_combobox.get().strip()
        if self.selected_entity:
            self.display_entity_properties(self.selected_entity)

    def display_entity_properties(self, entity_name):
        self.clear_properties()

        entity_data = self.config['VanillaEntity'].get(entity_name, {})
        materials = entity_data.get('Materials', {})
        properties = entity_data.get('Properties', {})

        for block_group_name, block_properties in materials.items():
            self.create_particle_controls(self.particles_block_frame, block_properties.get('Particles', {}), 'block')
            self.create_sound_controls(self.sound_frame_block, block_properties.get('Sound', {}))

        self.create_particle_controls(self.particles_explosion_frame, properties.get('Particles', {}), 'explosion')
        self.create_sound_controls(self.sound_frame_explosion, properties.get('Sound', {}))

    def clear_properties(self):
        for widget in self.particles_block_frame.winfo_children():
            widget.destroy()
        for widget in self.particles_explosion_frame.winfo_children():
            widget.destroy()
        for widget in self.sound_frame_block.winfo_children():
            widget.destroy()
        for widget in self.sound_frame_explosion.winfo_children():
            widget.destroy()

        self.particle_vars_block.clear()
        self.particle_vars_explosion.clear()
        self.sound_vars_block.clear()
        self.sound_vars_explosion.clear()

    def create_particle_controls(self, frame, particles, particle_type):
        if particles:  # Only create controls if particles exist
            current_row = 0
            for prop, default_value in particles.items():
                label = tk.Label(frame, text=prop)
                label.grid(row=current_row, column=0, sticky='w', padx=(0, 5))

                if prop == "Name":
                    particle_names = self.load_particle_names()
                    default_particle_name = default_value if default_value else ""
                    var = tk.StringVar(value=default_particle_name)

                    particle_combobox = ttk.Combobox(frame, textvariable=var, values=particle_names)
                    particle_combobox.grid(row=current_row, column=1, padx=(5, 0))
                    self.store_particle_var(prop, var, particle_type)
                elif isinstance(default_value, bool):
                    var = tk.BooleanVar(value=default_value)
                    toggle = tk.Checkbutton(frame, variable=var)
                    toggle.grid(row=current_row, column=1, sticky='w')
                    self.store_particle_var(prop, var, particle_type)
                elif isinstance(default_value, (int, float)):
                    var = tk.DoubleVar(value=default_value)
                    slider = tk.Scale(frame, from_=0, to=10000 if isinstance(default_value, int) else 10,
                                      resolution=0.1 if isinstance(default_value, float) else 1,
                                      variable=var, orient='horizontal')
                    slider.grid(row=current_row, column=1, padx=(5, 0))
                    self.store_particle_var(prop, var, particle_type)
                else:  # For strings
                    entry_var = tk.StringVar(value=str(default_value))
                    entry = tk.Entry(frame, textvariable=entry_var)
                    entry.grid(row=current_row, column=1, padx=(5, 0))
                    self.store_particle_var(prop, entry_var, particle_type)

                current_row += 1  # Increment row for the next property

    def store_particle_var(self, prop, var, particle_type):
        if particle_type == 'block':
            self.particle_vars_block[prop] = var
        elif particle_type == 'explosion':
            self.particle_vars_explosion[prop] = var

    def create_sound_controls(self, frame, sound):
        if sound:  # Only create controls if sound properties exist
            current_row = 0
            for prop, default_value in sound.items():
                label = tk.Label(frame, text=prop)
                label.grid(row=current_row, column=0, sticky='w', padx=(0, 5))

                if prop == "Name":
                    sound_names = self.load_sound_names()
                    default_sound_name = default_value if default_value else ""
                    var = tk.StringVar(value=default_sound_name)

                    sound_combobox = ttk.Combobox(frame, textvariable=var, values=sound_names)
                    sound_combobox.grid(row=current_row, column=1, padx=(5, 0))
                    if frame == self.sound_frame_block:
                        self.sound_vars_block[prop] = var  # Store the variable for saving
                    else:
                        self.sound_vars_explosion[prop] = var
                elif isinstance(default_value, (int, float)):
                    var = tk.DoubleVar(value=default_value)
                    slider = tk.Scale(frame, from_=0, to=10 if prop in ["Pitch", "Volume"] else 10000,
                                      resolution=0.1, variable=var, orient='horizontal')
                    slider.grid(row=current_row, column=1, padx=(5, 0))
                    if frame == self.sound_frame_block:
                        self.sound_vars_block[prop] = var  # Store the variable for saving
                    else:
                        self.sound_vars_explosion[prop] = var
                elif isinstance(default_value, str):
                    entry_var = tk.StringVar(value=str(default_value))
                    entry = tk.Entry(frame, textvariable=entry_var)
                    entry.grid(row=current_row, column=1, padx=(5, 0))
                    if frame == self.sound_frame_block:
                        self.sound_vars_block[prop] = entry_var  # Store the variable for saving
                    else:
                        self.sound_vars_explosion[prop] = entry_var

                current_row += 1  # Increment row for the next property

    def load_particle_names(self):
        particle_names = ["", "REDSTONE"]  # Include default particle name
        particle_file_path = os.path.join(os.path.dirname(self.config_file), "HARDCODED_PARTICLES_NAMES.txt")

        if os.path.isfile(particle_file_path):
            with open(particle_file_path, 'r') as file:
                particle_names.extend(line.strip() for line in file if line.strip())  # Add each line as a particle name

        return particle_names

    def load_sound_names(self):
        sound_names = ["", "BLOCK_SAND_BREAK"]  # Include default sound name
        sound_file_path = os.path.join(os.path.dirname(self.config_file), "HARDCODED_SOUND_NAMES.txt")

        if os.path.isfile(sound_file_path):
            with open(sound_file_path, 'r') as file:
                sound_names.extend(line.strip() for line in file if line.strip())  # Add each line as a sound name

        return sound_names

    def save_changes(self):
        if not self.selected_entity:
            messagebox.showwarning("Warning", "No entity selected!")
            return

        materials = self.config['VanillaEntity'][self.selected_entity]['Materials']
        properties = self.config['VanillaEntity'][self.selected_entity]['Properties']

        for prop, var in self.particle_vars_block.items():
            block_group_name = list(materials.keys())[0] if materials else 'BlockGroup1'  # Default if none
            if block_group_name not in materials:
                materials[block_group_name] = {}  # Create block group if it doesn't exist
            if 'Particles' not in materials[block_group_name]:
                materials[block_group_name]['Particles'] = {}
            materials[block_group_name]['Particles'][prop] = var.get()

        for prop, var in self.particle_vars_explosion.items():
            if 'Particles' not in properties:
                properties['Particles'] = {}
            properties['Particles'][prop] = var.get()

        for prop, var in self.sound_vars_block.items():
            if 'Sound' not in materials[block_group_name]:
                materials[block_group_name]['Sound'] = {}
            materials[block_group_name]['Sound'][prop] = var.get()

        for prop, var in self.sound_vars_explosion.items():
            if 'Sound' not in properties:
                properties['Sound'] = {}
            properties['Sound'][prop] = var.get()

        with open(self.config_file, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)

        messagebox.showinfo("Success", "Changes saved successfully!")



def update_property(properties, prop, value):
    properties[prop] = value

def create_slider(frame, row, prop, value, properties):
    var = tk.DoubleVar(value=value)
    slider = tk.Scale(frame, from_=0, to=10, resolution=0.1, variable=var, orient='horizontal')
    slider.grid(row=row, column=2, padx=(5, 0))  # Adjusted column index
    
    slider.config(command=lambda val: update_property_from_slider(properties, prop, float(val), entry))

    entry = tk.Entry(frame, width=10)  # Increased width for larger numbers
    entry.insert(0, str(value))
    entry.grid(row=row, column=3, padx=(5, 0))

    entry.bind("<FocusOut>", lambda event: update_property_from_entry(entry, properties, prop, slider))
    
    entry.bind("<Return>", lambda event: update_property_from_entry(entry, properties, prop, slider))

def update_property_from_slider(properties, prop, slider_value, entry):
    update_property(properties, prop, slider_value)
    entry.delete(0, tk.END)
    entry.insert(0, str(slider_value))  # Update the entry with the slider value

def update_property_from_entry(entry, properties, prop, slider):
    try:
        value = float(entry.get())
        update_property(properties, prop, value)
        slider.set(value)  # Update the slider to reflect the new value
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, "Invalid")  # Or set to str(slider.get())

def create_boolean(frame, row, prop, value, properties):
    var = tk.BooleanVar(value=value)
    toggle = tk.Checkbutton(frame, variable=var)
    toggle.grid(row=row, column=2, sticky='w')
    toggle.config(command=lambda: update_property(properties, prop, var.get()))

def create_entry(frame, row, prop, value, properties):
    entry_var = tk.StringVar(value=str(value))
    entry = tk.Entry(frame, textvariable=entry_var, width=10)  # Adjust width for visibility
    entry.grid(row=row, column=3, padx=(5, 0))
    entry.bind("<FocusOut>", lambda event: update_property(properties, prop, entry_var.get()))

def display_entity_properties_window(entity_group, config, file_path):

    properties_window = tk.Toplevel()
    properties_window.title(f"Properties of {entity_group}")
    
    properties_window.configure(bg='lightblue')

    materials = config['VanillaEntity'][entity_group]['Materials']
    properties = config['VanillaEntity'][entity_group]['Properties']
    
    main_frame = tk.Frame(properties_window)
    main_frame.pack(padx=10, pady=10)

    materials_frame = tk.Frame(main_frame)
    materials_frame.grid(row=0, column=0, padx=(0, 10))

    properties_frame = tk.Frame(main_frame)
    properties_frame.grid(row=0, column=1)

    current_row = 0

    first_material_name, first_material_properties = next(iter(materials.items()))

    first_material_label = tk.Label(materials_frame, text=f"{first_material_name}:", font=('Arial', 14, 'bold'))
    first_material_label.grid(row=current_row, column=0, sticky='w', pady=(5, 0))
    
    

    current_row += 1  # Move to the next row for properties

    for prop, value in first_material_properties.items():
        if prop in ['Particles', 'Sound']:
            continue

        prop_label = tk.Label(materials_frame, text=prop)
        prop_label.grid(row=current_row, column=1, sticky='w')

        if isinstance(value, bool):
            create_boolean(materials_frame, current_row, prop, value, first_material_properties)

        elif isinstance(value, (int, float)):
            create_slider(materials_frame, current_row, prop, value, first_material_properties)

        else:
            create_entry(materials_frame, current_row, prop, value, first_material_properties)

        current_row += 1

    for material_name, material_properties in materials.items():
        if material_name == first_material_name:
            continue  # Skip the first material since it's already displayed

        label = tk.Label(materials_frame, text=material_name)
        label.grid(row=current_row, column=0, sticky='w', padx=(0, 5))
        
        for prop, value in material_properties.items():
            if prop in ['Particles', 'Sound']:
                continue

            prop_label = tk.Label(materials_frame, text=prop)
            prop_label.grid(row=current_row, column=1, sticky='w')

            if isinstance(value, bool):
                create_boolean(materials_frame, current_row, prop, value, material_properties)

            elif isinstance(value, (int, float)):
                create_slider(materials_frame, current_row, prop, value, material_properties)

            else:
                create_entry(materials_frame, current_row, prop, value, material_properties)

            current_row += 1
        
        current_row += 1  # Add space between materials

    properties_label = tk.Label(properties_frame, text="Properties: - For Entity Explosion", font=('Arial', 12, 'bold'))
    properties_label.grid(row=current_row, column=0, sticky='w', pady=(5, 0))
    current_row += 1

    for prop, value in properties.items():
        label = tk.Label(properties_frame, text=prop)
        label.grid(row=current_row, column=0, sticky='w', padx=(0, 5))

        if isinstance(value, bool):
            create_boolean(properties_frame, current_row, prop, value, properties)

        elif isinstance(value, (int, float)):
            create_slider(properties_frame, current_row, prop, value, properties)

        else:
            create_entry(properties_frame, current_row, prop, value, properties)

        current_row += 1




    save_button = tk.Button(properties_window, text="Save Changes", command=lambda: save_and_reload_properties(properties_window, config, file_path))
    save_button.pack(pady=(10))

    help_button = tk.Button(properties_window, text="Help", bg="#2196F3", fg="white",
                            command=lambda: show_help_window())
    help_button.pack(pady=10)

    properties_window.update_idletasks()
    properties_window.minsize(properties_window.winfo_width(), properties_window.winfo_height())


def show_help_window():
    help_window = tk.Toplevel()
    help_window.title("ExplodeAny Plugin Configuration Guide")
    help_window.configure(bg="#d3d3d3")

    notebook = ttk.Notebook(help_window)
    notebook.pack(expand=True, fill='both', padx=10, pady=10)

    tabs_info = [
        ("Explosion Properties", explosion_properties_tab),
        ("Damage Properties", damage_properties_tab),
        ("Miscellaneous Properties", miscellaneous_properties_tab)
    ]

    for tab_name, tab_content in tabs_info:
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        tab_content(tab)

    close_button = tk.Button(help_window, text="Close", command=help_window.destroy)
    close_button.pack(pady=10)

def explosion_properties_tab(parent):
    help_text = """\
Explosion Properties

- ExplosionRadius (default: 0.0)
    - Purpose: Overrides the original explosion radius.
    - Range: 0.0 (no change) to any positive number.
    - Usage: Increase to magnify explosion size.

- ExplosionFactor (default: 1.0)
    - Purpose: Multiplies the explosion radius.
    - Range: 0.0 (nullifies explosion) and above.
    - Usage: Set above 1.0 to increase explosion size.

- ReplaceOriginalExplosion (default: false)
    - Purpose: Replaces the original explosion with custom values.
    - Usage: Set to true if you want to fully replace the original explosion's properties.

- UnderwaterExplosionFactor (default: 0.5)
    - Purpose: Modifies the explosion radius underwater.
    - Range: 0.0 (disable) to any positive number.
    - Usage: Set higher than 1.0 to magnify underwater explosions.

- ExplosionDamageBlocksUnderwater (default: false)
    - Purpose: Allows the explosion to damage unmanaged Vanilla blocks underwater.
    - Usage: Set to true for underwater explosions to break blocks like stone or dirt.
"""

    text_widget = tk.Text(parent, wrap='word', bg="#f0f0f0", font=("Helvetica", 10))
    text_widget.insert('1.0', help_text)
    text_widget.config(state='disabled')  # Make it read-only
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)

def damage_properties_tab(parent):
    help_text = """\
Damage Properties

- Damage (default varies)
    - Purpose: Base damage value for blocks.
    - Usage: Higher damage values can affect how blocks are destroyed by explosions.

- DropChance (default: 0.0)
    - Purpose: The chance that a block will drop items when broken.
    - Usage: Set between 0.0 (no drops) and 100.0 (always drop items).

- DistanceAttenuationFactor (default: 0.0)
    - Purpose: Adjusts damage based on distance from the explosion.
    - Usage: Set between 0.0 (uniform damage) and 1.0 (damage reduces with distance).

- UnderwaterDamageFactor (default: 0.5)
    - Purpose: Adjusts damage when the explosion occurs underwater.
    - Usage: Increase to magnify damage underwater.
"""

    text_widget = tk.Text(parent, wrap='word', bg="#f0f0f0", font=("Helvetica", 10))
    text_widget.insert('1.0', help_text)
    text_widget.config(state='disabled')
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)

def miscellaneous_properties_tab(parent):
    help_text = """\
Miscellaneous Properties

- FancyUnderwaterDetection (default: false)
    - Purpose: Traces water between the explosion center and blocks to simulate realistic underwater effects.
    - Usage: Set to true for more accurate underwater explosion effects.

- PackDroppedItems (default: false)
    - Purpose: Packs dropped items into one entity at the explosion site to reduce lag.
    - Usage: Set to true to optimize item drops during larger explosions.
"""

    text_widget = tk.Text(parent, wrap='word', bg="#f0f0f0", font=("Helvetica", 10))
    text_widget.insert('1.0', help_text)
    text_widget.config(state='disabled')
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)



def save_and_reload_properties(properties_window, config, file_path):
    save_config(file_path, config)  # Save the modified config to the file
    properties_window.destroy()  # Close the properties window

def handle_select_entity_group(entity_combobox, config,config_file):
    selected_entity = entity_combobox.get().strip()
    if not selected_entity or selected_entity not in config['VanillaEntity']:
        messagebox.showwarning("No Entity Group Selected", "Please add a Block & Entity Group first by clicking 'Add Group'.")
        return
    display_entity_properties_window(selected_entity, config,config_file)

def handle_sound_particles_config(entity_combobox, config, root):
    selected_entity = entity_combobox.get()
    
    if not selected_entity or selected_entity not in config['VanillaEntity']:
        messagebox.showwarning("No Entity Group Selected", "Please add a Block & Entity Group first by clicking 'Add Group'.")
        return

    open_sound_particles_configurator(entity_combobox, root, config)



def save_and_reload(config_file, config, output_text, entity_combobox):
    save_config(config_file, config)
    
    new_config = load_config(config_file)
    
    display_groups(new_config, output_text)
    
    entity_combobox['values'] = list(new_config['VanillaEntity'].keys())
    
    if entity_combobox['values']:  # Check if there are any items
        entity_combobox.current(0)  # Set default to the first option



def Justreload(config_file, config, output_text, entity_entry, block_entry, item_entry, group_combobox, entity_combobox):
    try:
        config.clear()  # Clear the current config
        config.update(load_config(config_file))  # Load fresh config from file
        

        entity_entry.delete(0, tk.END)  # Clear the entity group input field
        block_entry.delete(0, tk.END)   # Clear the block group input field
        item_entry.delete(0, tk.END)    # Clear the item input field

        group_combobox['values'] = list(config['Groups'].keys())
        group_combobox.set('')  # Clear any selected value in the combobox

        entity_combobox['values'] = list(config['VanillaEntity'].keys())
        updated_selected_entity = entity_combobox.get()
        entity_combobox.set("")  # Clear any selected entity group #maybe an ERROR heere?

        output_text.delete(1.0, tk.END)  # Clear the output text area
        display_groups(config, output_text)  # Display updated config

        messagebox.showinfo("Reloaded", "The configuration has been reloaded, including any external changes.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to reload the configuration: {e}")

def save_and_reload(config_file, config, output_text, entity_combobox):
    save_config(config_file, config)
    
    new_config = load_config(config_file)
    
    display_groups(new_config, output_text)
    
    entity_combobox['values'] = list(new_config['VanillaEntity'].keys())
    
    if entity_combobox['values']:  # Check if there are any items
        entity_combobox.current(0)  # Set default to the first option


def open_sound_particles_configurator(entity_combobox,root,config):
    selected_entity = entity_combobox.get()
    sound_particles_window = tk.Toplevel(root)
    configurator = SoundAndParticlesConfigurator(sound_particles_window, config, default_entity=selected_entity)



    

def User_Selected_Config():
    config_path = open_file_dialog()
    if config_path:
        config = load_config(config_path)
        config_file = config_path  # Use the selected config path
    else:
        config = {'Groups': {}, 'VanillaEntity': {}}  # Default config if no file is selected
        config_file = 'config.yml'  # Default config file name
    return config, config_file, config_path

def reload_configuration():
    global config, config_file, config_path,non_clickable_menu_item  
    config, config_file, config_path = User_Selected_Config()
    output_text.delete(1.0, tk.END)  # Clear existing text
    display_groups(config, output_text)  # Refresh displayed groups
    group_combobox['values'] = list(config['Groups'].keys())  # Update combobox
    entity_combobox['values'] = [key for key in config['VanillaEntity'].keys()]  # Update entity combobox
    if entity_combobox['values']:  # Check if there are any items
        entity_combobox.current(0)  # Set default to the first option
    non_clickable_menu_item.entryconfig(0, label="Current Config: " + config_file.split('/')[-1])  # Update label

    
    



def main_ui():
    global config, config_file, config_path, output_text, group_combobox, entity_combobox,root,non_clickable_menu_item
    
    config, config_file, config_path = User_Selected_Config()
    
    root = tk.Tk()
    root.title("ExplodeAny Config Editor")
    root.configure(bg='lightblue')
    
    menubar = tk.Menu(root)
    
    


    root.config(menu=menubar)
    
    

    root.grid_rowconfigure(7, weight=1)  # Allow the output_text area to expand
    root.grid_columnconfigure(0, weight=1)  # Allow the first column to expand
    root.grid_columnconfigure(1, weight=1)  # Allow the second column to expand

    style = ttk.Style()
    style.theme_use('default')
    style.configure("TCombobox")  # Adjust font and size

    style.configure("TLabel", 
                    background="lightblue",  # Label background color
                    foreground="black",      # Text color
                    font=('Arial', 12))      # Font style and size

    entity_label = ttk.Label(root, text="Entity Group Name:", style="TLabel")
    entity_label.grid(row=0, column=0, padx=5, pady=5)
    entity_entry = tk.Entry(root)
    entity_entry.grid(row=0, column=1, padx=5, pady=5)

    block_label = ttk.Label(root, text="Block Group Name:", style="TLabel")
    block_label.grid(row=1, column=0, padx=5, pady=5)
    block_entry = tk.Entry(root)
    block_entry.grid(row=1, column=1, padx=5, pady=5)



    entity_particles_var = tk.BooleanVar(value=True)
    entity_particles_checkbox = tk.Checkbutton(root, text="Entity Particles", variable=entity_particles_var, bg='lightblue', font=('Arial', 12))
    entity_particles_checkbox.grid(row=2, column=1, padx=1, pady=5, sticky="W")

    block_particles_var = tk.BooleanVar(value=True)
    block_particles_checkbox = tk.Checkbutton(root, text="Breaking Particles", variable=block_particles_var, bg='lightblue', font=('Arial', 12))
    block_particles_checkbox.grid(row=2, column=2, padx=1, pady=5, sticky="W")

    add_button = tk.Button(root, text="Add Group", command=lambda: handle_add_group(entity_entry, block_entry, config, output_text, group_combobox,block_particles_var, entity_particles_var))
    add_button.grid(row=3, column=0, columnspan=3, pady=10)

    group_label = ttk.Label(root, text="Group Name:", style="TLabel")
    group_label.grid(row=4, column=0, padx=5, pady=5)

    group_combobox = ttk.Combobox(root, style="TCombobox")
    group_combobox['values'] = list(config['Groups'].keys())
    group_combobox.grid(row=4, column=1, padx=5, pady=5)

    item_label = ttk.Label(root, text="Item Name:", style="TLabel")
    item_label.grid(row=5, column=0, padx=5, pady=5)
    item_entry = tk.Entry(root)
    item_entry.grid(row=5, column=1, padx=5, pady=5)

    remove_var = tk.BooleanVar()
    remove_checkbox = tk.Checkbutton(root, text="Remove Item", variable=remove_var, bg='lightblue', font=('Arial', 12))
    remove_checkbox.grid(row=6, column=0, columnspan=3, pady=5)

    add_item_button = tk.Button(root, text="Add/Remove Item", command=lambda: handle_add_item(group_combobox, item_entry, config, output_text, remove_var))
    add_item_button.grid(row=7, column=0, columnspan=3, pady=10)

    custom_font = font.Font(family="Futura", size=15)  # You can change the font and size here

    output_text = tk.Text(root, height=15, width=50, font=custom_font)
    output_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    display_groups(config, output_text)

    entity_combobox = ttk.Combobox(root)
    entity_combobox['values'] = [key for key in config['VanillaEntity'].keys()]
    entity_combobox.grid(row=9, column=0, columnspan=3, pady=10)
    if entity_combobox['values']:  # Check if there are any items
        entity_combobox.current(0)  # Set default to the first option
    selected_value = entity_combobox.get()
    print("Selected Entity Group:", selected_value)

    select_entity_button = tk.Button(root, text="Modify Entity Properties", command=lambda: handle_select_entity_group(entity_combobox, config, config_path))
    select_entity_button.grid(row=10, column=0, columnspan=1, pady=10)

    sound_particles_button = tk.Button(root, text="Sound And Particles", command=lambda: handle_sound_particles_config(entity_combobox, config, root))
    sound_particles_button.grid(row=10, column=1, columnspan=2, pady=10)

    reload_button = tk.Button(root, text="Reload Config", command=lambda: Justreload(config_file, config, output_text, entity_entry, block_entry, item_entry, group_combobox, entity_combobox))
    reload_button.grid(row=11, column=0, columnspan=1, pady=10)

    save_button = tk.Button(root, text="Save Changes", command=lambda: save_and_reload(config_file, config, output_text, entity_combobox))
    save_button.grid(row=11, column=1, columnspan=2, pady=10)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Load New Config", command=reload_configuration)
    menubar.add_cascade(label="File", menu=file_menu)
    non_clickable_menu = tk.Menu(menubar, tearoff=0)
    non_clickable_menu_item = tk.Menu(non_clickable_menu, tearoff=0)  # Create a menu item to hold the label
    non_clickable_menu_item.add_command(label="Loaded: " + config_file.split('/')[-1], state="disabled")
    menubar.add_cascade(label="Loaded Config:", menu=non_clickable_menu_item)



    root.mainloop()



if __name__ == "__main__":
    main_ui()
    
