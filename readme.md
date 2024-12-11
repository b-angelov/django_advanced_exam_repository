# Rozhdestvennik

-----
### *Current deployment servers:*
>> [рождественник](http://рождествен.ник.com)
>>
>> [azure deployment](https://rozhdestvennik-gzfxgbhthsgqh3aw.italynorth-01.azurewebsites.net/articles/)
*****

### *Important notices:*

> - This project is built in English, however it due to its purpose it is highly optimized 
>  and thus localized in Bulgarian. For best user experience, please ensure your browser 
> uses Bulgarian as default request language. Interface language switching is purposly not implemented.

> - This project uses pre-populated database fields, for navigation, styling and the calendar data itself.
>  Please ensure you have followed the basic instalation steps below. It is highly required, for proper installation,
> that a superuser is created after the migrations are done but before the data loading. This ensures, that
> few demonstrative articles will be correctly loaded.
****

### Installation steps:

----
> ```shell 
> python -m venv .venv
> . ./.venv/bin/activate # on linux and MacOs
> ./.venv/Scripts/activate # on Windows
> pip install -r requirements.txt
> python manage.py migrate
> python manage.py createsuperuser
> python manage.py loaddata ./fixed_fixture.json
> ```
----


## Overview

> This projects aims to display dynamic orthodox calendar functionality, based on Bulgarian Orthodox Church's 
> feast and saint list. This includes also dynamically determining the correct position 
> for easter and christmas related holidays, various calendars etc. 
> 
> The calendar itself is standalone app, which serves as a dynamic calendar source, 
> developed in Django, which allows adding articles and previews based on the 
> day of the year, yet letting users creating their own profiles in order to participate in
> the Adoption of the calendar.


-----

## Groups

>There Are 3 types of groups:
> Superusers: can do everything
> Administrators can edit other's article
> Users: can only edit their own staff

-----

# Apps Details
****
### Accounts app
<details>
<summary>This app manages main user functionalities</summary>
<blockquote>
    This  App serves user processing, like user and profile creation ,
    automatic profile assignment to each user, logging, sign up and etc. 
    All corresponding views are accessible in the user interface.
</blockquote>
</details>

*****

### Articles app
<details>
<summary>This app manages articles, and the ways they arfe processed</summary>
<blockquote>
    The app implements all CRUD operations on the articles. Also it provides article filtering views, 
    which sort the articles by given date or default date. 
    <i>Notice, that sorting views default to current date</i>
</blockquote>
</details>

*****

### Common app
<details>
<summary>This app manages default error processing, calendar and home page views</summary>
<blockquote>
    By serving the main page and calendar page this app loads the base template and also manages js scripts 
    and api calls for the calendar.
    <i>This app is the main one to handle js request to orth_calendar api (see below) by implementing js fetcher api modules
    which are dinamically loaded</i>
</blockquote>
<blockquote>
    Noticeable app here is the calendar app. It requires an html element with id main calendar and sub element,
    in that field, then fetches the library for the date provided by the view or the default date, then renders the fetched 
    result in the calendar element.
</blockquote>
</details>

*****

### Navigation app
<details>
<summary>This app implements all required navigation, so please read the details,
        below. The project won't have any navigation if this app isn't properly set and prefilled with data.
        Currently, this app is mainly filled with Bulgarian fields, thus many navigation items
    may not load if other language is served!</summary>
<i>Notice: all adjustments are done through admin interface</i>
<blockquote>
    This app incorporates it's own model in database, which renders navigation link elements in list,
    based on records in the database. All records are associated with language, thus if language isn't chosen
    for an item, this item won't be displayed in the menu. 
</blockquote>
<blockquote>
    The menu itself is rendered by template tag nav_render, which expects template
    the menu as set in the database and the user in order to load the menu for the respective item.
</blockquote>

<blockquote>
    This app incorporates three models:
    <ul>
    <li>language: This is filled automatically with the values of currently enabled languages and should not be set manually.</li>
    <li>Menu: This model sets the available menus. No menu could be added unless defined here. The menu name here is used as key 
    tag for the rendering template tag.</li>
    <li>
        Navigation: This model assigns items to given menu. the fields are
        <ol>
            <li>menu: this item should be set, if the item should be shown at top level of the menu. If the item is a 
            child element, you may ommit this field</li>
            <li>
                name: the element should have name. This name should be in the language chosen below, or in case multiple languages
                are selected, it should stay relevant. Free fontawesome symbols are also allowed here.
            </li>
            <li>
                internal or external url: this should be set to the link to where the item should redirect.
                as internal url a reversable url name could be used, which is the recommended method.
            </li>
            <li>
                order: This fields sets the order of the item of the field. It should usually be set to the last number of element items. 
                However, lesser value could bring this item closer to the beginning. 
                <i>Notice that duplicated items shall be loaded in order of creation.</i>
            </li>
            <li>
                login required: sets the field display to logged users only
            </li>
            <li>
                login not required: forces the field display to anonymous users.
            </li>
            <li>
                permission required: loads the item to user with specific permissions 
            </li>
            <li>
                parent item: This will set to which already enabled menu item the item should be assigned a child.
            </li>
        </ol>
    </li>
</ul>
</blockquote>

</details>

*****

### Styling app
<details>
<summary>This app allows interface style adjustments</summary>
<i>Notice: all adjustments are done through admin interface</i>
<blockquote>
    <h4>How it works?</h4>
    <p>This element renders django template to url /dynamic/style.name/menu which
    loads the respective items through a templatetag in styling template.
    If you want to add additional elements and fields to be rendered,
    you should edit the styling template and add the values of the desired fields. Then add respective database items for the required fields
    And their value shall be present in the rendered CSS</p>
</blockquote>
<blockquote>
    This app implements two models: 
    <ul>
        <li>section: this sets to which CSS section the elements is relevant,
        it also assignes additional attribute, cencerning a different style for the same attribute, to
        deffer different items in distinct menus.
        </li>
        <li>
            option: this model sets different items for respective sections, by setting style,
                CSS attribute value and other adjustments.
            <i>Base on selected field type, the preview of the item is rendered differently
            in order to provide ability to set properties as colour for example in more comfortable way, by UI.</i>
        </li>
    </ul>
</blockquote>

</details>


*****

### Orthodox calendar app

<details>
    <summary>
    <p>This app required the hardest effort in order this project to work.
    Yet its purpose is not directly editable furthermore, thus it might inferrior compared to other parts of the app.</p>
    <p>Let explain what it does mean: To ensure the proper function so: be able to load all holidays
    and all saints for any date in any year, based on calendar style, first an index of all saints and
    feasts had to be implemented. This meant: hand pasting in relevant fields data from the orthodox calendar
    for one whole year, then assigning these days for another one year. By doing this, the app determines whether
    holiday occurrences and feasts occur on a same date in both years first - depending on the distance of this day from last Christmas,
    then by the relevant distance by the date and the Easter in it's corresponding year.
    <p>Thus, an index about the saint's day ot feast's day was to be set about these two holidays,
    towards which a day could differ in the years. After building the required index, the app compares whether
    events occur on same date as this in present year and returns the data if so.</p>
    <p>That explained, it means all fields in database from this app served in the development project,
    and should be restricted to legitimate editors only. For frontend usage, the app provides rest API and views, to serve data, by
    mocking a database object for each requested date, basing it on queries for occurrences in provided years. </p>
    </p>
    </summary>
    <article>
        <h5>API:</h5>
        <p>This app provides API urls for fetching calendar requests, these are:
        <ul>
            <li>/orth_calendar/saints/ endpoint:
                This serves all saints on the date, optional parameters are
                related_holidays (true or false or 0 or 1)
                related_feasts (true or false or 0 or 1)
                which should load all related to the saint objects
            </li>
            <li>
                /orth_calendar/saints/pk/ endpoint:
                provides single saint item, the relevant relations are also available as above.
            </li>
            <li>
                /orth_calendat/feasts/ endpoint:
                This serves all feasts on the date, optional parameters are
                related_holidays (true or false or 0 or 1)
                related_saints (true or false or 0 or 1)
                which should load all related to the saint objects
            </li>
            <li>
                /orth_calendar/feasts/pk/ endpoint:
                provides single feast item, the relevant relations are also available as above.
            </li>
            <li>
                /orth_calendar/holidays/ endpoint:
                This serves all holidays on the date, optional parameters are
                related (true or false or 0 or 1)
                which should load all related to the saint objects
            </li>
            <li>
                /orth_calendar/holidays/pk/
                Serves holiday by pk,
                optional field related (true or false or 0 or 1) is available,
                which should load all related saints and feasts
            </li>
            <li>
                /orth_calendar/holidays/date/
                Serves holiday by given date,
                optional field related (true or false or 0 or 1) is available,
                which should load all related saints and feasts
            </li>
        </ul>
        <i>All fields are purposly get only</i>
        </p>
    </article>
</details>

