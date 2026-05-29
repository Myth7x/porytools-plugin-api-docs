## PoryTools Plugin API Documentation

**Read the docs:** https://myth7x.github.io/porytools-plugin-api-docs/

The API reference is generated with [pydoctor](https://pydoctor.readthedocs.io/)
from the typed stub package in [`pt/`](pt/). Those modules carry no runtime
code — they mirror the Lua `pt.*` plugin API so its surface can be documented.

### Build locally

```sh
pip install -r requirements.txt
pydoctor            # config is in pyproject.toml; output lands in site/
```

Then open `site/index.html`.
