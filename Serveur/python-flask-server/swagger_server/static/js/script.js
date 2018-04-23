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

		if (parseInt(canvasX / realWidth) + parseInt(canvasY / realHeight) * 6 >= 8*6)
			return;
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

c.addEventListener('mouseout', function (event) {
	down = false;
}, false);

function draw() {
	taille_i = 8;
	taille_j = 6;

	for (var i = 0; i < taille_i; i++) {
		for (var j = 0; j < taille_j; j++) {
			if(number[i * 6 + j] == null){
				number[i * 6 + j] = -1;
			}

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

function eraseNull(table){
	var retour = table;
	for (var i = 0; i < 8; i++) {
		for (var j = 0; j < 6; j++) {
			if(retour[i * 6 + j] == null){
				retour[i * 6 + j] = -1;
				console.log("Un null detecté en "+i+":"+j);
			}
		}
	}
	return retour;
}

function displayNumber() {
	//alert("[" + number.toString() + "]");
	alert(JSON.stringify(number));
}

function addToTrain() {
	var chiffre = -1;
	number = eraseNull(number);
	draw();
	while(isNaN(chiffre) || (chiffre<0 || chiffre>9)){
		chiffre = prompt("Quel chiffre avez vous écrit ?", 0);
		if(chiffre == null){
			return;
		}
    	chiffre = parseInt(chiffre);
	}
    var data = JSON.stringify({'data':number,'solution':chiffre});
    number = eraseNull(number);
	draw();
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
	number = eraseNull(number);
	draw();
	data = JSON.stringify({'data':number});
	number = eraseNull(number);
	draw();
	$.ajax({
	    url: "/test",
	    type: "post",
	    contentType: "application/json",
	    datatype:"json",
	    data: data,
	    success: function(response){
	        //mettre à jour les resultats
	        //kvoisin
	        $('#res_kvois').text(response.kmeans);
	        //bayesienne
			$('#res_bayes').text(response.baye);
	        //neurones
			$('#res_neuro').text(response.neural);

	        //Une fois les resultats reçus on mets à jour les matrices
			getMatrix();
	    },
	    error: function(jqXHR,textStatus,errorThrown){
	    	alert(" !!! Une erreur a eu lieu voir la console pour plus d'info !!! ");
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
        url: "/getMatrix",
        type: "get",
        contentType: "application/json",
        success: function(response){
            var id;
            var totalCorrect = [0, 0, 0];
            var total = [0, 0, 0];
            for(i=0;i<11;i++){
            	id_k = '#'+response.data[1].method+'_ligne'+i;
            	id_b = '#'+response.data[0].method+'_ligne'+i;
            	id_n = '#'+response.data[2].method+'_ligne'+i;
				$(id_k).empty();
				$(id_b).empty();
				$(id_n).empty();
				if (i == 10){
					$(id_k).append('<th scope="row">percent</th>');
					$(id_b).append('<th scope="row">percent</th>');
					$(id_n).append('<th scope="row">percent</th>');
				}
				else {
					$(id_k).append('<th scope="row">' + i + '</th>');
					$(id_b).append('<th scope="row">' + i + '</th>');
					$(id_n).append('<th scope="row">' + i + '</th>');
				}
				for(j=0; j<11; j++){
					if(i == 10 || j == 10){

						if(i == j){
							var k = totalCorrect[1]/total[1];
							var b = totalCorrect[0]/total[0];
							var n = totalCorrect[2]/total[2];
							$(id_k).append("<th class='ui-helper-green'>" + k + "</th>");
							$(id_b).append("<th class='ui-helper-green'>" + b + "</th>");
							$(id_n).append("<th class='ui-helper-green'>" + n + "</th>");
						}
						else{
							$(id_k).append("<th class='ui-helper-green'></th>");
							$(id_b).append("<th class='ui-helper-green'></th>");
							$(id_n).append("<th class='ui-helper-green'></th>");
						}
						continue;
					}

					total[0] += response.data[0].matrix[i][j];
					total[1] += response.data[1].matrix[i][j];
					total[2] += response.data[2].matrix[i][j];

					if (i==j){
						$(id_k).append("<th class='ui-helper-green'>"+response.data[1].matrix[i][j]+"</th>");
						$(id_b).append("<th class='ui-helper-green'>"+response.data[0].matrix[i][j]+"</th>");
						$(id_n).append("<th class='ui-helper-green'>"+response.data[2].matrix[i][j]+"</th>");
						totalCorrect[0] += response.data[0].matrix[i][j];
						totalCorrect[1] += response.data[1].matrix[i][j];
						totalCorrect[2] += response.data[2].matrix[i][j];
					}else{
						$(id_k).append("<th>"+response.data[1].matrix[i][j]+"</th>");
						$(id_b).append("<th>"+response.data[0].matrix[i][j]+"</th>");
						$(id_n).append("<th>"+response.data[2].matrix[i][j]+"</th>");
					}
				}
            }

        },
        error: function(jqXHR,textStatus,errorThrown){
        	alert(" !!! Une erreur a eu lieu voir la console pour plus d'info !!! ");
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
getMatrix();