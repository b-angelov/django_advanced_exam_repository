{% load has_style %}
{% with object_list as obl %}

function DynamicStylesAndContent(){
    const ChangeContent = (elementName, content) => {
        const element = document.querySelector(elementName);
        element.value = content;
    };
    const ChangeTitle = (elementName, content) => {
        document.title = content
    };
    {% hstyle obl 'title' 'title' 'ChangeTitle("title","%s");' %}
}

{% endwith %}

window.addEventListener('load', DynamicStylesAndContent);