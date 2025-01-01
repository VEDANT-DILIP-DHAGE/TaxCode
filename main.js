document.getElementById('salaried-option').addEventListener('click', function (event) {
    // event.preventDefault();
    // alert('Salaried Income option selected.');
    // Add functionality here for handling salaried income
});

document.getElementById('business-option').addEventListener('click', function (event) {
    //event.preventDefault();
    //alert('Business Income option selected.');
    // Add functionality here for handling business income
});

const faqToggleButton = document.getElementById('faq-toggle');
const faqContent = document.getElementById('faq-content');

faqToggleButton.addEventListener('click', function () {
    if (faqContent.style.display === 'none' || faqContent.style.display === '') {
        faqContent.style.display = 'block';
        // faqToggleButton.textContent = 'Hide FAQs';
        faqToggleButton.classList.add('collapsed');
    } else {
        faqContent.style.display = 'none';
        // faqToggleButton.textContent = 'Show FAQs';
        faqToggleButton.classList.remove('collapsed');
    }
});

const contactToggleButton = document.getElementById('contact-toggle');
const contactContent = document.getElementById('contact-content');

contactToggleButton.addEventListener('click', function () {
    if (contactContent.style.display === 'none' || contactContent.style.display === '') {
        contactContent.style.display = 'block';
        // contactToggleButton.textContent = 'Hide Contacts';
        contactToggleButton.classList.add('collapsed');
    } else {
        contactContent.style.display = 'none';
        // contactToggleButton.textContent = 'Show Contacts';
        contactToggleButton.classList.remove('collapsed');
    }
});

const aboutToggleButton = document.getElementById('about-toggle');
const aboutContent = document.getElementById('about-content');

aboutToggleButton.addEventListener('click', function () {
    if (aboutContent.style.display === 'none' || aboutContent.style.display === '') {
        aboutContent.style.display = 'block';
        // aboutToggleButton.textContent = 'Hide About';
        aboutToggleButton.classList.add('collapsed');
    } else {
        aboutContent.style.display = 'none';
        // aboutToggleButton.textContent = 'Show About';
        aboutToggleButton.classList.remove('collapsed');
    }
});
