import unreal
# from import_facial_animation import import_facial_animation

'''
1. Duplicate the 'Template' folder in the Content Browser and all its contents
2. Rename the duplicated folder to match the video name
3. Rename the map and the level sequence in the folder to match the video name
4. Open/Load the map
5. Get the level sequence actor in the level, and change the level sequence asset to the one in the newly created folder
6. Check if all the level sequence bindings are correct or valid, and if not, fix them
6. Import the facial animation asset
7. Add the facial animation asset to the level sequence
8. Save the level sequence asset and the map
9. Render the level sequence to a video file
10. Upload the video file to the server
'''

e_asset_lib = unreal.EditorAssetLibrary()


def duplicate_template_folder_and_rename(new_folder_name):
    '''
    - Duplicate the 'Template' folder in the Content Browser and all its contents
    - Rename the duplicated folder to match the video name
    - Get all the assets in the duplicated folder
    - Rename the map and the level sequence in the folder to match the video name
    - Open/Load the newly duplicated map
    '''
    # 1. Duplicate the 'Template' folder in the Content Browser and all its contents
    # 2. Rename the duplicated folder to match the video name
    
    template_folder_path = '/Game/mgm/Animation/level_sequences/Template'
    new_folder_path = f'/Game/mgm/Animation/level_sequences/{new_folder_name}'
    e_asset_lib.duplicate_directory(template_folder_path, new_folder_path)

    # Get all the assets in the duplicated folder
    dir_assets = e_asset_lib.list_assets(new_folder_path, recursive=True)

    # 3. Rename the map and the level sequence in the folder to match the video name
    for asset in dir_assets:
        if asset.endswith('_level'):
            new_map = f'{new_folder_path}/{new_folder_name}_level.{new_folder_name}_level'
            e_asset_lib.rename_asset(asset, new_map) # rename the map

        if asset.endswith('_sequence'):
            new_level_sequence = f'{new_folder_path}/{new_folder_name}_sequence.{new_folder_name}_sequence'
            e_asset_lib.rename_asset(asset, new_level_sequence) # rename the level sequence

    # 4. Open/Load the map
    e_level_lib = unreal.LevelEditorSubsystem()
    e_level_lib.load_level(new_map)

    return new_folder_path, new_map, new_level_sequence


def get_level_actors():
    '''
    - Get the level sequence actor in the level
    - Get the camera actor in the level
    - Get the metahuman character in the level and its skeletal meshes components
    '''
    # 5. Get the level sequence actor in the level, and change the level sequence asset to the one in the newly created folder
    e_actor_subsystem = unreal.EditorActorSubsystem()
    level_actors = e_actor_subsystem.get_all_level_actors()

    # Loop through all the actors in the level
    for actor in level_actors:
        if actor.get_actor_label() == 'BP_TrackingActor':
            bp_tracking_actor = actor
        if actor.get_actor_label() == 'CineCameraActor1':
            print(actor)
            camera_actor = actor # this is the camera actor in the level

        if actor.get_actor_label() == 'BP_man_business':
            print(actor)
            bp_man_business = actor # this is the metahuman character

        if actor.get_actor_label() == 'LevelSequence':
            print(actor)

            # this is the level sequence actor in the level
            level_sequence_actor = actor

    return level_sequence_actor, bp_tracking_actor, camera_actor, bp_man_business


def edit_level_sequence(level_sequence_actor, level_sequence, bp_tracking_actor, camera_actor, metahuman, folder_path, source_file, asset_name):
    '''
    - Change the level sequence asset to the one in the newly created folder
    - Remove all bindings from the level sequence asset, and create new ones
    - Import the facial animation asset
    - Add the facial animation asset to the level sequence
    - Save the level sequence asset and the map
    '''
    # change the level sequence asset to the one in the newly created folder
    level_sequence_actor.set_sequence( unreal.load_asset(level_sequence, unreal.LevelSequence) )

    # this is the level sequence asset that's assigned to the level sequence actor in the details panel
    level_sequence = level_sequence_actor.get_sequence()
    print(level_sequence)

    # Remove all bindings from the level sequence asset
    for track in level_sequence.get_master_tracks():
        print(f'mastertrack name: {track.get_display_name()}, track: {track}')
        level_sequence.remove_master_track(track)

    for binding in level_sequence.get_bindings():
        print(f'binding name: {binding.get_display_name()}')
        for track in binding.get_tracks():
            print(f'track name: {track.get_display_name()}')
            binding.remove_track(track)
        binding.remove()

    binding_name = unreal.Name('MetaHuman')
    print(f'binding_name: {binding_name}')

    # Create new bindings for the metahuman character
    level_sequence.add_possessable(metahuman)

    # Get the skeletal meshes components of the metahuman character
    for component in metahuman.get_components_by_class(unreal.SkeletalMeshComponent):
                if component.get_name() == 'Body':
                    skeletal_mesh_body = component
                if component.get_name() == 'Face':
                    skeletal_mesh_face = component

    # Add the body animation track to the level sequence
    body_track = level_sequence.add_possessable(skeletal_mesh_body).add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = body_track.add_section()
    anim_asset = unreal.load_asset('/Game/Neutral_Idle_Anim_mixamo_com.Neutral_Idle_Anim_mixamo_com')
    anim_section.params = unreal.MovieSceneSkeletalAnimationParams(animation= anim_asset)
    anim_section.set_range_seconds(0, level_sequence.get_playback_end_seconds())

    # Add the facial animation track to the level sequence
    face_track = level_sequence.add_possessable(skeletal_mesh_face).add_track(unreal.MovieSceneSkeletalAnimationTrack)
    anim_section = face_track.add_section()

    # TODO: Import the facial animation asset here
    # source_file = None
    # asset_name = None
    

    # Import the facial animation asset using import_facial_animation function
    import_facial_animation(source_file, folder_path, asset_name)

    # Load the facial animation asset
    anim_asset = unreal.load_asset(f'{folder_path}/{asset_name}.{asset_name}') # anim_asset = unreal.load_asset(f'/Game/mgm/Animation/anim_AngryIntoxicatedGuest.anim_AngryIntoxicatedGuest')
    anim_section.params = unreal.MovieSceneSkeletalAnimationParams(animation= anim_asset)
    anim_section.set_range_seconds(0, anim_asset.sequence_length)

    # Add the camera actor to the level sequence
    camera_binding = level_sequence.add_possessable(camera_actor)
    camera_component = camera_actor.get_cine_camera_component()
    camera_component.focus_settings.focus_method = unreal.CameraFocusMethod.TRACKING
    camera_component.focus_settings.tracking_focus_settings.actor_to_track = bp_tracking_actor

    # camera_binding_id = level_sequence.find_binding_by_name('CineCameraActor1').get_binding_id().copy()
    camera_binding_id = unreal.MovieSceneObjectBindingID()
    camera_binding_id.set_editor_property("Guid", camera_binding.get_id())

    print(f'camera_binding_id: {camera_binding_id}')

    # Add the camera cut track to the level sequence and bind the camera actor to it
    camera_cut_track = level_sequence.add_master_track(unreal.MovieSceneCameraCutTrack)
    camera_cut_section = camera_cut_track.add_section()
    camera_cut_section.set_range_seconds(0, level_sequence.get_playback_end_seconds())
    camera_cut_section.set_camera_binding_id(camera_binding_id)

    # Set the playback end time of the level sequence to the length of the facial animation asset
    level_sequence.set_playback_end_seconds(anim_asset.sequence_length)

    # Save All Assets in the folder
    e_asset_lib.save_directory(folder_path)


def import_facial_animation(source_file, destination_path, asset_name):
    # Load the function from the wrapper
    load_facial_animation = unreal.OmniverseFacialAnimationWrapper.py_load_facial_animation

    # Load skeleton asset
    skeleton_asset_path = '/Game/MetaHumans/Common/Face/Face_Archetype_Skeleton.Face_Archetype_Skeleton'
    skeleton_asset = unreal.load_asset(skeleton_asset_path, unreal.Skeleton)

    imported_asset = load_facial_animation(None, source_file, destination_path, skeleton_asset, asset_name)

    # Print the imported asset path
    print('-' * 50)
    print(f"Facial animation, {asset_name} has been imported! {imported_asset}")
    print('-' * 50)


def __main__():
    # Parse the command line for any additional args
    (cmdTokens, cmdSwitches, cmdParameters) = unreal.SystemLibrary.parse_command_line(unreal.SystemLibrary.get_command_line())
    print("hello world")
    folder_name = None
    try:
        for key, value in cmdParameters.items():
            print(f'key: {key}, value: {value}')
        
        # folder_name = cmdParameters['VideoName']
        folder_name = "MyVideoName"
    except:
        unreal.log_error("Missing '-VideoName=MyVideoName' argument")
        return


    # Duplicate the 'Template' folder
    try:
        (folder_path, map, level_sequence) = duplicate_template_folder_and_rename(folder_name)

    except Exception as err:
        unreal.log_error(f'Error Duplicating folder and renaming assets: {err}')
        return
    
    try:
        # Get the level actors for the sequence
        (level_sequence_actor, bp_tracking_actor, camera_actor, metahuman) = get_level_actors()
    except Exception as err:
        unreal.log_error(f'Error getting actors from map: {err}')
        return
    
    try:
        source_file = "C:/Users/mgm-resorts/Downloads/export/a2f_cache.usd" # Used for testing
        asset_name = "Facial_Anim" # Used for testing
        # Edit the level sequence
        edit_level_sequence(level_sequence_actor, level_sequence, bp_tracking_actor, camera_actor, metahuman, folder_path, source_file, asset_name)
    except Exception as err:
        unreal.log_error(f'Error editing level sequence: {err}')
        return


if __name__ == '__main__':
    __main__()

'''
# Here's how we can scan the command line for any additional args such as the path to a level sequence.
        (cmdTokens, cmdSwitches, cmdParameters) = unreal.SystemLibrary.parse_command_line(unreal.SystemLibrary.get_command_line())
        levelSequencePath = None
        try:
            levelSequencePath = cmdParameters['LevelSequence']
        except:
            unreal.log_error("Missing '-LevelSequence=/Game/Foo/MySequence.MySequence' argument")
            self.on_executor_errored()
            return
'''





# for x in sorted(dir(unreal)):
#     print(x)


'''
# 1. Duplicate the 'Template' folder in the Content Browser and all its contents
# 2. Rename the duplicated folder to match the video name
e_asset_lib = unreal.EditorAssetLibrary()
template_folder_path = '/Game/mgm/Animation/level_sequences/Template'
new_folder_name = 'Test'
new_folder_path = f'/Game/mgm/Animation/level_sequences/{new_folder_name}'
e_asset_lib.duplicate_directory(template_folder_path, new_folder_path)

# Get all the assets in the duplicated folder
dir_assets = e_asset_lib.list_assets(new_folder_path, recursive=True)

# 3. Rename the map and the level sequence in the folder to match the video name
for asset in dir_assets:
    if asset.endswith('_level'):
        new_map = f'{new_folder_path}/{new_folder_name}_level.{new_folder_name}_level'
        e_asset_lib.rename_asset(asset, new_map) # rename the map

    if asset.endswith('_sequence'):
        new_level_sequence = f'{new_folder_path}/{new_folder_name}_sequence.{new_folder_name}_sequence'
        e_asset_lib.rename_asset(asset, new_level_sequence) # rename the level sequence

# 4. Open/Load the map
e_level_lib = unreal.LevelEditorSubsystem()
e_level_lib.load_level(new_map)

# 5. Get the level sequence actor in the level, and change the level sequence asset to the one in the newly created folder
e_actor_subsystem = unreal.EditorActorSubsystem()
level_actors = e_actor_subsystem.get_all_level_actors()

# Loop through all the actors in the level
for actor in level_actors:
    if actor.get_actor_label() == 'BP_TrackingActor':
        bp_tracking_actor = actor
    if actor.get_actor_label() == 'CineCameraActor1':
        print(actor)
        camera_actor = actor # this is the camera actor in the level

    if actor.get_actor_label() == 'BP_man_business':
        print(actor)
        bp_man_business = actor # this is the bp character
        for component in actor.get_components_by_class(unreal.SkeletalMeshComponent):
            if component.get_name() == 'Body':
                skeletal_mesh_body = component
            if component.get_name() == 'Face':
                skeletal_mesh_face = component

    if actor.get_actor_label() == 'LevelSequence':
        print(actor)

        # this is the level sequence actor in the level
        level_sequence_actor = actor

# change the level sequence asset to the one in the newly created folder
level_sequence_actor.set_sequence( unreal.load_asset(new_level_sequence, unreal.LevelSequence) )

# this is the level sequence asset that's assigned to the level sequence actor in the details panel
level_sequence = level_sequence_actor.get_sequence()
print(level_sequence)

# Remove all bindings from the level sequence asset
for track in level_sequence.get_master_tracks():
    print(f'mastertrack name: {track.get_display_name()}, track: {track}')
    level_sequence.remove_master_track(track)

for binding in level_sequence.get_bindings():
    print(f'binding name: {binding.get_display_name()}')
    for track in binding.get_tracks():
        print(f'track name: {track.get_display_name()}')
        binding.remove_track(track)
    binding.remove()

binding_name = unreal.Name('MetaHuman')
print(f'binding_name: {binding_name}')

# print(level_sequence.find_binding_by_name('BP_man_business'))
# level_sequence_actor.add_binding(
#     level_sequence.find_binding_by_name('BP_man_business').get_binding_id(), 
#     bp_man_business
# )

level_sequence.add_possessable(bp_man_business)

body_track = level_sequence.add_possessable(skeletal_mesh_body).add_track(unreal.MovieSceneSkeletalAnimationTrack)
anim_section = body_track.add_section()
anim_asset = unreal.load_asset('/Game/Neutral_Idle_Anim_mixamo_com.Neutral_Idle_Anim_mixamo_com')
anim_section.params = unreal.MovieSceneSkeletalAnimationParams(animation= anim_asset)
anim_section.set_range_seconds(0, level_sequence.get_playback_end_seconds())

face_track = level_sequence.add_possessable(skeletal_mesh_face).add_track(unreal.MovieSceneSkeletalAnimationTrack)
anim_section = face_track.add_section()
anim_asset = unreal.load_asset('/Game/mgm/Animation/anim_AngryIntoxicatedGuest.anim_AngryIntoxicatedGuest')
anim_section.params = unreal.MovieSceneSkeletalAnimationParams(animation= anim_asset)
anim_section.set_range_seconds(0, anim_asset.sequence_length)

level_sequence.add_possessable(camera_actor)
camera_actor.get_cine_camera_component().focus_settings.focus_method = unreal.CameraFocusMethod.TRACKING
camera_actor.get_cine_camera_component().focus_settings.tracking_focus_settings.actor_to_track = bp_tracking_actor

# camera_binding_id = unreal.MovieSceneObjectBindingID()

camera_binding_id = level_sequence.find_binding_by_name('CineCameraActor1').get_binding_id().copy()
# camera_bind_id = level_sequence.find_binding_by_name('CineCameraActor1').get_id()

# camera_binding_id.set_editor_property('guid', camera_bind_id)
print(f'camera_binding_id: {camera_binding_id}')
# camera_binding_id.guid= camera_bind_id, 
# camera_binding_id.space= unreal.MovieSceneObjectBindingSpace.LOCAL
# camera_binding_id.copy(level_sequence.find_binding_by_name('CineCameraActor1').get_binding_id())
# print(f'camera_binding_id: {camera_binding_id}')

camera_cut_track = level_sequence.add_master_track(unreal.MovieSceneCameraCutTrack)
camera_cut_section = camera_cut_track.add_section()
camera_cut_section.set_range_seconds(0, level_sequence.get_playback_end_seconds())
camera_cut_section.set_camera_binding_id(camera_binding_id)
# camera_cut_section.set_editor_property('camera_binding_id', camera_binding_id)
# print(f'camera_cut_section: {camera_cut_section.get_camera_binding_id()}')

level_sequence.set_playback_end_seconds(anim_asset.sequence_length)

e_asset_lib.save_directory(new_folder_path)

'''