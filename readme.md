## Example of topic exchange using Celery and Attrs

This is the POC of a blog post in https://rightpython.com.

To run you can either use `celery` or `docker-compose`.

Celery:
```bash
python setup.py develop
celery worker -A billing.app -l INFO -n billing 
celery worker -A logistic.app -l INFO -n logistic 
python order/task.py
```

`docker-compose`:
```bash
docker-compose up --build
```

In the latter case you can check the success using the following command:
```bash
docker-compose logs | grep "Task order.v1.submit"
```
