import os
import shutil
import argparse
import logging
from datetime import datetime
from pathlib import Path
import zipfile

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/backup_sync.log',
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
    )


# Create ZIP archive of the backup folder
def zip_backup(folder_path, destination, timestamp):

    # Create zips folder
    zip_dir = os.path.join(destination, "zips")
    os.makedirs(zip_dir, exist_ok=True)

    # ZIP file name
    zip_name = os.path.join(
        zip_dir,
        f"backup_{timestamp}.zip"
    )

    # Create ZIP file
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                backup_zip.write(
                    file_path,
                    os.path.relpath(file_path, folder_path)
                )

    print(f"ZIP backup created: {zip_name}")


# Rotate old backups, keeping only the most recent ones
def rotate_backups(destination, keep=3):
    backup_folders = list(
        Path(destination).glob("backup_*")
    )

    zip_dir = Path(destination).joinpath("zips")
    if zip_dir.exists():
        zip_files = list(zip_dir.glob("*.zip"))
    else:
        zip_files = []

    backups = sorted(
        backup_folders + zip_files,
        key=os.path.getmtime
    )

    while len(backups) > keep:
        oldest = backups.pop(0)
        try:
            # If it's a folder
            if oldest.is_dir():
                shutil.rmtree(oldest)
                print(f"Deleted old backup folder: {oldest}")
                logging.info(f"Deleted folder: {oldest}")

            # If it's a zip file
            elif oldest.is_file():
                os.remove(oldest)
                print(f"Deleted old ZIP: {oldest}")
                logging.info(f"Deleted ZIP: {oldest}")

        except Exception as e:
            print(f"Error deleting {oldest}: {e}")
            logging.error(f"Error deleting {oldest}: {e}")


def remove_deleted_files(source, backup_folder, dry_run = False):

    for root, dirs, files in os.walk(backup_folder):
        for file in files:
            backup_file = os.path.join(root, file)

            relative_path = os.path.relpath(
                backup_file,
                backup_folder
            )

            source_file = os.path.join(
                source,
                relative_path
            )

            # File no longer exists in source
            if not os.path.exists(source_file):
                try:
                    if dry_run:
                        print(f"[DRY RUN] Would delete: {backup_file}")

                    else:
                        os.remove(backup_file)
                        print(f"Deleted: {backup_file}")
                        logging.info(f"Deleted: {backup_file}")

                except Exception as e:
                    print(f"Error deleting {backup_file}: {e}")
                    logging.error(
                        f"Error deleting {backup_file}: {e}"
                    )


def main():
    # Create logs directory if it doesn't exist
    parser = argparse.ArgumentParser(description='Folder backup & Sync Tool')

    parser.add_argument("--source", required=True, help="Source folder path")
    parser.add_argument("--destination", required=True, help="Backup destination path")
    parser.add_argument("--dry-run", action='store_true', help="preview changes without copying files")

    args = parser.parse_args()

    if not os.path.exists(args.source):
        print("Source folder does not exist!")
        return

    print("Starting backup...")
    logging.info("Backup started")

    # Create backup folder with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_folder = os.path.join(
        args.destination,
        "Current_Backup"
    )

    if not args.dry_run:
        os.makedirs(backup_folder, exist_ok=True)


    # Walk through source directory and copy files to backup folder
    for root, dirs, files in os.walk(args.source):
        for file in files:
            source_file = os.path.join(root, file)

            relative_path = os.path.relpath(root, args.source)

            destination_dir = os.path.join(
                backup_folder,
                relative_path
            )
            if not args.dry_run:
                os.makedirs(destination_dir, exist_ok=True)

            destination_file = os.path.join(destination_dir, file)

            # DRY RUN: only preview
            if args.dry_run:
                if not os.path.exists(destination_file):
                    print(f"[DRY RUN] Would copy: {source_file}")
                
                else:
                    if (os.path.getsize(source_file) != os.path.getsize(destination_file)
                    or os.path.getmtime(source_file) != os.path.getmtime(destination_file)):
                        print(f"[DRY RUN] Would update: {source_file}")
                
                continue

            # Check if file exists in destination
            if not os.path.exists(destination_file):
                try:
                    shutil.copy2(source_file, destination_file)
                    logging.info(f"Copied: {source_file}")
                    print(f"Copied: {file}")

                except Exception as e:
                    print(f"Error copying {source_file}: {e}")
                    logging.error(f"Error Copying {source_file}: {e}")

            # If file exists : check for updates
            else:
                if (os.path.getsize(source_file) != os.path.getsize(destination_file)
                or os.path.getmtime(source_file) != os.path.getmtime(destination_file)):
                    try:
                        shutil.copy2(source_file, destination_file)
                        logging.info(f"Updated: {source_file}")
                        print(f"Updated: {file}")

                    except Exception as e:
                        print(f"Error copying {source_file}: {e}")
                        logging.error(f"Error Copying {source_file}: {e}")             

    remove_deleted_files(args.source, backup_folder, args.dry_run)
    
    if not args.dry_run:
        zip_backup(backup_folder, args.destination, timestamp)
        rotate_backups(args.destination)
    
    logging.info("Backup completed")
    print("Backup completed successfully!")


if __name__ == "__main__":
    main()