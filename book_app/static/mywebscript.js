let GenerateRecom = ()=>{
    ISBN = document.getElementById("ISBN").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("input_isbn").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "RecommendBooks?ISBN"+"="+ISBN, true);
    xhttp.send();
}


