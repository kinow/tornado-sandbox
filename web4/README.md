An example with GraphQL and WebSockets for subscriptions

## Notes

Had to patch `graphene-tornado` to workaround an issue with
`allow_subscriptions` missing parameter. See PR for an example
on how to fix it locally: https://github.com/graphql-python/graphene-tornado/pull/28

Still have the following exception:

```bash
ERROR:tornado.application:Error: 'AnonymousObservable' object has no attribute 'errors' Traceback (most recent call last):
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/graphene_tornado/tornado_graphql_handler.py", line 109, in post
    yield self.run('post')
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/tornado/gen.py", line 735, in run
    value = future.result()
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/tornado/gen.py", line 742, in run
    yielded = self.gen.throw(*exc_info)  # type: ignore
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/graphene_tornado/tornado_graphql_handler.py", line 131, in run
    result, status_code = yield self.get_response(data, method, show_graphiql)
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/tornado/gen.py", line 735, in run
    value = future.result()
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/tornado/gen.py", line 748, in run
    yielded = self.gen.send(value)
  File "/home/kinow/Development/python/workspace/tornado-sandbox/venv/lib/python3.7/site-packages/graphene_tornado/tornado_graphql_handler.py", line 219, in get_response
    if execution_result.errors:
AttributeError: 'AnonymousObservable' object has no attribute 'errors'
```

Described in https://github.com/graphql-python/graphene-tornado/issues/27