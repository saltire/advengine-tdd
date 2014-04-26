# Adventure Engine API Documentation

This is a list of all tests and actions available when writing adventures
for the Adventure Engine.


## Selectors

Some tests and actions take selectors as arguments.
A selector is a string that identifies one or more game objects, usually nouns or rooms.
It can consist of one or more object IDs separated by pipes (`|`), or a wildcard,
and can optionally be followed by one or more filters.

Selectors have four types: *noun*, *room*, *entity* (noun or room),
or *location* (noun, room, or one of the special locations "*INVENTORY*" or "*WORN*").
Selectors of a certain type will only identify objects of that type.

The simplest *wildcard* is an asterisk (`*`).
If filters are specified, you can even leave that out.
This will select all items of the selector's type.

A *numeric wildcard* consists of a percent symbol (`%`) followed by a number,
and stands for the word at that place in the player's command
(excluding articles like "a" and "the"). For instance, if the player typed `open door`
(or `open the door`), the noun selector `%2` would match any nouns with the word `door`,
and the test or action would be performed on that noun or nouns.

A *filter* consists of a colon (`:`) followed by the name of an existing test,
and is used to narrow down the list of objects identified by a selector.
Any test that takes a selector argument can be used as a filter.
Any objects matching the selector will be sent to that filter test,
and only the ones for which the test returns true will be sent to the original test or action.
If the filter takes more than one selector argument, the current set of objects is used
as the first, and the second can be specified in parentheses (e.g. `:test_name(selector2)`).
If the selector has more than one filter, each will be called in turn
with the results of the previous one.



## Tests

Tests always return true or false.
When preceded by a bang (`!`), they will return the opposite of their actual result.

### **any** *entity*

Check if any nouns or rooms match the selector.
A blank selector will return all entities. This can be used in conjunction with filters.

### **var** *variable* [<>=]*value*

Check if *variable* is set to the given *value*. If *value* begins with
a comparison operator (`<`, `>`, `=`, `<=`, `>=`), check if that comparison is true.

### **room** *room*

Check if any given room is the current room.

### **visited** *room*

Check if any given room has been visited by the player.

### **exitexists** direction

Check if the current room has an exit in the given direction.
*direction* can be a word or a numeric wildcard.

### **nounloc** *noun* *location*

Check if any given noun is at any given location.

### **carrying** [*noun*]

Check if any given noun is in the inventory.
If no noun is specified, check if any nouns at all are in the inventory.

### **wearing** [*noun*]

Check if any given noun is being worn.
If no noun is specified, check if any nouns at all are being worn.

### **inroom** *noun*

Check if any given noun is in the current room.

### **present** *noun*

Check if any given noun is in the current room, carried, worn, or inside another present noun.

### **contained** *noun*

Check if any given noun is located inside another noun.

### **somewhere** *noun*

Check if any given noun has at least one location.

### **movable** *noun*

Check if any given noun can be picked up or dropped.

### **wearable** *noun*

Check if any given noun can be worn.

### **hasdesc** *entity*

Check if any given noun or room has a description set.

### **hasnotes** *entity*

Check if any given noun or room has at least one note set.

### **hascontents** *location*

Check if any given location has at least one noun located inside it.

### **random** percent

Return true a given percent of the time.


## Actions

Actions return a list of messages, when appropriate.
The exception is the **pause** action, which returns a 'PAUSE' symbol instead of a message.
Clients should check for this symbol and handle it however they like.

### **message** messageID [, messageID, ...]

Return the message for each given message ID.
Any numerical wildcards in messages are substituted with the corresponding word.

### **pause**

Return a symbol indicating that the game should pause and wait for a keypress.

### **showdesc** [*entity*]

Return the description of each entity.
If no entity is specified, return the description of the current room.

### **shownotes** [*entity*]

Return all notes for each entity.
If no entity is specified, return the notes for the current room.

### **showcontents** [*location*] [text] [indent] [in_msg] [worn_msg] [recursive] [contains_msg]

Return a listing of all nouns at each given location.
If no location is specified, list the nouns in the current room.

This action has several other optional arguments:
- *text* is an attribute of the noun to use for the listing, defaulting to its name.
- *noun_msg* specifies a message to use for the listing instead of just the value set by *text*.
  The wildcard `%NOUN` should be in this message, and will be replaced with that value.
- *in_msg* specifies a message to display after the noun if it is contained inside another noun.
  If the wildcard `%NOUN` is in the message,
  it will be replaced with the containing noun's short name.
- *worn_msg* specifies a message to display after the noun if it is being worn.
- *recursive* decides whether to list any nouns inside the listed nouns; default is false.
- *indent* decides whether the list will be indented (useful for recursive lists); default is false.
- *contains_msg* specifies a message to display before a list of nouns inside another noun.
  If the wildcard `%NOUN` is in the message,
  it will be replaced with the containing noun's short name.

### **inv** [text] [indent] [in_msg] [worn_msg] [recursive] [contains_msg]

Return a listing of all nouns in the inventory. Options are the same as for **showcontents**.

### 
