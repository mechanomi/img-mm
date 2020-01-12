<ul>
{% for file in files %}
  <li>
    filename: {{ file["filename"] }}<br>
    mtime: {{ file["mtime"] }}<br>
    previous_rating: {{ file["previous_rating"] }}<br>
    rating: {{ file["rating"] }}<br>
  </li>
{% endfor %}
</ul>
