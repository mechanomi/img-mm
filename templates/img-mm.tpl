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

.result img,
.undo img {
    max-height: 8vh;
    max-width: 100%;
}

#result-win {
    background: green;
    padding: 10px;
}

#result-lose {
    background: white;
    padding: 10px;
}

#result-rm {
    background: red;
    padding: 10px;
}

.undo {
    background: yellow;
    padding: 10px;
}

#candidate-0 {
    clear: left;
}

</style>

{% if undo %}

  <form>

    <div class="undo" id="undo-win">
      <img src="img?filename={{ undo['win']['filename'] | urlencode }}" title="{{ undo['win']['rank'] }}, {{ undo['win']['rating'].sigma }}" onclick="submit()" >
    </div>

    {% if undo['lose'] %}
      <div class="undo" id="undo-lose">
        <img src="img?filename={{ undo['lose']['filename'] | urlencode }}" title="{{ undo['lose']['rank'] }}, {{ undo['lose']['rating'].sigma }}" onclick="submit()" >
      </div>
    {% endif %}

    {% if undo['rm'] %}
      <div class="undo" id="undo-rm">
        <img src="img?filename={{ undo['rm']['filename'] }}" title="{{ undo['rm']['rank'] }}, {{ undo['rm']['rating'].sigma }}" onclick="submit()" >
      </div>
    {% endif %}

  </form>

{% endif %}

{% if results %}

  <form>

    <div class="result" id="result-win">
      <img src="img?filename={{ results['win']['filename'] | urlencode }}" title="{{ results['win']['rank'] }}, {{ results['win']['rating'].sigma }}" onclick="submit()" >
    </div>
    <input type="hidden" name="unwin" value="{{ results['win']['filename'] }}">

    {% if results['lose'] %}
      <div class="result" id="result-lose">
        <img src="img?filename={{ results['lose']['filename'] | urlencode }}" title="{{ results['lose']['rank'] }}, {{ results['lose']['rating'].sigma }}" onclick="submit()" >
      </div>
      <input type="hidden" name="unlose" value="{{ results['lose']['filename'] }}">
    {% endif %}

    {% if results['rm'] %}
      <div class="result" id="result-rm">
        <img src="img?filename={{ results['rm']['filename'] }}" title="{{ results['rm']['rank'] }}, {{ results['rm']['rating'].sigma }}" onclick="submit()" >
      </div>
      <input type="hidden" name="unrm" value="{{ results['rm']['filename'] }}">
    {% endif %}

    <br>

    <input type="submit" value="UNDO">

  </form>

{% endif %}

<div class="candidate" id="candidate-0">
  <form id="c0-win">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[1]['filename'] }}">
    <img src="img?filename={{ candidates[0]['filename'] | urlencode }}" title="{{ candidates[0]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()" >
    <br><br>
    <input type="submit" value="WIN">
  </form>
  <form id="c0-rm">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="rm" value="{{ candidates[0]['filename'] }}">
    <input type="submit" value="REMOVE">
  </form>
</div>

<div class="candidate" id="candidate-1">
  <form id="c1-win">
    <input type="hidden" name="win" value="{{ candidates[1]['filename'] }}">
    <input type="hidden" name="lose" value="{{ candidates[0]['filename'] }}">
    <img src="img?filename={{ candidates[1]['filename'] | urlencode }}" title="{{ candidates[1]['rank'] }}, {{ candidates[0]['rating'].sigma }}" onclick="submit()">
    <br><br>
    <input type="submit" value="WIN">
  </form>
  <form id="c1-rm">
    <input type="hidden" name="win" value="{{ candidates[0]['filename'] }}">
    <input type="hidden" name="rm" value="{{ candidates[1]['filename'] }}">
    <input type="submit" value="REMOVE">
  </form>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<script>

$(document).keydown(function(e) {
    // Left arrow key
    if (e.which == 37) {
        if (e.shiftKey) {
            $("#c1-rm").submit();
        } else {
            $("#c0-win").submit();
        }
        e.preventDefault();
    }
    // Right arrow key
    if (e.which == 39) {
        if (e.shiftKey) {
            $("#c0-rm").submit();
        } else {
            $("#c1-win").submit();
        }
        e.preventDefault();
    }
})

</script>
