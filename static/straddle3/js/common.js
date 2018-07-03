/**
 * common.js
 * Common scripts to be used throughout the site
 */


 /**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    var seemore_button = document.querySelector('.see-more');
    var body = document.querySelector('body');
    if(seemore_button){
        body.classList.add('trimmed-content');
        seemore_button.addEventListener('click', function(){
            body.classList.remove('trimmed-content');
        });
        document.querySelector('.see-less').addEventListener('click', function(){
            body.classList.add('trimmed-content');
        })
    }
    // Show navigation -- hamburguer icon in toolbar
    document.querySelector('.hamburguer-icon').onclick = function(){
        document.body.classList.toggle('navigation-open');
    };
});
