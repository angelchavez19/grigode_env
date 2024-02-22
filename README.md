# grigode_env

grigode_env reads key-value pairs from a `.env` file and parses them into various data types.

- [Getting Started](#getting-started)
- [Types of available data](#types-of-available-data)
- [Accessing variables](#accessing-variables)
- [Configure Your Own Converters](#configure-your-own-converters)

## Getting Started

```bash
python install grigode_env
```

If you need to use system environment variables and want to add more environment variables without having to configure them manually or modify the system variables, you can choose to add grigode_env to your application to load the configuration from one or more .env files:

```python
from grigode_env import Environ

environ = Environ(path='.env')

```

The `environ` attribute of the `Environ` class stores the environment variables from `os.environ`, from `.env` files, and any extra variables you want to add from the code.

The syntax of `.env` files supported by grigode_env is similar to that of Python:

```
# Development settings

ADMIN_EMAIL: str = "admin@example.org"
SECRET_KEY: str = "my-secret-key"
SECRET_CODE: int = 123456
DEBUG: bool = true
SUPER_USER: dict = { "name": "John", "age": 30, "city": "New York"}
RELEASE_DATE: datetime : ["%m/%d/%y %H:%M:%S"] = "15/03/24 13:55:26"
```

## Types of available data

There are several types of data available:

```
# Development settings

ADMIN_EMAIL: str = "admin@example.org"
SECRET_KEY: str = "my-secret-key"
SECRET_CODE: int = 123456
DEBUG: bool = true
SUPER_USER: dict = { "name": "John", "age": 30, "city": "New York"}
RELEASE_DATE: datetime : ["%m/%d/%y %H:%M:%S"] = "03/19/24 13:55:26"
```

## Accessing variables

In this example, we list all environment variables:

```python
from grigode_env import Environ

environ = Environ(path='.env').environ

for key, value in environ.items():
    print(f"{key}: {value}")

```

## Configure Your Own Converters

Here's an example of how to add a new data type:

```python
from collections import namedtuple
from grigode_env import Environ, Parsers


my_parser = Parsers()
User = namedtuple('User', ['name', 'last_name', 'age', 'city'])


def convert_to_user(value: str):
    data = my_parser._convert_to_list(value)

    return User(*data)


my_parser.set_parser('user', (convert_to_user, 1))

env = Environ(path='.env', parsers=my_parser)

```

In the `.env` file, you can define something like this:

```
USER1: user = ["John", "Doe", 30, "New York"]
```

And the result is as follows:

```
USER1: User(name='John', last_name='Doe', age=30, city='New York')
```

## Multiple archivos

Puedes leer más archivos, con la misma clase, siempre y cuando terminen con la extension `.env`:

```python
from grigode_env import Environ

environ = Environ(path=['.env', 'secret.env']).environ

for key, value in environ.items():
    print(f"{key}: {value}")

```

Si desea separar las variables de un archivo de las de otro, puede agregar el atributo `merge_files` en `False`:

```python
from grigode_env import Environ

environ = Environ(path=['.env', 'secret.env'], merge_files=False).environ

for key, value in environ.items():
    print(f"{key}: {value}")

```
