import unreal

def import_file(source_file, destination_path):
    # Set the import options
    import_options = unreal.FbxImportUI()
    import_options.set_editor_property("import_mesh", True)
    import_options.set_editor_property("import_textures", False)
    import_options.set_editor_property("import_materials", False)
    import_options.set_editor_property("import_rigid_mesh", False)
    import_options.set_editor_property("import_animations", False)

    # Prevent the import options from detecting the file type
    # import_options.automated_import_should_detect_type = False


    # Create an AssetImportTask
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", source_file)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("options", import_options)
    task.set_editor_property("save", True)
    task.set_editor_property("automated", True)

    # Execute the import task
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    # Return the imported asset
    return task.get_editor_property("imported_object_paths")[0]

# Specify the source USD file and destination path within the Content Browser
source_file = "C:/Users/mgm-resorts/Downloads/backgammon/source/UV.fbx"
destination_path = "/Game/Example/Files"

# Import the file
imported_asset = import_file(source_file, destination_path)

# Print the imported asset path
print('-' * 50)
print(f"File path of the newly imported FBX file from Python Script! {imported_asset}")
print('-' * 50)