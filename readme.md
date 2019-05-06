# Example of topic exchange using Celery and Attrs

This is the POC of a blog post on https://rightpython.com.

To run you can either use `celery` or `docker-compose`.

## Using `celery` in the host machine:
```bash
python setup.py develop
celery worker -A billing.app -l INFO -n billing 
celery worker -A logistic.app -l INFO -n logistic 
python order/task.py
```

## Using `docker-compose`:
```bash
docker-compose up --build
```

In this case you can check the success using the following command:
```bash
docker-compose logs | grep "Task order.v1.submit"
```
this should return two rows, one for `logistic` and one for `billing`.
