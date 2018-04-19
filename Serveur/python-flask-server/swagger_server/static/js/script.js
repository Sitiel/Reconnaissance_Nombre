number = new Array(6 * 8);
number.fill(-1, 0);

var c   = document.getElementById("canvas");
var ctx = c.getContext("2d");

var width      = 6;
var height     = 8;
var realWidth  = c.width / width;
var realHeight = c.height / height;

var down = false;

c.addEventListener('mousedown', function (event) {
	var totalOffsetX   = 0;
	var totalOffsetY   = 0;
	var canvasX        = 0;
	var canvasY        = 0;
	var currentElement = this;

	do {
		totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
		totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
	}
	while (currentElement = currentElement.offsetParent);

	canvasX = event.pageX - totalOffsetX;
	canvasY = event.pageY - totalOffsetY;

	var i = parseInt(canvasY / realHeight);
	var j = parseInt(canvasX / realWidth);
	if (number[j + i * 6] === 1) {
		number[j + i * 6] = -1;
		draw();
		/*ctx.fillStyle = "#FFFFFF";
		ctx.fillRect(j * realWidth+1, i * realHeight+1, realWidth-2, realHeight-2);*/
	}
	else {
		ctx.fillStyle = "#000000";
		ctx.fillRect(j * realWidth, i * realHeight, realWidth, realHeight);
		number[j + i * 6] = 1;
		down              = true;
	}


}, false);

c.addEventListener('mousemove', function (event) {
	if (down) {
		var totalOffsetX   = 0;
		var totalOffsetY   = 0;
		var canvasX        = 0;
		var canvasY        = 0;
		var currentElement = this;

		do {
			totalOffsetX += currentElement.offsetLeft - currentElement.scrollLeft;
			totalOffsetY += currentElement.offsetTop - currentElement.scrollTop;
		}
		while (currentElement = currentElement.offsetParent);

		canvasX = event.pageX - totalOffsetX;
		canvasY = event.pageY - totalOffsetY;

		number[parseInt(canvasX / realWidth) + parseInt(canvasY / realHeight) * 6] = 1;
		var i                                                                      = parseInt(canvasY / realHeight);
		var j                                                                      = parseInt(canvasX / realWidth);
		ctx.fillStyle                                                              = "#000000";
		ctx.fillRect(j * realWidth, i * realHeight, realWidth, realHeight);
	}
}, false);

c.addEventListener('mouseup', function (event) {
	down = false;
}, false);

function draw() {
	taille_i = 8;
	taille_j = 6;

	for (var i = 0; i < taille_i; i++) {
		for (var j = 0; j < taille_j; j++) {

			if (number[i * 6 + j] === 1) {
				ctx.fillStyle = "#000000";
				ctx.fillRect(j * realWidth, i * realHeight, realWidth, realHeight);
			}
			else {
				ctx.fillStyle = "#FFFFFF";
				ctx.fillRect(j * realWidth, i * realHeight, realWidth, realHeight);
			}

			ctx.moveTo(j * realWidth, 0);
			ctx.lineTo(j * realWidth, c.height);
			ctx.stroke();

			ctx.moveTo(0, i * realHeight);
			ctx.lineTo(c.width, i * realHeight);
			ctx.stroke();

		}
	}
}

function displayNumber() {
	//alert("[" + number.toString() + "]");
	alert(JSON.stringify(number));
}

function addToTrain() {

    var chiffre = prompt("Quel chiffre avez vous écrit ?", 0);
    chiffre = parseInt(chiffre);
    var data = JSON.stringify({'data':number,'solution':chiffre});
    console.log(data);
    $.ajax({
    	url: "/add",
        type: "post",
        contentType: "application/json",
        datatype:"json",
        data: data,
        success: function(response){
            alert("Reçu");
        },
        error: function(jqXHR,textStatus,errorThrown){
        	alert("ERROR");
        	console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
        }
    });

}

function sendToDB() {
	//Fonction avec un appel ajax qui va envoyer en AJAX au format JSON l'image dessinée et l'envoyer au serveur python
    displayNumber();
    data = JSON.stringify({'data':number});
    $.ajax({
        url: "/test",
        type: "post",
        contentType: "application/json",
        datatype:"json",
        data: data,
        success: function(response){
            alert("Reçu");
            //Une fois les resultats reçus on mets a jour les matrices
    		getMatrix();
        },
        error: function(jqXHR,textStatus,errorThrown){
        	alert("ERROR");
        	console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
        }
    });
    
}	

function getMatrix() {
	$.ajax({
        url: "localhost:8080/add",
        type: "post",
        contentType: "application/json; charset=utf-8",
        success: function(response){
            alert("Reçu");
        },
        error: function(jqXHR,textStatus,errorThrown){
        	alert("ERROR");
        	console.log('jqXHR:');
            console.log(jqXHR);
            console.log('textStatus:');
            console.log(textStatus);
            console.log('errorThrown:');
            console.log(errorThrown);
        }
    });
}



function clearNumber() {
	number.fill(-1, 0);
	draw();
}

draw();