/**
 * featured-image.js
 * Script to automatically unselect previous featured images in forms
 */

 /**
 *  Add event listeners when DOM is completely loaded
 *  equivalent to $(document).ready()
 */
document.addEventListener("DOMContentLoaded", function()
{
    var featured_checkboxes = document.querySelectorAll('.field-views_featured input[type=checkbox]');
    featured_checkboxes.forEach( function(c){
        c.addEventListener('click', function(){
            featured_checkboxes.forEach( function(c){ c.checked = false; });
            c.checked = true;
        })
    });
});
