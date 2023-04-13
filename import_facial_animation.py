import unreal

def import_facial_animation(source_file, destination_path, asset_name):
    # Load the function from the wrapper
    load_facial_animation = unreal.OmniverseFacialAnimationWrapper.py_load_facial_animation

    # Load skeleton asset
    skeleton_asset_path = '/Game/CitySampleCrowd/Character/Shared/Rig/Face_Archetype_Skeleton.Face_Archetype_Skeleton'
    skeleton_asset = unreal.load_asset(skeleton_asset_path, unreal.Skeleton)

    imported_asset = load_facial_animation(None, source_file, destination_path, skeleton_asset, asset_name)

    # Print the imported asset path
    print('-' * 50)
    print(f"Facial animation, {asset_name} has been imported! {imported_asset}")
    print('-' * 50)






# Specify the source USD file and destination path within the Content Browser
source_file = "C:/Users/mgm-resorts/Downloads/export/a2f_cache.usd"
destination_path = "/Game/Example/Files"

# Import the file
import_facial_animation(source_file, destination_path, "Test_Import")

