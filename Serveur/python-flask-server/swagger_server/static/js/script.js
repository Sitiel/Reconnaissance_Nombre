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

//Dessine la grille
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

//Redessine en blanc la case cliquée
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

//Remets la grille a zero
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

//Si un null se trouve dans la grille il est remplacé par un -1
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

//Liée au bouton Add to train, demande quel nombre est dessiné puis envoie le dessin avec sa solution via JSON au serveur
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


//Fonction qui va envoyer en AJAX au format JSON l'image dessinée au serveur python
function sendToDB() {
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

//Fonction de couleur pour les matrices de confusion
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

//Corrige les erreurs liée au calcul de pourcentage dans la matrice (Nb chiffre après la virgule et division par 0)
function getPercentage(num){
	ret = 0
	if(isNaN(num)){
		return ret.toFixed(1);
	}else{
		return num.toFixed(1);
	}
}

//Demande au serveur les matrices de confusion du serveur puis va les afficher dans le site
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

            for(i=0;i<11;i++){//Lignes
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

				for(j=0; j<11; j++){//Colonnes
					//Colonne&Ligne sur les pourcentages
					if(i == 10 || j == 10){
						if(i == j){
							//Pourcentage de réussite
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
							//Pourcentage lignes
							var k = (totalColCorrect[1]/totalCol[1])*100;
							var b = (totalColCorrect[0]/totalCol[0])*100;
							var n = (totalColCorrect[2]/totalCol[2])*100;
							var a = (totalColCorrect[3]/totalCol[3])*100;
							$(id_k).append("<th class='"+getColorScheme(getPercentage(k))+"'>" + getPercentage(k) + "</th>");
							$(id_b).append("<th class='"+getColorScheme(getPercentage(b))+"'>" + getPercentage(b) + "</th>");
							$(id_n).append("<th class='"+getColorScheme(getPercentage(n))+"'>" + getPercentage(n) + "</th>");
							$(id_a).append("<th class='"+getColorScheme(getPercentage(a))+"'>" + getPercentage(a) + "</th>");

							//Retour a zero pour une nouvelle ligne
							for(k = 0; k<4; k++){
								totalCol[k] = 0;
								totalColCorrect[k] = 0;
							}		

						}else{
							//Pourcentage colonne
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

					for(k = 0; k<4; k++){
						//Colonne
						totalCol[k] += response.data[k].matrix[i][j];
						//Ligne
						totalLigne[j][k] += response.data[k].matrix[i][j];
						//Diag
						total[k] += response.data[k].matrix[i][j]; 
					}			


					if (i==j){
						$(id_k).append("<th class='ui-helper-green'>"+response.data[1].matrix[i][j]+"</th>");
						$(id_b).append("<th class='ui-helper-green'>"+response.data[0].matrix[i][j]+"</th>");
						$(id_n).append("<th class='ui-helper-green'>"+response.data[2].matrix[i][j]+"</th>");
						$(id_a).append("<th class='ui-helper-green'>"+response.data[3].matrix[i][j]+"</th>");

						for(k = 0; k<4; k++){
							//Ligne
							totalColCorrect[k] += response.data[k].matrix[i][j];
							//Ligne
							totalLigneCorrect[j][k] += response.data[k].matrix[i][j];
							//Diag
							totalCorrect[k] += response.data[k].matrix[i][j];
						}

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

//Demande au serveur de commencer l'entraînement des algorithmes
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

//Demande au serveur de vider les matrices
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

//Création d'une div et apparition dans des endroits aléatoire avec une taille aléatoire
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

//Faire disparaitre l'image si elle est cliquée
function stopImage(idimg){
	tabIdImg[idimg] = false;
	$("#boobs"+idimg).animate({
        height: '150px',
        width: '150px'
    });
}


//Fonction lecture du code konami :  haut,haut,bas,bas,gauche,droite,gauche,droite,b,a
var k = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
var image = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4];
n = 0;
$(document).keydown(function (e) {
    if (e.keyCode === k[n++]) {
        if (n === k.length) {
        	//creer un random et choisir une des images gif pour le makeDiv
        	for(i = 0; i< 10; i++){
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