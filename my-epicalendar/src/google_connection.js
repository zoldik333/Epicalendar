var client;
var access_token;

function initClient() {
    client = google.accounts.oauth2.initTokenClient({
        client_id: '490850150345-slrqug5oghlih3565ubimrte8epeprda.apps.googleusercontent.com',
        scope: 'https://www.googleapis.com/auth/calendar.readonly',
        callback: (tokenResponse) => {
            access_token = tokenResponse.access_token;
            loadCalendar();
        },
    });
}
function getToken() {
    client.requestAccessToken();
}
function revokeToken() {
    google.accounts.oauth2.revoke(access_token, () => {console.log('access token revoked')});
}
function loadCalendar() {
    /*var xhr = new XMLHttpRequest();
    xhr.open('GET', 'https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=2023-01-01T00:00:00Z');
    xhr.setRequestHeader('Authorization', 'Bearer ' + access_token);
    xhr.send();*/
    $.ajax({
        url: "https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=2000&timeMin="+(new Date(2023, 01, 01)).toISOString(),
        method: "GET",
        headers: {'Authorization': 'Bearer ' + access_token},
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: false,
        cache: false,
        success: function (response) {
            console.log(response);
            for (let i = 0; i < response.items.length; i++) {
                let event = {title: response.items[i].summary,
                    start: response.items[i].start.dateTime,
                    end: response.items[i].end.dateTime
                };
                console.log(event);
                calendar.addEvent(event);
            }
        }
    });
}
