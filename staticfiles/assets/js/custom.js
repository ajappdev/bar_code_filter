///////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////
//////////////DECLARING FUNCTIONS//////////////////////////
///////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////
function numberWithCommas(x, relplace_with)
{
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, relplace_with);
}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


 
function formatAiAnswer(text) {
    // Replace ```python with <pre><code class="language-python">
    text = text.replace(/```python/g, '<pre><code class="language-python">');

    // Replace ``` with </code></pre>
    text = text.replace(/```/g, '</code></pre>');

    text = text.replace(/`([^`]+)`/g, '<b>$1</b>');

    return text;
}
 