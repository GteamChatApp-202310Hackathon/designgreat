const flash = document.getElementById('visibility-flash');
if (flash != null){
    function buttonClick() {
        ;
    }
}else{
    const selecterBox = document.getElementById('visibility');
    let count = 0;

        function buttonClick() {
            count += 1;
            if (count % 2 == 0 ) {
                selecterBox.style.visibility = "visible";
            }        else {
                selecterBox.style.visibility = "hidden";
            }
        }
        window.addEventListener('load', buttonClick());
}

