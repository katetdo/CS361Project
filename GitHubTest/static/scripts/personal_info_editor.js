/*
author: Connor Oaks
This script allows users to submit changes to their personal info.
 */

const ENTER = 13

function updateInfo(event) {
    if(event.keyCode === ENTER) {
        event.target.parentElement.submit();
    }
}

