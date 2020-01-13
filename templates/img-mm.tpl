<style>

body {
  background: url(img?filename=assets/bg.png);
  margin: 0 0 0 1%;
  padding: 0;
}

form {
  margin: 0;
}

div {
  display: inline;
  float: left;
  width: 49%;
  margin: 1% 1% 0 0;
}

img {
  cursor: hand;
  width: 100%;
}

</style>

<div>
  <form id="c1" class="candidate">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[1]['filename'] }}">
    <img src="img?filename={{ candidates[0]['filename'] }}" title="{{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()" >
  </form>
</div>

<div>
  <form id="c2" class="candidate">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[0]['filename'] }}">
    <img src="img?filename={{ candidates[1]['filename'] }}" title="{{ candidates[1]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()">
  </form>
</div>
