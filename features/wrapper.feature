Feature: Custom wrapper for dictionary that saves stuff to index.
    This is for testing whether the dictionary wrapper works properly

Scenario: Wd object is provided a string key and string value and has to store and retrieve them.
    Store a string key and string value
    Retrieve via key for string key and string value

Scenario: Wd object is provided a listOfStrings[elementID] as key, string as value, and has to store and retrieve.
    Store a listOfStrings element as key and string as value
    Retrieve via key for string-list-element key and string value

Scenario: Wd object is provided a string as key, listOfStrings[elementID] as value, and has to store and retrieve them.
    Store a string as key and listOfStrings element as value
    Retrieve via key for string key and string-list-element value