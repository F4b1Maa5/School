document.querySelector('#ipv4').onclick = function () {
	var IPv4 = document.querySelector("#IPv4").value;
    var regex = /[0-9]{1,3}/g;
    var IPv4Parts = IPv4.match(regex);
    if(IPv4Parts.length != 4)
    {
        alert("No IPv4 address detected. Please check your input.");
        throw Error("Error");
    }
    IPv6Parts = [];
    IPv4Parts.forEach(quad => {
        //console.log("quad " + quad);
        var firstpart = parseInt(parseInt(quad) / 16);
        //console.log("firstpart "+firstpart);
        var secondpart = parseInt(quad) % 16;
        //console.log("secondpart "+secondpart);
        var hex1 = gethexvalue(firstpart);
        var hex2 = gethexvalue(secondpart);
        IPv6Parts.push(hex1 + "" + hex2);
    });
    IPv6Parts = setsemicolon(IPv6Parts);
    let string = "";
    IPv6Parts.forEach(element => {
        string =+ element;
    });
    document.querySelector('.output').innerHTML = string;
}

function gethexvalue(number) {
    hexnumber = '0';
    if (number == 10) {
        hexnumber = 'A';
    } else if (number == 11) {
        hexnumber = 'B';
    } else if (number == 12) {
        hexnumber = 'C';
    } else if (number == 13) {
        hexnumber = 'D';
    } else if (number == 14) {
        hexnumber = 'E';
    } else if (number == 15) {
        hexnumber = 'F';
    } else {
        hexnumber = number;
    }
    return hexnumber;
}

function setsemicolon(array){
    let temparray = [];
    for (let index = 0; index < array.length-1; index++) {
        const element = array[index];
        temparray.push(":"+element +"" + array[index+1])
    }
    return temparray;
}