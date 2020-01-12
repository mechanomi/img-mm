<ul>
{% for file in files %}
  <li>{{ file["filename"] }} - {{ file["mtime"] }}</a></li>
{% endfor %}
</ul>
