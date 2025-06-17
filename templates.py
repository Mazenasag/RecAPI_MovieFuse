import os
from pathlib import Path

ProjectName = "RECAPI_MOVIEFUSE"

list_file=[
     ".github/workflows/.gitkeep",
     f"src/{ProjectName}/components/__init__.py",
     f"src/{ProjectName}/utils/__init__.py",
    f"src/{ProjectName}/config/__init__.py",
    f"src/{ProjectName}/pipeline/__init__.py",
    f"src/{ProjectName}/entity/__init__.py",
    f"src/{ProjectName}/entity/con.py",
    f"src/{ProjectName}/constant/__init__.py",
     "src/dvc.yaml",
    "config/config.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb"

]


for file in list_file:
    filepath=Path(file)
    file_dir,file_name=os.path.split(filepath)
    if file_dir !="":
        os.makedirs(file_dir,exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) ==0):
        with open(filepath ,'w'):
            pass
    
