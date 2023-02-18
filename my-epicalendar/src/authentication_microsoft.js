function verification_mail_string(email) {
    let re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

function verification_mail() {
    let email = document.getElementById('email').value;
    if (verification_mail_string(email) === false) {
        document.getElementById('email').style.borderColor="red";
        return false;
    } else {
        document.getElementById('email').style.borderColor="gray";
        return true;
    }
}
