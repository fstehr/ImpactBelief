let allRadios = document.querySelectorAll('input[type=radio]')

    function submitForm() {
        let form = document.getElementById('form');
        if (form.reportValidity()) {
            let switchingPoint = document.getElementById('id_switching_point');

            let allChoicesAreOnLeft = true;
            for (let radio of allRadios) {
                if (radio.value === 'right' && radio.checked) {
                    switchingPoint.value = radio.dataset.amount;
                    allChoicesAreOnLeft = false;
                    break;
                }
            }
            if (allChoicesAreOnLeft) {
                // '9999' represents the valueInput if the user didn't click the right side for any choice
                // it means their switching point is off the scale. you can change 9999 to some other valueInput
                // that is larger than any right-hand-side choice.
                switchingPoint.value = '9999';
            }
            form.submit();
        }
    }

    function onRadioClick(evt) {
        let clickedRadio = evt.target;
        let afterClickedRadio = false;
        let clickedRightRadio = clickedRadio.value === 'right';

        for (let aRadio of allRadios) {
            if (aRadio === clickedRadio) {
                afterClickedRadio = true;
                continue;
            }
            if (clickedRightRadio && afterClickedRadio && aRadio.value === 'right') {
                aRadio.checked = true;
            }
            if (!clickedRightRadio && !afterClickedRadio && aRadio.value === 'left') {
                aRadio.checked = true;
            }
        }
    }

    document.addEventListener("DOMContentLoaded", function (event) {
        for (let radio of document.querySelectorAll('input[type=radio]')) {
            radio.onchange = onRadioClick;
        }
    });
