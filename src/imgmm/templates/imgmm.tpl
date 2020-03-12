<style>

body {
    background: url(img?filename={{ src_dir }}/assets/bg.png);
    margin: 1vh;
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

.status {
    background: white;
    padding: 1vh;
}

</style>

<p class="status">{{ imgs_count }} images, {{ unrated_imgs_count }} unrated, {{ unrated_pct }}% coverage, {{ avg_sigma }} avg. sigma</p>

{% if undo %}

  <form>

    <div class="undo" id="undo-win">
      <img src="img?filename={{ undo['win'].filename | urlencode }}" title="{{ undo['win'].rank }}, {{ undo['win'].rating.sigma }}" onclick="submit()" >
    </div>

    {% if undo['lose'] %}
      <div class="undo" id="undo-lose">
        <img src="img?filename={{ undo['lose'].filename | urlencode }}" title="{{ undo['lose'].rank }}, {{ undo['lose'].rating.sigma }}" onclick="submit()" >
      </div>
    {% endif %}

    {% if undo['rm'] %}
      <div class="undo" id="undo-rm">
        <img src="img?filename={{ undo['rm'].filename }}" title="{{ undo['rm'].rank }}, {{ undo['rm'].rating.sigma }}" onclick="submit()" >
      </div>
    {% endif %}

  </form>

{% endif %}

{% if results %}

  <form>

    <div class="result" id="result-win">
      <img src="img?filename={{ results['win'].filename | urlencode }}" title="{{ results['win'].rank }}, {{ results['win'].rating.sigma }}" onclick="submit()" >
    </div>
    <input type="hidden" name="unwin" value="{{ results['win'].filename }}">

    {% if results['lose'] %}
      <div class="result" id="result-lose">
        <img src="img?filename={{ results['lose'].filename | urlencode }}" title="{{ results['lose'].rank }}, {{ results['lose'].rating.sigma }}" onclick="submit()" >
      </div>
      <input type="hidden" name="unlose" value="{{ results['lose'].filename }}">
    {% endif %}

    {% if results['rm'] %}
      <div class="result" id="result-rm">
        <img src="img?filename={{ results['rm'].filename }}" title="{{ results['rm'].rank }}, {{ results['rm'].rating.sigma }}" onclick="submit()" >
      </div>
      <input type="hidden" name="unrm" value="{{ results['rm'].filename }}">
    {% endif %}

    <br>

    <input type="submit" value="UNDO">

  </form>

{% endif %}

<div class="candidate" id="candidate-0">
  <img src="img?filename={{ candidates[0].filename | urlencode }}&ts={{ ts }}" title="{{ candidates[0].rank }}, {{ candidates[0].rating.sigma }}" onclick="submit()" >
  <br><br>
  <form id="c0-rotate-cw">
    <input type="hidden" name="rotate_img" value="{{ candidates[0].filename }}">
    <input type="hidden" name="direction" value="cw">
    <input type="submit" value="↻">
  </form>
  <form id="c0-win">
    <input type="hidden" name="win" value="{{ candidates[1].filename }}">
    <input type="hidden" name="lose" value="{{ candidates[0].filename }}">
    <input type="submit" value="LOSE">
  </form>
  <form id="c0-rm">
    <input type="hidden" name="win" value="{{ candidates[1].filename }}">
    <input type="hidden" name="rm" value="{{ candidates[0].filename }}">
    <input type="submit" value="REMOVE">
  </form>
  <form id="c0-rotate-ccw">
    <input type="hidden" name="rotate_img" value="{{ candidates[0].filename }}">
    <input type="hidden" name="direction" value="ccw">
    <input type="submit" value="↺">
  </form>
</div>

<div class="candidate" id="candidate-1">
  <img src="img?filename={{ candidates[1].filename | urlencode }}&ts={{ ts }}" title="{{ candidates[1].rank }}, {{ candidates[0].rating.sigma }}" onclick="submit()">
  <br><br>
  <form id="c0-rotate-cw">
    <input type="hidden" name="rotate_img" value="{{ candidates[1].filename }}">
    <input type="hidden" name="direction" value="cw">
    <input type="submit" value="↻">
  </form>
  <form id="c1-win">
    <input type="hidden" name="win" value="{{ candidates[0].filename }}">
    <input type="hidden" name="lose" value="{{ candidates[1].filename }}">
    <input type="submit" value="LOSE">
  </form>
  <form id="c1-rm">
    <input type="hidden" name="win" value="{{ candidates[0].filename }}">
    <input type="hidden" name="rm" value="{{ candidates[1].filename }}">
    <input type="submit" value="REMOVE">
  </form>
  <form id="c0-rotate-ccw">
    <input type="hidden" name="rotate_img" value="{{ candidates[1].filename }}">
    <input type="hidden" name="direction" value="ccw">
    <input type="submit" value="↺">
  </form>
</div>

<br><br>

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
