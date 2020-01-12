<style>

body {
  background: url(img?filename=assets/bg.png);
  margin: 2%;
  text-align: center;
}

img {
    width: 45%;
    margin: 2%;
}

</style>

{% for file in files %}
  <img src="img?filename={{ file["filename"] }}">
{% endfor %}
