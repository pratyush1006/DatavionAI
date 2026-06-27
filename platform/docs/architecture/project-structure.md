# Project Structure

```
platform/

apps/
config/
docs/
tests/
requirements/
```

Every business module follows:

```
models.py
selectors.py
services.py
serializers.py
views.py
urls.py
admin.py
tests/
```

Views contain HTTP logic only.

Services contain business logic.

Selectors contain read queries.
