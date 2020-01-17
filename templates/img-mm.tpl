<style>

body {
  background: url(img?filename=assets/bg.png);
  margin: 0 0 1vh 1vh;
  padding: 0;
}

form {
  margin: 0;
  display: inline;
}

input {
    font-size: 2em;
}

div {
  display: inline;
  text-align: center;
  float: left;
  max-width: 49vw;
  margin: 1vh 1vh 0 0;
}

img {
  cursor: hand;
  max-height: 98vh;
  max-width: 100%;
}

</style>

<div>
  <form id="c0-win">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[1]['filename'] }}">
    <img src="img?filename={{ candidates[0]['filename'] }}" title="{{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()" >
    <br><br>
    <input type="submit" value="WIN">
  </form>
  <form id="c0-delete">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="delete" value="{{ candidates[0]['filename'] }}">
    <input type="submit" value="DELETE">
  </form>
</div>

<div>
  <form id="c1-win">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[0]['filename'] }}">
    <img src="img?filename={{ candidates[1]['filename'] }}" title="{{ candidates[1]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()">
    <br><br>
    <input type="submit" value="WIN">
  </form>
  <form id="c1-delete">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="delete" value="{{ candidates[1]['filename'] }}">
    <input type="submit" value="DELETE">
  </form>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<script>

$(document).keydown(function(e) {
    // Left arrow key
    if (e.which == 37) {
        $("#c0").submit();
        e.preventDefault();
    }
    // Right arrow key
    if (e.which == 39) {
        $("#c1").submit();
        e.preventDefault();
    }
})

</script>
