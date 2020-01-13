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
  {{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}<br>
  <form id="c1">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[1]['filename'] }}">
    <img src="img?filename={{ candidates[0]['filename'] }}" title="{{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()" >
  </form>
</div>

<div>
  {{ candidates[1]['rank'] }}, {{ candidates[1]['rating'].sigma }}<br>
  <form id="c2">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[0]['filename'] }}">
    <img src="img?filename={{ candidates[1]['filename'] }}" title="{{ candidates[1]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()">
  </form>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<script>

$(document).keydown(function(e) {
    // Left arrow key
    if (e.which == 37) {
        $("#c1").submit();
        e.preventDefault();
    }
    // Right arrow key
    if (e.which == 39) {
        $("#c2").submit();
        e.preventDefault();
    }
})

</script>
