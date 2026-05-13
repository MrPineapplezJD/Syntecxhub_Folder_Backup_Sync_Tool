# 📖 About The Project

This project is a Python-based backup and synchronization tool designed to automate file backups while keeping folders synchronized.

The application:

* Copies new files
* Updates modified files
* Removes deleted files from the backup folder
* Creates compressed ZIP snapshots
* Rotates older backups automatically
* Logs all operations and errors
* Supports a safe `--dry-run` preview mode

This project was built to practice:

* Python file handling
* Automation scripting
* Command-line interface development
* Error handling
* Logging systems
* ZIP compression
* Modular programming

---

# ✨ Features

✅ Incremental file synchronization
✅ Automatic file updates
✅ Deleted file detection
✅ ZIP backup creation
✅ Backup rotation system
✅ Dry-run preview mode
✅ Logging support
✅ Command-line interface (CLI)
✅ Error handling and recovery
✅ Preserves original file metadata

---

# 🛠️ Built With

* Python 3
* os
* shutil
* argparse
* logging
* pathlib
* zipfile
* datetime

---

# 📂 Project Structure

```bash
Folder_Backup_Sync_Tool/
│
├── backup_sync.py
├── logs/
│   └── backup_sync.log
├── Current_Backup/
├── zips/
└── README.md
```

---

# ⚙️ Installation

## Clone The Repository

```bash
git clone https://github.com/MrPineapplezJD/Syntecxhub_Folder_Backup_Sync_Tool.git
```

## Navigate Into The Project Folder

```bash
cd Folder_Backup_Sync_Tool
```

---

# ▶️ Usage

## Windows

```bash
python backup_sync.py --source "C:\Users\YourName\Documents" --destination "D:\Backups"
```

## Mac/Linux

```bash
python3 backup_sync.py --source "/home/user/Documents" --destination "/mnt/backups"
```

---

# 🧪 Dry Run Mode

Preview all changes without modifying files.

```bash
python backup_sync.py --source "SOURCE_PATH" --destination "DESTINATION_PATH" --dry-run
```

### Example Output

```bash
[DRY RUN] Would copy: example.txt
[DRY RUN] Would update: report.docx
[DRY RUN] Would delete: old_file.png
```

---

# 📦 ZIP Backup System

Compressed ZIP snapshots are automatically created after synchronization.

```bash
zips/
├── backup_2026-05-12_14-30-11.zip
├── backup_2026-05-12_15-00-45.zip
```

---

# 🔄 Backup Rotation

Old backup archives are automatically deleted to save storage space.

Default retention setting:

```python
keep=3
```

This can be changed inside the `rotate_backups()` function.

---

# 📝 Logging

All operations are logged inside:

```bash
logs/backup_sync.log
```

### Example Log Entries

```bash
2026-05-12 14:31:05 - INFO - Copied: C:/Documents/file.txt
2026-05-12 14:31:06 - INFO - Updated: C:/Documents/report.docx
2026-05-12 14:31:07 - INFO - Deleted: D:/Backups/Current_Backup/old.png
```

---

# 🚀 Future Improvements

* GUI version using Tkinter or PyQt
* Multi-threaded file synchronization
* File hashing for advanced comparison
* Cloud backup support
* Restore functionality
* Scheduled automatic backups
* Email notifications

---

# 🧠 What I Learned

Through this project I gained experience with:

* File system operations
* Recursive directory traversal
* Synchronization logic
* ZIP compression handling
* Logging systems
* Exception handling
* Building CLI applications
* Writing modular Python code

---

# 👨‍💻 Author

This project was created by **Emmanuel Joshua Deoduth**

---

# 📜 License

This project is licensed under the MIT License.

Feel free to use, modify, and improve this project.
