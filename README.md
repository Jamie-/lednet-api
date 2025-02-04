# LEDnet #

LEDnet was born after I bought a pile of RGB LED strip on eBay in the spur of the moment and wanted to control it all from one remote but have the strips installed around my house.
I already had lots of hardware kicking about so I built it to use what I had.

How does it work? This software runs on a Raspberry Pi which is connected to your local network.
The Raspberry Pi has a serial connection to an Arduino compatible microcontroller which can control one of more strips over serial (number of strips depends on your Arduino type).
The Uno has 6 PWM lanes so can drive 2 strips, with the help of some MOSFETS.
See setup below on how to wire it up.
The whole system is controlled by a REST API on the Pi.

## Installation / Setup ##
TBC

## Configuration File Options ##

| Field      | Type    | Description                                 |
| ---------- | ------- | ------------------------------------------- |
| systemName | string  | System name.                                |
| strips     | list    | Configuration of strips attached to system. |
| cycles     | list    | System cycle settings (optional).           |
| authKey    | string  | API authentication key (optional).          |

#### Cycles Configuration ####

| Field  | Type   | Description                                   |
| ------ | ------ | --------------------------------------------- |
| name   | string | Cycle name.                                   |
| mode   | string | Cycle mode: `normal`, `static` and `off`.     |
| target | string | Target strip name or `global` for all strips. |
| start  | string | Cycle starting time in format `%H:%M.%S`.     |
| values | object | Static colour values if mode is `static`.     |

##### Cycle Modes #####
* Normal: Network controlled mode. Uses last set value or black if none set yet.
* Static: Static colour as defined in `values` object.
* Off: Static black colour - i.e. all channels at 0.

##### Values #####
Integer values (0 - 255) are required for keys: `red`, `green` and `blue`.

#### Strips Configuration ####

| Field  | Type    | Description                           |
| ------ | ------- | ------------------------------------- |
| id     | string  | Strip identifier used for API.        |
| name   | string  | Pretty name for strip.                |
| device | string  | System serial slave device for strip. |
| number | integer | Slave device strip number.            |

#### Example Config ####

``` json
{
    "systemName": "My LEDnet",
    "strips" : [
        {
            "name": "Kitchen Wall",
            "id": "k_wall",
            "device": "/dev/kitchenusb",
            "number": 0
        },
        {
            "name": "Kitchen Floor",
            "id": "k_floor",
            "device": "/dev/kitchenusb",
            "number": 1
        },
        {
            "name": "Stairs",
            "id": "stairs",
            "device": "/dev/stairsusb",
            "number": 0
        }
    ],
    "cycles": [
      {
        "name": "day",
        "mode": "normal",
        "target": "global",
        "start": "08:00.00"
      },
      {
        "name": "evening",
        "mode": "static",
        "target": "global",
        "values": {
          "red": 128,
          "green": 128,
          "blue": 128
        },
        "start": "21:30.00"
      },
      {
        "name": "night",
        "mode": "off",
        "target": "global",
        "start": "23:30.00"
      }
    ],
    "authKey": "asdfghjkl"
}
```

## API Documentation ##

### View System Info ###

**GET /info**
Returns various useful system parameters.

#### Response Structure ####
| Field      | Type    | Description                                |
| ---------- | ------- | ------------------------------------------ |
| cycle      | string  | Current system cycle.                      |
| strips     | integer | Number of strips attached to system.       |
| systemName | string  | System name as set in `config.json`.       |
| systemTime | string  | Current system time in format: `%H:%M.%S`. |

### View System Config ###

**GET /config**
Returns configuration file.
Returns 401 UNAUTHORISED if authorisation needed.

**POST /config**
Returns configuration file providing authentication.
Returns 401 UNAUTHORISED if authentication is incorrect and 400 BAD REQUEST if POST data is in incorrect format.

#### Request Structure ####
| Field   | Type   | Description                |
| ------- | ------ | -------------------------- |
| authKey | string | System authentication key. |

#### Request Example ####
``` json
{
    "authKey": "asdfghjkl"
}
```

### View Strip Info ###

**GET /led**
Returns data for all strips attached to the system.

#### Response Structure ####
| Field  | Type | Description                        |
| ------ | ---- | ---------------------------------- |
| strips | list | List of strips attached to system. |

#### Strips Structure ####
| Field  | Type    | Description            |
| ------ | ------- | ---------------------- |
| device | string  | Device port.           |
| id     | string  | ID of strip.           |
| name   | string  | Pretty name of strip.  |
| number | integer | Strip index on system. |

### View/Change Strip Values ###

**GET /led/{strip_id}**
Gets strip by ID.
Returns RGB values and current mode.

**POST /led/{strip_id}**
Changes strip RGB values.
Returns new values and current mode on success.
Returns a 400 BAD REQUEST if POST data in incorrect format and 401 UNAUTHORISED if authentiction needed but not supplied.

#### Request Structure ####
| Field   | Type    | Description                                 |
| ------- | ------- | ------------------------------------------- |
| red     | integer | Red value.                                  |
| green   | integer | Green value.                                |
| blue    | integer | Blue value.                                 |
| authKey | string  | Authentication key if set in `config.json`. |

#### Request Examples ####
``` json
{
    "red": 255,
    "green": 128,
    "blue": 0
}
```

``` json
{
    "red": 0,
    "green": 70,
    "blue": 255,
    "authKey": "asdfghjkl"
}
```

#### Response Structure ####
| Field | Type    | Description         |
| ----- | ------- | ------------------- |
| id    | string  | Strip ID.           |
| red   | integer | Red value.          |
| green | integer | Green value.        |
| blue  | integer | Blue value.         |
| mode  | string  | Current strip mode. |

### Errors ###

#### Response Structure ####
| Field       | Type    | Description                 |
| ----------- | ------- | --------------------------- |
| code        | integer | HTTP error code.            |
| description | string  | Description of given error. |
