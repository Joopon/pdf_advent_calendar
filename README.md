# pdf_advent_calendar
Terminal Python program that creates an advent calender in the form of two pdf files that can be printed with a printer.
One pdf file is for the front, containing an image and the 24 doors, the other pdf is for the back containing the images that will be behind the doors.
After printing, you can assemble the calendar by cutting out the doors and gluing the front and back image together.

## Setup (Linux)
- Install python
- Setup virtual environment
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

> Note: You need to activate the virtual environment with `$ source .venv/bin/activate` before running the python program. It is activated if there is a '(.venv)' at the beginning of your terminal prompt.

## Usage
- Put the 24 door images into `my-project/images`. You have to specify which image belongs to which door number by naming the file after the number (e.g. `1.png`, `12.jpg`).
- Put the front image into `my-project/images` and name it front_image (e.g. `front_image.png`).
- Put TrueType font file into `fonts` (e.g. `arial.ttf`)
- Adjust settings in `my-project/ProjectSettings.py`.
- Run Python program: `$ python main.py`
- Output pdf files will be stored in `my-project/output`

## Multiple Projects
You can create multiple projects.
The variable `PROJECT_NAME` in `main.py` tracks the current project.
You can create a new project called *new-project* by doing the following:
- Set `PROJECT_NAME` in `main.py` to *new-project*.
- Make a copy of directory `my-project` called *new-project*: `$ cp -r my-project new-project`

You can now make changes to *new-project* without affecting my-project.
If you want to use my-project again, change the variable `PROJECT_NAME` back to my-project