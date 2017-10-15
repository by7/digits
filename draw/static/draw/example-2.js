// Keep everything in anonymous function, called on window load.
if(window.addEventListener) {
window.addEventListener('load', function () {
  var canvas, context, tool;

  function init () {
    // Find the canvas element.
    canvas = document.getElementById('imageView');
    if (!canvas) {
      alert('Error: I cannot find the canvas element!');
      return;
    }

    if (!canvas.getContext) {
      alert('Error: no canvas.getContext!');
      return;
    }

    // Get the 2D canvas context.
    context = canvas.getContext('2d');
    if (!context) {
      alert('Error: failed to getContext!');
      return;
    }
	context.lineWidth = 5;

    // Pencil tool instance.
    tool = new tool_pencil();

    // Attach the mousedown, mousemove and mouseup event listeners.
    canvas.addEventListener('mousedown', ev_canvas, false);
    canvas.addEventListener('mousemove', ev_canvas, false);
    canvas.addEventListener('mouseup',   ev_canvas, false);
  }

  
  function getOffset( el ) {
    var _x = 0;
    var _y = 0;
    while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
        _x += el.offsetLeft - el.scrollLeft;
        _y += el.offsetTop - el.scrollTop;
        el = el.offsetParent;
    }
    return { top: _y, left: _x };
  }
  
  // This painting tool works like a drawing pencil which tracks the mouse 
  // movements.
  function tool_pencil () {
    var tool = this;
    this.started = false;
	var offset = getOffset(canvas);
	
    // This is called when you start holding down the mouse button.
    // This starts the pencil drawing.
    this.mousedown = function (ev) {
        context.beginPath();
        context.moveTo((ev.pageX-offset.left), (ev.pageY-offset.top));
        tool.started = true;
    };

    // This function is called every time you move the mouse. Obviously, it only 
    // draws if the tool.started state is set to true (when you are holding down 
    // the mouse button).
    this.mousemove = function (ev) {
      if (tool.started) {
        context.lineTo((ev.pageX-offset.left), (ev.pageY-offset.top));
        context.stroke();
      }
    };

    // This is called when you release the mouse button.
    this.mouseup = function (ev) {
      if (tool.started) {
        tool.mousemove(ev);
        tool.started = false;
      }
    };
  }

  // The general-purpose event handler. This function just determines the mouse 
  // position relative to the canvas element.
  function ev_canvas (ev) {

    // Call the event handler of the tool.
    var func = tool[ev.type];
    if (func) {
      func(ev);
    }
  }
  
  function ev_canvas_touch (ev) {
    if (ev.touches[0].layerX || ev.touches[0].layerX == 0) { // Firefox
      ev._x = ev.touches[0].layerX;
      ev._y = ev.touches[0].layerY;
    } else if (ev.touches[0].offsetX || ev.touches[0].offsetX == 0) { // Opera
      ev._x = ev.touches[0].offsetX;
      ev._y = ev.touches[0].offsetY;
    }

    // Call the event handler of the tool.
    var func = tool[ev.touches[0].type];
    if (func) {
      func(ev.touches[0]);
    }
  }

  init();

}, false); }
