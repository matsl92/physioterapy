const loginPageSelector = document.getElementById('pills-login-tab');
const historyPageSelector = document.getElementById('pills-history-tab');
const indexPageSelector = document.getElementById('pills-index-tab');

const loginPane = document.getElementById('pills-login');
const historyPane = document.getElementById('pills-history');
const indexPane = document.getElementById('pills-index');

const panes = document.querySelectorAll('.tab-pane');

const links = document.querySelectorAll('.nav-link');
links.forEach(link => {
    link.addEventListener('click', (e) => {
        // e.preventDefault();
        toggleTabs(e);
    })
})




function toggleTabs(e) {

    links.forEach(link => {
        if (link === e.target) {
            link.classList.toggle('active');
        } else {
            link.classList.remove('active');
        }
        
        if (link.classList.contains('active')) {
            link.setAttribute('aria-selected', 'true');
        } else {
            link.setAttribute('aria-selected', 'false');
            
        }
    })

    let relatedPaneId = e.target.getAttribute('aria-controls');
    let relatedPane = document.getElementById(relatedPaneId);

    panes.forEach(pane => {
        pane.classList.remove('show', 'active');
    })

    if (e.target.classList.contains('active')) {
        relatedPane.classList.add('show', 'active');
    } else {
        relatedPane.classList.remove('show', 'active');
    }

    // e.target.classList.contains('active')? relatedPane.classList.add('show', 'active') : 
    // relatedPane.classList.remove('show', 'active');


    if (checkforActivePane()) {
        deactivateIndexPane();
    } else {
        activateIndexPane();
    }

}

// toggle tab

// toggle pane

// if not active
//     index active
// else
//     index inactive

function checkforActivePane() {
    let isThereAnyActive = false;
    panes.forEach(pane => {
        if (pane.classList.contains('active')) {
            isThereAnyActive = true
        }
    })

    return isThereAnyActive;
}

function activateIndexPane() {
    indexPageSelector.classList.add('active');
    indexPane.classList.add('show', 'active');
}

function deactivateIndexPane() {
    indexPageSelector.classList.remove('active');
    indexPane.classList.remove('show', 'active');
}