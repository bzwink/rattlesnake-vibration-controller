## Steps to create environment

1. Adding environment to registries
    - [x] Create EnvironmentType in environment_utilities.py
    - [x] Add EnvironmentType to UNIMPLEMENTED_ENVIRONMENT in environment_registry.py
    - [x] Create name_environment.py
        - [x] Add EnvironmentCommands
        - [x] Add EnvironmentUICommands
        - [x] Add EnvironmentMetadata
        - [x] Add EnvironmentInstructions
        - [x] Add Environment
        - [x] Add environment_process
    - [x] Create name_ui.py
        - [x] Add EnvironmentUI
    - [x] Add classes to environment_registry.py
    - [x] Add UI to ui_registry.py

2. (Optional) Create definition tab and run tab ui using qtdesigner
    - [x] See src/rattlesnake/user_interface/ui_files for inspiration
    - [x] Add a Start Environment/Stop Environment button in the run tab

3. EnvironmentMetadata class
    # The environment metadata class should contain the values required to fully define and build a metadata object
    - [x] Metadata region
        - [x] __init__
            # Assigns relevant values. Should be capable of creating a valid metadata object from the single call.
            - [x] Required inputs: environment_type, environment_name, channel_list_bools, sample_rate
            - [x] Call super().__init__()
            - [x] Add inputs specific to environment
            - [x] Try to follow
                - [x] All relevant values should be inputs into __init__ instead of setting values = None and assigning later
        - [x] Add properties specific to environment
    - [ ] Validation region
        - [ ] validate
            # Is given a hardware metadata object. Should raise an error if metadata object will cause an error when initialize_environment is called
            - [x] Call super().validate()
            - [ ] Raise RattlesnakeError if you want UI to display text
            - [ ] Raise Exception if you want UI to display traceback
    - [ ] Loading region
        - [ ] save_metadata_to_netcdf
            # Is given a netcdf group handle. Should assign values directly to group handle (ie: netcdf_group_handle.sample_rate = self.sample_rate)
        - [ ] load_metadata_from_netcdf
            # Counterpart to save_metadata_to_netcdf. Should assign values from the netcdf group handle.
            # This is a classmethod that returns a cls(). This is given environment_name, etc. since they are required inputs into cls()
        - [ ] create_blank_worksheet_template
            # This is given an openpyxl worksheet. Should build out the excel worksheet template using worksheet.cell(row, col, text)
            # Hints to the inputs are usually given in col 3
        - [ ] save_metadata_to_worksheet
            # Save the values from the metadata object to the blank worksheet
            - [ ] Call super().save_metadata_to_worksheet() which builds the blank worksheet
        - [ ] load_metadata_from_worksheet
            # Counterpart to save_metadata_to_worksheet. Build metadata object from values within a worksheet
            # This is a classmethod that returns a cls(). This is given environment_name, etc. since they are required inputs into cls()

4. (Optional) EnvironmentQueue class
    # It is recommended to create an EnvironmentQueue class that acts as a container for the many queues required by the environment
    - [ ] __init__ suggested queues
        - [ ] environment_command_queue: Queue from which the environment will receive instructions.
        - [ ] gui_update_queue: Queue to which the environment will put GUI updates.
        - [ ] controller_communication_queue: Queue to which the environment will put global contorller instructions.
        - [ ] data_in_queue: Queue from which the environment will receive data from acquisition.
        - [ ] data_out_queue: Queue to which the environment will write data for output.
        - [ ] log_file_queue: Queue to which the environment will write log file messages.

4. Create an __init__ for the Environment Class
    - [x] Environment Region
        - [x] __init__
            - [x] Must call super().__init__()
            - [x] Suggested inputs
                - [x] environment_name: str, queue_name: str, queue_container: ReadQueues, acquisition_active_event: mp.synchronize.Event, 
                output_active_event: mp.synchronize.Event, active_event: mp.synchronize.Event, ready_event: mp.synchronize.Event,
            - [x] Suggested assignments
                - [x] self.queue_container = queue_container
                - [x] self.hardware_metadata = None
                - [x] self.environment_metadata = None
                - [x] self.shutdown_flag = False

5. Create environment_process function
    - [x] Required inputs
        - [x] environment_name: str, queue_name: str, input_queue: VerboseMessageQueue, gui_update_queue: mp.Queue, controller_command_queue: VerboseMessageQueue,
        log_file_queue: mp.Queue, data_in_queue: mp.Queue, data_out_queue: mp.Queue, acquisition_active_event: mp.synchronize.Event, output_active_event: mp.synchronize.Event,
        active_event: mp.synchronize.Event, ready_event: mp.synchronize.Event, shutdown_event: mp.synchronize.Event, sysid_active_event: mp.synchronize.Event,
        sysid_stored_event: mp.synchronize.Event, threaded: bool
        - [x] Create queue container
        - [x] Create Environment object
        - [x] Call environment_object.run(shutdown_event)

6. Create Environment State Sync functions
    # These are functions that are assigning data to the environment
    - [ ] State Sync region
        - [ ] initialize_hardware
            # Assigns a hardware metadata class to the environment. The values you have access to are:
            # hardware_metadata.sample_rate, channel_list, samples_per_read, samples_per_write
            - [ ] (optional) self.hardware_metadata = hardware_metadata
            - [ ] Must call self.set_ready() as Rattlesnake will wait for this to be called before moving on
        - [ ] initialize_enviornment
            # Assigns the EnvironmentMetadata to the environment. Must set up the environment from the values in the Metadata class
            - [ ] Must call self.environment_name = environment_metadata.environment_name
            - [ ] (optional) self.environment_metadata = environment_metadata
            - [ ] Must call self.set_ready()

7. Add a method of starting up the environment
    - [ ] Add self.command_map[GlobalCommands.START_ENVIRONMENT] = self.run_environment to end of Environment.__init__()
    - [ ]
    - [ ] Command region
        - [ ] run_environment(environment_instruction)
            # This function is called when rattlesnake.start_environment() is called. This function will recieve