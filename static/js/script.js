

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
        deleteCookie("admin_visibility")
    } else {
        setCookie("admin_visibility", vis)
    }

}

function expandNotes() {
    let collection = document.getElementsByClassName("note-header");
    for (var i = 0; i < collection.length; i++){
        collection[i].classList.add('show');
    }
}

function collapseNotes() {
    let collection = document.getElementsByClassName("note-header");
    for (var i = 0; i < collection.length; i++){
        collection[i].classList.remove('show');
    }
}


function setHeight(fieldId){
    document.getElementById(fieldId).style.height = document.getElementById(fieldId).scrollHeight+'px';
}