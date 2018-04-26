//Modal

//////////
//CANVAS//
//////////
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
		drawWhite(i,j);
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

function drawWhite(x,y){

	ctx.fillStyle = "#FFFFFF";
	ctx.fillRect(y * realWidth, x * realHeight, realWidth, realHeight);

	ctx.moveTo(y * realWidth, 0);
	ctx.lineTo(y * realWidth, c.height);
	ctx.stroke();

	ctx.moveTo(0, x * realHeight);
	ctx.lineTo(c.width, x * realHeight);
	ctx.stroke();
}


function clearNumber() {
	number.fill(-1, 0);
	draw();
}

//////////
//////////
//////////


//////////
///AJAX///
//////////

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
            //Une fois les resultats reçus on mets à jour les matrices
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
			//all
			$('#res_all').text(response.all);
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

function getColorScheme(num){
	//KVOISIN
	if(num > 75.0){
		return "ui-helper-green";
	}else if(num > 40.0){
		return "ui-helper-orange";
	}else{
		return "ui-helper-red";
	}
}

function getPercentage(num){
	ret = 0
	if(isNaN(num)){
		return ret.toFixed(1);
	}else{
		return num.toFixed(1);
	}
}


function getMatrix() {
	$.ajax({
        url: "/getMatrix",
        type: "get",
        contentType: "application/json",
        success: function(response){
            var id;
            var k_color;
            var b_color;
            var n_color;
            var a_color;
            //Diagonnal
            var totalCorrect = [0, 0, 0, 0];
            var total = [0, 0, 0, 0];
            //Ligne
            var totalColCorrect = [0, 0, 0, 0];
            var totalCol = [0, 0, 0, 0];
            //Colonne
            var totalLigneCorrect = [];
            var totalLigne = [];

            for(i=0; i<10; i++){
            	totalLigneCorrect[i] = [0, 0, 0, 0];
            	totalLigne[i] = [0, 0, 0, 0];
            }

            for(i=0;i<11;i++){//Ligne
            	id_k = '#'+response.data[1].method+'_ligne'+i;
            	id_b = '#'+response.data[0].method+'_ligne'+i;
            	id_n = '#'+response.data[2].method+'_ligne'+i;
            	id_a = '#'+response.data[3].method+'_ligne'+i;
            	//On vide les matrices de confusion
				$(id_k).empty();
				$(id_b).empty();
				$(id_n).empty();
				$(id_a).empty();
				//Colonne&Ligne pourcentage
				if (i == 10){
					$(id_k).append('<th scope="row">percent</th>');
					$(id_b).append('<th scope="row">percent</th>');
					$(id_n).append('<th scope="row">percent</th>');
					$(id_a).append('<th scope="row">percent</th>');
				}
				else {
					$(id_k).append('<th scope="row">' + i + '</th>');
					$(id_b).append('<th scope="row">' + i + '</th>');
					$(id_n).append('<th scope="row">' + i + '</th>');
					$(id_a).append('<th scope="row">' + i + '</th>');
				}

				for(j=0; j<11; j++){//Colonne
					//Colonne&Ligne sur les pourcentages
					if(i == 10 || j == 10){
						if(i == j){
							var k = (totalCorrect[1]/total[1])*100;
							var b = (totalCorrect[0]/total[0])*100;
							var n = (totalCorrect[2]/total[2])*100;
							var a = (totalCorrect[3]/total[3])*100;
							$(id_k).append("<th class='"+getColorScheme(getPercentage(k))+"'>" + getPercentage(k) + "</th>");
							$(id_b).append("<th class='"+getColorScheme(getPercentage(b))+"'>" + getPercentage(b) + "</th>");
							$(id_n).append("<th class='"+getColorScheme(getPercentage(n))+"'>" + getPercentage(n) + "</th>");
							$(id_a).append("<th class='"+getColorScheme(getPercentage(a))+"'>" + getPercentage(a) + "</th>");
						}
						else if(j == 10){
							var k = (totalColCorrect[1]/totalCol[1])*100;
							var b = (totalColCorrect[0]/totalCol[0])*100;
							var n = (totalColCorrect[2]/totalCol[2])*100;
							var a = (totalColCorrect[3]/totalCol[3])*100;
							$(id_k).append("<th class='"+getColorScheme(getPercentage(k))+"'>" + getPercentage(k) + "</th>");
							$(id_b).append("<th class='"+getColorScheme(getPercentage(b))+"'>" + getPercentage(b) + "</th>");
							$(id_n).append("<th class='"+getColorScheme(getPercentage(n))+"'>" + getPercentage(n) + "</th>");
							$(id_a).append("<th class='"+getColorScheme(getPercentage(a))+"'>" + getPercentage(a) + "</th>");

							//Retour a zero pour une nouvelle ligne
							totalCol[0] = 0;//Total Bayesienne
							totalCol[1] = 0;//Total KVoisin
							totalCol[2] = 0;//Total Neural
							totalCol[3] = 0;
							totalColCorrect[0] = 0;//Total Bayesienne
							totalColCorrect[1] = 0;//Total KVoisin
							totalColCorrect[2] = 0;//Total Neural
							totalColCorrect[3] = 0;							

						}else{
							var k = (totalLigneCorrect[j][1]/totalLigne[j][1])*100;
							var b = (totalLigneCorrect[j][0]/totalLigne[j][0])*100;
							var n = (totalLigneCorrect[j][2]/totalLigne[j][2])*100;
							var a = (totalLigneCorrect[j][3]/totalLigne[j][3])*100;
							$(id_k).append("<th class='"+getColorScheme(getPercentage(k))+"'>" + getPercentage(k) + "</th>");
							$(id_b).append("<th class='"+getColorScheme(getPercentage(b))+"'>" + getPercentage(b) + "</th>");
							$(id_n).append("<th class='"+getColorScheme(getPercentage(n))+"'>" + getPercentage(n) + "</th>");
							$(id_a).append("<th class='"+getColorScheme(getPercentage(a))+"'>" + getPercentage(a) + "</th>");
						}
						continue;
					}

					//Colonne
					totalCol[0] += response.data[0].matrix[i][j];//Total Bayesienne
					totalCol[1] += response.data[1].matrix[i][j];//Total KVoisin
					totalCol[2] += response.data[2].matrix[i][j];//Total Neural
					totalCol[3] += response.data[3].matrix[i][j];//Total Neural
					//Ligne
					totalLigne[j][0] += response.data[0].matrix[i][j];
					totalLigne[j][1] += response.data[1].matrix[i][j];
					totalLigne[j][2] += response.data[2].matrix[i][j];
					totalLigne[j][3] += response.data[3].matrix[i][j];
					//Diag
					total[0] += response.data[0].matrix[i][j];//Total Bayesienne
					total[1] += response.data[1].matrix[i][j];//Total KVoisin
					total[2] += response.data[2].matrix[i][j];//Total Neural
					total[3] += response.data[3].matrix[i][j];//Total Neural

					if (i==j){
						$(id_k).append("<th class='ui-helper-green'>"+response.data[1].matrix[i][j]+"</th>");
						$(id_b).append("<th class='ui-helper-green'>"+response.data[0].matrix[i][j]+"</th>");
						$(id_n).append("<th class='ui-helper-green'>"+response.data[2].matrix[i][j]+"</th>");
						$(id_a).append("<th class='ui-helper-green'>"+response.data[3].matrix[i][j]+"</th>");
						//Ligne
						totalColCorrect[0] += response.data[0].matrix[i][j];
						totalColCorrect[1] += response.data[1].matrix[i][j];
						totalColCorrect[2] += response.data[2].matrix[i][j];
						totalColCorrect[3] += response.data[3].matrix[i][j];
						//Ligne
						totalLigneCorrect[j][0] += response.data[0].matrix[i][j];
						totalLigneCorrect[j][1] += response.data[1].matrix[i][j];
						totalLigneCorrect[j][2] += response.data[2].matrix[i][j];
						totalLigneCorrect[j][3] += response.data[3].matrix[i][j];
						//Diag
						totalCorrect[0] += response.data[0].matrix[i][j];
						totalCorrect[1] += response.data[1].matrix[i][j];
						totalCorrect[2] += response.data[2].matrix[i][j];
						totalCorrect[3] += response.data[3].matrix[i][j];
					}else{
						$(id_k).append("<th>"+response.data[1].matrix[i][j]+"</th>");
						$(id_b).append("<th>"+response.data[0].matrix[i][j]+"</th>");
						$(id_n).append("<th>"+response.data[2].matrix[i][j]+"</th>");
						$(id_a).append("<th>"+response.data[3].matrix[i][j]+"</th>");
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


function startTrain() {
	$('#loading').modal({
	    backdrop: 'static',
	    keyboard: false
	});
	$.ajax({
	    url: "/startTrain",
	    type: "post",
	    success: function(response){
	    	getMatrix();
	    	$('#loading').modal('toggle');
	    },
	    error: function(jqXHR,textStatus,errorThrown){
	    	alert(" !!! Une erreur a eu lieu voir la console pour plus d'info !!! ");
	    	console.log('jqXHR:');
	        console.log(jqXHR);
	        console.log('textStatus:');
	        console.log(textStatus);
	        console.log('errorThrown:');
	        console.log(errorThrown);

	        $('#loading').modal('toggle');
	    }
	});
}


function clearMatrices() {
	$.ajax({
	    url: "/resetMatrix",
	    type: "post",
	    success: function(response){
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
///////////
///////////
///////////


///////////
////FUN////
///////////

nbImg = 0;
tabIdImg = [];


function makeDiv(img,idimg){
    // vary size for fun
    var divsize = ((Math.random()*100) + 50).toFixed();
    $newdiv = $('<img id="boobs'+idimg+'" src="'+img+'" alt="load" onclick="stopImage('+idimg+')"></a>').css({
        'width':divsize+'px',
        'height':divsize+'px'
    });

    // make position sensitive to size and document's width
    var posx = (Math.random() * ($(document).width() - divsize)).toFixed();
    var posy = (Math.random() * ($(document).height() - divsize)).toFixed();

    $newdiv.css({
        'position':'absolute',
        'left':posx+'px',
        'top':posy+'px',
        'display':'none'
    }).appendTo( 'body' ).fadeIn(500).delay(1000).fadeOut(500, function(){
		$(this).remove();
		if(tabIdImg[idimg]){
			makeDiv(img,idimg);
		}
    }); 
}

function stopImage(idimg){
	tabIdImg[idimg] = false;
	$("#boobs"+idimg).animate({
        height: '150px',
        width: '150px'
    });
}


var k = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
var image = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4];
n = 0;
$(document).keydown(function (e) {
    if (e.keyCode === k[n++]) {
        if (n === k.length) {
        	//creer un random et choisir une des images gif pour le makeDiv

        	for(i = 0; i< 20; i++){
            	makeDiv('css/bounce'+image[Math.floor(Math.random() * image.length)]+'.gif',nbImg); // à remplacer par votre code
            	tabIdImg.push(true);
            	nbImg+=1;
            }
            n = 0;
            return false;
        }
    }
    else {
        n = 0;
    }
});

///////////
///////////
///////////




draw();
getMatrix();