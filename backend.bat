cd "backend"
if not exist env\ (call virtualenv env)
call env\Scripts\activate.bat
call pip install -r requirements.txt
cd "src"
call python main.py