# LEDnet #

LEDnet was born after I bought a pile of RGB LED strip on eBay in the spur of the moment and wanted to control it all from one remote but have the strips installed around my house.
I already had lots of hardware kicking about so I built it to use what I had.

How does it work? This software runs on a Raspberry Pi which is connected to your local network.
The Raspberry Pi has a serial connection to an Arduino compatible microcontroller which can control one of more strips over serial (number of strips depends on your Arduino type).
The Uno has 6 PWM lanes so can drive 2 strips, with the help of some MOSFETS.
See setup below on how to wire it up.
The whole system is controlled by a REST API on the Pi.

Control Clients:
 * Android App (WIP) - written by me.
 * iOS App (WIP) - written by Huw Jones.
 * EMF Tilda MkPi Badge App (WIP) - written by me.

## Installation / Setup ##


## Configuration File Options ##

| Field      | Type    | Description                                 |
| ---------- | ------- | ------------------------------------------- |
| systemName | string  | System name.                                |
| strips     | list    | Configuration of strips attached to system. |
| cycle      | JSON    | Day/Night cycle start times.                |
| authKey    | string  | System authentication key.                  |

#### Cycle Options ####

| Field   | Type   | Description                      |
| ------- | ------ | -------------------------------- |
| day     | string | Starting time for day cycle.     |
| evening | string | Starting time for evening cycle. |
| night   | string | Starting time for night cycle.   |

Time needs to be given in the format `%H:%M.%S`.

#### Strips Options ####

| Field  | Type    | Description                    |
| ------ | ------- | ------------------------------ |
| id     | string  | Strip identifier used for API. |
| name   | string  | Pretty name for strip.         |
| device | string  | Serial device for strip.       |
| number | integer | Serial device strip number.    |

#### Example Config ####

``` json
{
    "systemName": "namae",
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
    "cycle": {
        "day": "08:00.00",
        "evening": "21:30.00",
        "night": "23:30.00"
    },
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
Returns number of strips on system.

#### Response Structure ####
| Field  | Type | Description                        |
| ------ | ---- | ---------------------------------- |
| strips | list | List of strips attached to system. |

### View/Change Strip Values ###

**GET /led/{strip_number}**
Gets strip by ID number.
Returns RGB values and current mode.

**POST /led/{strip_number}**
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
