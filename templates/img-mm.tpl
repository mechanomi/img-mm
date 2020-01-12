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
  <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
  <input type="hidden" name="lose" value="{{ candidates[1]['filename'] }}">
  <img src="img?filename={{ candidates[0]['filename'] }}" title="{{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()" >


  <form>
  <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
  <input type="hidden" name="lose" value="{{ candidates[0]['filename'] }}">
  <img src="img?filename={{ candidates[1]['filename'] }}" title="{{ candidates[1]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()">
