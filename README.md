# Create virtual environemnt 
```python3 -m venv venv
```source venv/bin/activate

# Install all libs
pip install -r requirements.txt

# First you need to prepare DB, run command bellow:
python init_db.py

# Start server:
python main.py

# Get hello page
curl localhost:5000/hello
# Create user
curl -d '{"name":"Joe"}' -H "Content-Type: application/json" -X POST http://localhost:5000/user  -i

# If you wanna inser user to DB then you should have this variable in env vars
export IMPORT_TO_DB=True

# Get user ( this endpoint only will work if IMPORT_TO_DB was True when user was creating )
curl localhost:5000/username=Joe



#### Helm part
# cd chart and run commond bellow
helm upgrade -i py-exness py-exness


# Service monitor
in values we have value serviceMonitor
By default it is false, you can put True to enable it

```helm upgrade -i py-exness py-exness --set serviceMonitor=True```
