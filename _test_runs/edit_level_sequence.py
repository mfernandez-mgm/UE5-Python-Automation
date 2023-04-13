import unreal

# Create a new Level Sequence asset
level_sequence_asset_path = '/Game/mgm/Animation/level_sequences/MyLevelSequence'
# level_sequence_factory = unreal.LevelSequenceFactoryNew()
# level_sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name='MyLevelSequence', package_path='/Game/mgm/Animation/level_sequences', asset_class=unreal.LevelSequence, factory=level_sequence_factory)


# Get the skeletal mesh component of the character rig (assuming it's already placed in the level)
editor_actor_subsystem = unreal.EditorActorSubsystem()
level_actors = editor_actor_subsystem.get_all_level_actors()


# Loop through all the actors in the level
for actor in level_actors:
    if actor.get_actor_label() == 'BP_man_business':
        print(actor)
        skeletal_mesh_component = actor.get_component_by_class(unreal.SkeletalMeshComponent) # this is the skeletal mesh component of the character rig
    if actor.get_actor_label() == 'LevelSequence':
        print(actor)
        level_sequence_actor = actor # this is the level sequence actor in the level
        level_sequence = level_sequence_actor.get_sequence() # this is the level sequence asset that's assigned to the level sequence actor in the details panel
        print('Bindings: ')
        print('-' * 50)

        # these are the bindings in the level sequence asset
        # each binding is a track for a specific actor or component
        for binding in level_sequence.get_bindings():
            print(f'{binding.get_display_name()}: {binding}') # binding.get_display_name() is the name of the actor/component, i.e. 'Face' which is the name of the skeletal mesh component of the character rig
            
            print('Tracks: ')
            for track in binding.get_tracks(): # these are the tracks for each binding
                print(f'{track.get_display_name()}: {track}')
                print('Sections: ')
                for section in track.get_sections():
                    print(f'{section}')

            if binding.get_display_name() == 'Face':
                print('Found Face binding')
                # get the animation track for the Face binding
                animation_track = binding.get_tracks()[0]
                # add a new section to the animation track
                anim_section = animation_track.add_section()


            print('-' * 50)
# load the facial animation asset
facial_animation_asset = unreal.load_asset('/Game/mgm/Animation/anim_AngryIntoxicatedGuest.anim_AngryIntoxicatedGuest')
print(f'setting animation to {facial_animation_asset}')
# add a new animation asset to the section
animation = anim_section.params = unreal.MovieSceneSkeletalAnimationParams(animation=facial_animation_asset)
# set the range of the section to the length of the animation asset
anim_section.set_range_seconds(0, facial_animation_asset.sequence_length)


# Save the level sequence asset
# unreal.EditorAssetLibrary.save_asset(level_sequence_asset_path)

# print(level_sequence.get_movie_scene())
# for x in sorted(dir(level_sequence)):
#     print(x)

# set_playback_end_seconds
# remove_master_track
# modify
# get_playback_range
# get_playback_end
# get_master_tracks
# get_bindings
# add_master_track