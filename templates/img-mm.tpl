<style>

body {
  background: url(img?filename=assets/bg.png);
  margin: 2%;
  text-align: center;
}

img {
  width: 45%;
  margin: 2%;
  cursor: hand;
}

</style>

  <form>
  <input type="hidden" name="win" value="{{ files[0]['filename'] }}">
  <input type="hidden" name="lose" value="{{ files[1]['filename'] }}">
  <img src="img?filename={{ files[0]['filename'] }}" title="{{ files[0]['rating'] }}" onclick="submit()" >


  <form>
  <input type="hidden" name="win" value="{{ files[1]['filename'] }}">
  <input type="hidden" name="lose" value="{{ files[0]['filename'] }}">
  <img src="img?filename={{ files[1]['filename'] }}" title="{{ files[1]['rating'] }}" onclick="submit()">
