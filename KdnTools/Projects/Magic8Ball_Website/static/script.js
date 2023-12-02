function move() {
    const elem = document.getElementById("myBar");
    const label = document.getElementById("label");
    let width = 0;
    let id = setInterval(frame, 20);

    function frame() {
        if (width >= 100) {
            clearInterval(id);
            setTimeout(function() {
                document.forms[0].submit();
            }, 500); // delay the form submission by 500ms
        } else {
            width += 5;
            elem.style.width = width + '%';
            label.textContent = width + '%';
        }
    }
}