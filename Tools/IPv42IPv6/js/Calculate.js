document.querySelector('#ipv4').onclick = function () {
	var IPv4 = document.querySelector("#IPv4").value;
	var IPv6Prefix = document.querySelector("#IPv6Prefix").value;
    var regex = /[0-9]{1,3}/g;
    var IPv4Parts = IPv4.match(regex);
    if(IPv4Parts.length != 4)
    {
        alert("No IPv4 address detected. Please check your input.");
        throw Error("Error");
    }
    IPv6Parts = [];
    IPv4Parts.forEach(quad => {
        var firstpart = parseInt(parseInt(quad) / 16);
        var secondpart = parseInt(quad) % 16;
        var hex1 = gethexvalue(firstpart);
        var hex2 = gethexvalue(secondpart);
        IPv6Parts.push(hex1 + "" + hex2);
    });
    IPv6Parts = setsemicolon(IPv6Parts);
    string = "";
    IPv6Parts.forEach(element => {
        string = string + element;
    });
    document.querySelector('.output').innerHTML = IPv6Prefix+ ":"+ string;
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
    for (let index = 0; index < array.length-1; index+=2) {
        const element = array[index];
        temparray.push(":"+element +"" + array[index+1])
    }
    return temparray;
}


document.querySelector('#mac').onclick = function () {
	var MAC = document.querySelector("#MAC").value;
	var IPv6Prefix = document.querySelector("#IPv6Prefix").value;
    MacArray = MAC.split(":")
    
    MacArray[0] = flipHex(MacArray[0]);

    MacArray.splice(3,0,"FF");
    MacArray.join();
    MacArray.splice(4,0,"FE");
    MacArray.join();


    MacArray = setsemicolon(MacArray);
    string = "";
    MacArray.forEach(element => {
        string = string + element;
    });
    document.querySelector('.output').innerHTML = IPv6Prefix + string;
 }

function flipHex(hextoflip){
    HexArraySplit = hextoflip.split("",2);
    console.log(HexArraySplit[1]);
    bit = parseInt(HexArraySplit[1],16).toString(2);
    console.log(bit);
    bittoflip = bit.split("",4);
    console.log(bittoflip[2]);
    switch (bittoflip[2]) {
        case "1":
            bittoflip[2] = 0; 
            break;
        case "0":
            bittoflip[2] = 1;
            break
        default:
            throw new Error("Not Implemented");
    }
    flipped = bittoflip.join('');
    hex = parseInt(flipped,2).toString(16).toUpperCase();
    HexArraySplit[1] = hex;
    return HexArraySplit.join('');
}