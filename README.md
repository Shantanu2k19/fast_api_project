# fast_api_project

python3.11 -m venv myenv

uvicorn main:app --reload

uvicorn blog.main:app --reload


# DATABASE 

#install 
pip install sqlalchemy

#version check :
python -c "import sqlalchemy; print(sqlalchemy.__version__)"

#gui -> tableplus 


#create db using init_dp.py, (database.py file should be made first and init in the same folder)




TODO:
- separate out the models for each functionality 