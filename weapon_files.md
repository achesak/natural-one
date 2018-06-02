# Weapon data files

Natural One uses JSON files to store weapon data for use in damage rolls. This allows for data from RPGs
other than what Natural One supports by default to be added with minimal effort.

## Data file location

All data files must be located in `resources/data/weapons/`, and must be JSON files. In order for the
application to find and load the files, they must also be registered in the `weapons.json` meta file,
located in `resources/data`. 

`weapons.json` contains a `systems` array, with each element containing the name of the system and the
filename of the data file. Registering a data file is as simple as creating a new object in this array.

For example, to add system "Demo Game System" with filename `demogamesystem.json`, this would be added:

```json
{
    "systems": [
        {
            "name": "Demo Game System",
            "filename": "demogamesystem.json"
        }
    ]
}
```

Natural One will then load the data and be able to use it on the next application startup.

## Data file format

Each data file is a JSON object with two keys: `system` and `data`. `system` should be the same as the
system name in the `weapons.json` meta file. `data` is an array of the weapon data, organized into
categories.

## Category objects

Each category is an object with two fields. `category` is the name of the category, and is displayed
in the UI to make it easier for the user to find the weapon they are looking for. `weapons` is an array
of weapon objects.

## Weapon objects

Required keys:
* `name` - The name displayed to the user in the weapon selection
* One or more damage objects. See below.
* `crit_range` - The minimum value the weapon can score a critical on. For systems that only have
  criticals on natural 20s, this should be 20
* `crit_mult` - The critical multiplier of the weapon

Optional keyss:
* `display` - If present, this will be used instead of `name` when displaying the results of the roll. 
  For example, the spiked gauntlet in Pathfinder uses a `name` of "Gauntlet, spiked" and a `display` of
  "Spiked gauntlet"
* `no_format` - If present and set to `true`, the weapon name when displaying the results of the roll
  will not be converted to lowercase.
* `reroll_below` - If present, rolls lower than or equal to this number will be rerolled until above.
* `dmg_static` - If present, this value will be added to the damage roll. Note that this is NOT intended
  for player modifiers and should only be used if the weapon ALWAYS has this damage added.
* `max_on_crit` - If present and set to `true`, then `crit_mult` is ignored when determining critical
  damage, and the damage on critical hits is the weapon's maximum possible damage roll.
* `crit_extra` - If present, this specifies extra damage to roll or add only on critical attacks. See
  below.

### Weapon damage objects

Natural One supports both systems that change damage based on character size and those that do not.

For systems that change damage die by size, two keys must be present in the weapon object: `dmg_small`
and `dmg_medium`. Each key is an array of objects, with each object having `count` and `die` keys; these
are the values that determine the number (`count`) of which die (`die`) to roll.

Example:
```json
{
    "name": "Dagger",
    "dmg_small": [
        {
            "count": 1,
            "die": 3
        }
    ],
    "dmg_medium": [
        {
            "count": 1,
            "die": 4
        }
    ],
    "crit_range": 19,
    "crit_mult": 2
}
```

For systems that do not change damage die by size, another key, `no_size_steps` must be present and set
to `true`. In this case, there should only be one key for damage, called `dmg`.

Example:
```json
{
    "name": "Club",
    "no_size_steps": true,
    "dmg": [
        {
            "count": 1,
            "die": 6
        }
    ],
    "crit_range": 20,
    "crit_mult": 2
}
```


### Extra critical objects

The `crit_extra` object, if present, should contain a list of rolls or extra damage to add only on
critical hits. This is formatted very similarly to weapon damage objects.

If using a system that changes damage die by character size, use two damage lists, `dmg_small` and
`dmg_medium`. Otherwise, use one list called `dmg`. Note that this object does not require a
`no_size_steps` field, as it inherits the value already specified in the weapon object.

A `dmg_static` field can also be specified, functioning just like its counterpart in the weapon 
objects.

Example:
```json
{
    "name": "Flame rifle",
    "no_size_steps": true,
    "dmg": [
        {
            "count": 1,
            "die": 6
        }
    ],
    "crit_range": 20,
    "crit_mult": 2,
    "crit_extra": {
        "dmg": [
            {
                "count": 1,
                "die": 6
            }
        ]
    }
}
```