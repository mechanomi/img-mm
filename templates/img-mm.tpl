<ul>
{% for file in files %}
  <li>
    filename: {{ file["filename"] }}<br>
    mtime: {{ file["mtime"] }}<br>
    rating: {{ file["rating"] }}
  </li>
{% endfor %}
</ul>
