var tChange = false;
var dChange = false;
var reserved = ["A2", "C8", "D20"];

var prevA = 0;
var prevC = 0;
var prevS = 0;


function checkForRestriction(restriction){
    if(restriction == 'R'){
        var childBox = document.getElementById('childQuantity');
        childBox.disabled = true;
    }
}

function changeTime(){
    tChange = true;
                     
    if(tChange == true && dChange == true){

        var time = document.getElementById('time').textContent;
        showHidden(time);
    }
}

function changeDate(){
    dChange = true;
                     
    if(tChange == true && dChange == true){
        var time = document.getElementById('time').textContent;
        showHidden(time);
    }
}

function isReserved(row, seat){
    var seatNum = row.concat(seat.toString());
    var len =  reserved.length;

    for(i = 0; i < len; i ++){
    //window.alert(reserved[i]);
        if (reserved[i] == seatNum){
            return true;
        }
    }

    return false;
}


function showHidden(){
    document.getElementById('hiddenDisplay').className = 'container shown-details';

    //Clear previous seating
    const myNode = document.getElementById("seats");
    while (myNode.firstChild) {
        myNode.removeChild(myNode.lastChild);
    }

    var element = document.createElement("div");

    element.innerHTML = "SCREEN";
    element.style.textAlign = 'center';
    element.style.position = "absolute";
    element.style.border = "1px solid rgb(0,0,0)";
    element.style.height = "30px";
    element.style.width = "750px";

    var foo = document.getElementById("seats");

    foo.appendChild(element);

    var linebreak = document.createElement("br");
    foo.appendChild(linebreak);
    var linebreak1 = document.createElement("br");
    foo.appendChild(linebreak1);
    var linebreak2 = document.createElement("br");
    foo.appendChild(linebreak2);

    for(row = 0; row < 5; row++){
        for(seat = 0; seat < 25; seat++){
            var element;
            if(seat == 0 || seat == 24){
                element = document.createElement("button");
                element.disabled = true;
                element.style.background = "white";
                element.style.color = "black";
                element.name = "letter";

                element.textContent = String.fromCharCode(65 + row);
            }else {
                if(isReserved(String.fromCharCode(65 + row), seat) == true){
                    //Create an input type dynamically.   
                    element = document.createElement("button");
                    //Assign different attributes to the element.
                    element.disabled = true; 
                    element.name = "button";
                    element.style.background = "#666666";
                    element.onclick = function() { // Note this is a function
                        alert("Seat Unavailable");
                    };
                }else{
                    //Create an input type dynamically.   
                    element = document.createElement("button");
                    //Assign different attributes to the element. 
                    element.name = "button";
                    element.style.background = "#dbdad7";
                    element.onclick = function() { // Note this is a function
                        userSelect();
                    };
                }

                element.style.color = "black";
                element.textContent = seat;

            }

            element.style.height = "30px";
            element.style.width = "30px";
            //Append the element in page (in span).  
            foo.appendChild(element);

        }
                            
    }

}

function changeAdult(){
    var quantity = document.getElementById("adultQuantity").value;
    document.getElementById("tableAQ").innerHTML = quantity;

    var total = document.getElementById("total").textContent;
    var res = total.substr(8);
    var newTotal = 0;

    if(quantity > prevA){
        newTotal = Math.round(res) + 10;
    }else{
        newTotal = Math.round(res) - 10;
    }

    prevA = quantity;
    document.getElementById("total").innerHTML = "Total: £" + newTotal + ".00";
}

function changeChild(){
    var quantity = document.getElementById("childQuantity").value;
    document.getElementById("tableCQ").innerHTML = quantity;

    var total = document.getElementById("total").textContent;
    var res = total.substr(8);
    var newTotal = 0;

    if(quantity > prevC){
        newTotal = Math.round(res) + 6;
    }else{
        newTotal = Math.round(res) - 6;
    }

    prevC = quantity;
    document.getElementById("total").innerHTML = "Total: £" + newTotal + ".00";
}

function changeSenior(){
    var quantity = document.getElementById("seniorQuantity").value;
    document.getElementById("tableSQ").innerHTML = quantity;

    var total = document.getElementById("total").textContent;
    var res = total.substr(8);
    var newTotal = 0;

    if(quantity > prevS){
        newTotal = Math.round(res) + 6;
    }else{
        newTotal = Math.round(res) - 6;
    }

    prevS = quantity;
    document.getElementById("total").innerHTML = "Total: £" + newTotal + ".00";
}