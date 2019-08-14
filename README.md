# mtn
**MTN MoMo API Implementation in Django**

>1. Clone a repo and setup requirements and database

```
$ git clone https://github.com/robin-001/mtn.git
$ cd mtn
$ pip install requirements.txt
$ python manage.py migrate
```

>2. Open another terminal in the same directory and start the background task scheduler

```
$ python manage.py process_tasks --queue mtn-momo
```

>3. Create a MomoRequest Object
```
$ python manage.py shell
>>> from momo.models import MomoRequest
>>> mm = MomoRequest(msisdn="256775065459",amount=500.00,type="COLLECT")
>>> mm.save()
```
