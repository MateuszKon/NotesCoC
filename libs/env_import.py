from dotenv import load_dotenv

from libs.path import get_project_directory

load_dotenv(get_project_directory().joinpath(".env"), verbose=True)
