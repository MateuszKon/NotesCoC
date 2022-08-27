window.oncontextmenu = function (e) {
    e.preventDefault();

    if (e.target.className == "notebook-h1" || e.target.className == "note-h1") {
        for (var i = 0; i < document.getElementsByClassName("contextmenu").length; i++) {
            document.getElementsByClassName("contextmenu")[i].style.display = "none";
        }
        var grandparentId = e.target.parentElement.parentElement.id;
        var grandparent = document.getElementById(grandparentId);
        grandparent.querySelector("#contextmenu").style.display = "block";
    }
}

window.onclick = function () {
    for (var i = 0; i < document.getElementsByClassName("contextmenu").length; i++) {
        document.getElementsByClassName("contextmenu")[i].style.display = "none";
    }
}


var counter = 0;
function toggleSettings(){
    counter++;
    if(counter % 2 != 0){
        document.getElementById("settings").style.display="none";
    }
    else{
        document.getElementById("settings").style.display="block";
    }

}

// Set a Cookie
function setCookie(cName, cValue, expDays) {
        document.cookie = cName + "=" + cValue;
}
// Apply setCookie
// setCookie('username', username);

// Get a Cookie
function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie); //to be careful
      const cArr = cDecoded .split('; ');
      let res;
      cArr.forEach(val => {
          if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
}

function deleteCookie(cName) {
    document.cookie = cName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC";
}

function setVisibilityCookie(name) {
    let vis = name;
    if (vis == "all") {
        deleteCookie("visibility_selection")
    } else {
        setCookie("visibility_selection", vis)
    }

}
