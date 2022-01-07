/**
 * @author AH.SALAH
 * @email https://github.com/AH-SALAH
 * @create date 2022-01-06 23:23:16
 * @modify date 2022-01-06 23:23:35
 * @desc [bootstrap init]
 */


let useTooltip = () => {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    if (tooltipTriggerList.length) {
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
};
useTooltip();

let useToast = () => {
    let toastTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="toast"]'))
    if (toastTriggerList.length) {
        ToastTriggerList.map(toastTriggerEl => new bootstrap.Toast(toastTriggerEl));
    }
};
useToast();

let useCollapse = () => {
    function getIcon(ele) {
        if (!ele) return false;
        let trigger = document.querySelector('[href="#' + ele.id + '"], [data-bs-target="#' + ele.id + '"]');
        if (!trigger) return false;
        let trigger_icon = trigger.querySelector('[class*=fa-]');
        return trigger_icon || false;
    }
    function changeIconClass(icon, removeClass, addClass) {
        if (!icon) return false;
        icon.classList.replace(removeClass, addClass);
    }

    let collapseTriggerList = [].slice.call(document.querySelectorAll('.collapse'))

    if (!collapseTriggerList.length) return false;

    collapseTriggerList.forEach(el => {
        el.addEventListener('shown.bs.collapse', event => {
            let icon = getIcon(event.target);
            changeIconClass(icon, 'fa-plus', 'fa-minus');
        });
        el.addEventListener('hidden.bs.collapse', event => {
            let icon = getIcon(event.target);
            changeIconClass(icon, 'fa-minus', 'fa-plus');
        });
    });
};
useCollapse();